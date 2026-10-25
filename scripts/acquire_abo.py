"""Remote-only acquisition of a bounded ABO jeans screening set; no labels inferred."""

import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from urllib.request import urlopen


BASE = 'https://amazon-berkeley-objects.s3.amazonaws.com/'


def jeans_candidate(item):
    names = ' '.join(row.get('value', '') for row in item.get('item_name', [])
                     if row.get('language_tag', '').startswith('en'))
    # Screening only: use titles, not a denim-colored product or a mention in marketing copy.
    title = names.lower()
    return (bool(re.search(r'\bjeans\b|\bdenim\b.*\b(pants|trousers)\b', title))
            and not re.search(r'\b(shorts|skirt|jacket|shirt|dress|jumpsuit|dungarees|'
                              r'phone|iphone|samsung|case|cover|shoe|shoes|sneaker|sneakers)\b', title))


def image_path(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{2}/[0-9a-f]+\.(jpg|png)', value):
        raise ValueError('Unexpected official image path')
    return value


def download(url, target, maximum):
    with urlopen(url, timeout=90) as source, target.open('xb') as output:
        size = 0
        while chunk := source.read(1024 * 1024):
            size += len(chunk)
            if size > maximum:
                raise ValueError('Download exceeded size bound')
            output.write(chunk)
    return hashlib.sha256(target.read_bytes()).hexdigest()


def main():
    if not Path('/kaggle/working').is_dir():
        raise RuntimeError('Acquire on Kaggle CPU, not the laptop')
    from PIL import Image
    root = Path('/kaggle/working') / ('abo_jeans_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    root.mkdir(exist_ok=False)
    (root / 'images').mkdir()
    print('Output:', root, flush=True)
    sources = {}
    for remote in ['LICENSE-CC-BY-4.0.txt', 'README.md', 'listings/README.md', 'images/README.md']:
        target = root / remote.replace('/', '_')
        sources[remote] = download(BASE + remote, target, 1000000)
    archive = root / 'abo-listings.tar'
    sources['archives/abo-listings.tar'] = download(BASE + 'archives/abo-listings.tar', archive, 120000000)
    candidates, total = [], 0
    with tarfile.open(archive) as bundle:
        for member in bundle:
            if not member.isfile() or not member.name.endswith('.json.gz'):
                continue
            # Read members as streams; never extract archive paths onto disk.
            with gzip.open(bundle.extractfile(member), 'rt', encoding='utf-8') as stream:
                for line in stream:
                    item = json.loads(line)
                    total += 1
                    if jeans_candidate(item):
                        candidates.append(item)
    with (root / 'candidate_listings.jsonl').open('x', encoding='utf-8') as output:
        for item in candidates:
            output.write(json.dumps(item, ensure_ascii=False) + '\n')
    print('Listings:', total, 'jeans title candidates:', len(candidates), flush=True)
    metadata = root / 'images.csv.gz'
    sources['images/metadata/images.csv.gz'] = download(BASE + 'images/metadata/images.csv.gz', metadata, 40000000)
    wanted = {}
    for item in candidates:
        for key in [item.get('main_image_id'), *item.get('other_image_id', [])]:
            if key:
                wanted.setdefault(key, []).append({'item_id': item['item_id'], 'domain_name': item['domain_name']})
    selected = []
    with gzip.open(metadata, 'rt', encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            if row['image_id'] in wanted:
                image_path(row['path'])
                selected.append(row)
    selected.sort(key=lambda row: row['image_id'])
    # shortcut: first 600 IDs bound this acquisition pilot; sample representatively after visual review.
    selected = selected[:600]

    def fetch(row):
        path = image_path(row['path'])
        target = root / 'images' / PurePosixPath(path).name
        url = BASE + 'images/original/' + path
        try:
            checksum = download(url, target, 25000000)
            with Image.open(target) as image:
                image.verify()
            with Image.open(target) as image:
                dimensions = list(image.size)
                mode = image.mode
            return {'image_id': row['image_id'], 'file': 'images/' + target.name,
                    'source_url': url, 'sha256': checksum, 'size': dimensions, 'mode': mode,
                    'source_listings': wanted[row['image_id']], 'license': 'CC-BY-4.0',
                    'attribution': 'Amazon.com; ABO dataset creators (see README)',
                    'denim_status': 'unreviewed', 'crop_status': 'unreviewed',
                    'product_group_status': 'source_listing_ids_unreviewed', 'research_split': None}
        except Exception as error:
            return {'image_id': row['image_id'], 'error': type(error).__name__ + ': ' + str(error), 'source_url': url}

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(fetch, selected))
    successful = [row for row in results if 'error' not in row]
    failed = [row for row in results if 'error' in row]
    with (root / 'screening_images.jsonl').open('x', encoding='utf-8') as output:
        for row in successful:
            output.write(json.dumps(row) + '\n')
    (root / 'download_errors.json').write_text(json.dumps(failed, indent=2), encoding='utf-8')
    summary = {'complete': True, 'source': BASE + 'index.html', 'license': 'CC-BY-4.0',
               'source_sha256': sources, 'listing_count': total, 'candidate_listing_count': len(candidates),
               'candidate_unique_images': len(wanted), 'attempted_images': len(selected),
               'downloaded_verified_images': len(successful), 'failed_images': len(failed),
               'image_bytes': sum((root / row['file']).stat().st_size for row in successful),
               'confirmed_denim': 0, 'training_ready': 0, 'output': str(root),
               'notes': 'Title-screened pilot only. No crops, relevance labels or research splits inferred.'}
    (root / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
