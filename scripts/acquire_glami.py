"""Remote-only GLAMI-1M jeans subset acquisition via range-readable official ZIP."""

import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.request import urlopen
import zipfile


def jeans_candidate(row):
    return (row.get('category_name') in {'mens-pants', 'womens-pants', 'boys-pants', 'girls-pants'}
            and bool(re.search(r'\b(jeans|denim)\b', row.get('name', '') + ' ' +
                               row.get('description', ''), flags=re.IGNORECASE)))


def main():
    if not Path('/kaggle/working').is_dir():
        raise RuntimeError('Acquire on remote Kaggle CPU')
    import fsspec
    from PIL import Image
    repo = 'https://huggingface.co/datasets/glami/glami-1m/'
    revision = json.load(urlopen('https://huggingface.co/api/datasets/glami/glami-1m', timeout=60))['sha']
    url = repo + 'resolve/' + revision + '/GLAMI-1M-dataset.zip'
    root = Path('/kaggle/working') / ('glami_jeans_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    root.mkdir(exist_ok=False)
    (root / 'images').mkdir()
    print('GLAMI output:', root, 'revision:', revision, flush=True)
    # HTTPFile refuses unsupported range reads rather than silently downloading the entire archive.
    with fsspec.open(url, 'rb', block_size=2**20, cache_type='readahead') as remote:
        with zipfile.ZipFile(remote) as archive:
            names = archive.namelist()
            print('Archive members:', len(names), 'sample:', names[:5], flush=True)
            rows = []
            csv_names = [name for name in names if re.search(r'GLAMI-1M-(train|test)\.csv$', name)]
            if not csv_names:
                raise ValueError('Expected official train/test CSV files')
            for name in csv_names:
                with archive.open(name) as stream:
                    raw = stream.read(350000001)
                if len(raw) > 350000000:
                    raise ValueError('CSV exceeds size bound')
                (root / Path(name).name).write_bytes(raw)
                for row in csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))):
                    if jeans_candidate(row):
                        row['source_split'] = 'train' if name.endswith('-train.csv') else 'test'
                        rows.append(row)
            with (root / 'jeans_rows.jsonl').open('x', encoding='utf-8') as output:
                for row in rows:
                    output.write(json.dumps(row, ensure_ascii=False) + '\n')
            image_members = {Path(name).stem: name for name in names if name.endswith('.jpg')}
            image_ids = sorted({row['image_id'] for row in rows})[:300]
            if not image_ids:
                raise ValueError('No jeans screening candidates; acquisition incomplete')
            print('Jeans rows:', len(rows), 'selected images:', len(image_ids), flush=True)
            manifest = []
            for image_id in image_ids:
                if not re.fullmatch(r'[0-9]+', image_id):
                    raise ValueError('Unexpected image ID')
                member = image_members[image_id]
                with archive.open(member) as stream:
                    raw = stream.read(10000001)
                if len(raw) > 10000000:
                    raise ValueError('Image too large')
                with Image.open(io.BytesIO(raw)) as image:
                    image.verify()
                (root / 'images' / (image_id + '.jpg')).write_bytes(raw)
                manifest.append({'image_id': image_id, 'file': 'images/' + image_id + '.jpg',
                                 'sha256': hashlib.sha256(raw).hexdigest(), 'denim_status': 'unreviewed',
                                 'crop_status': 'unreviewed', 'research_split': None})
            with (root / 'screening_images.jsonl').open('x', encoding='utf-8') as output:
                for row in manifest:
                    output.write(json.dumps(row) + '\n')
    card = urlopen(repo + 'resolve/' + revision + '/README.md', timeout=60).read()
    (root / 'SOURCE_README.md').write_bytes(card)
    summary = {'complete': True, 'source': repo, 'revision': revision,
               'license': 'apache-2.0 (official dataset card)', 'candidate_rows': len(rows),
               'downloaded_verified_images': len(manifest),
               'image_bytes': sum((root / row['file']).stat().st_size for row in manifest),
               'output': str(root), 'confirmed_denim': 0, 'training_ready': 0,
               'selection': 'First 300 unique IDs: pants category plus jeans/denim in title or description; screening only',
               'notes': 'Range reads from official ZIP; no complete-archive checksum claim. Source splits are not research splits.'}
    (root / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
