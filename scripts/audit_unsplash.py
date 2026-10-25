"""Remote metadata-only denim screen of the officially licensed Unsplash Lite ZIP."""

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile


def denim_text(value):
    return bool(re.search(r'\b(jeans|denim)\b', value or '', re.IGNORECASE))


def audit_archive(archive, output):
    output.mkdir(exist_ok=False)
    keywords = defaultdict(set)
    counts = Counter()
    candidates, seen = [], set()
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        for table in ['photos', 'keywords']:
            if not any(re.fullmatch(table+r'\.tsv[0-9]*', name) for name in names):
                raise ValueError('Missing table: '+table)
        for name in names:
            if not re.fullmatch(r'keywords\.tsv[0-9]*', name):
                continue
            with bundle.open(name) as raw, io.TextIOWrapper(raw, encoding='utf-8-sig', newline='') as stream:
                reader = csv.DictReader(stream, delimiter='\t')
                if not {'photo_id', 'keyword'} <= set(reader.fieldnames or []):
                    raise ValueError('Unexpected keywords schema')
                for row in reader:
                    counts['keyword_rows'] += 1
                    if denim_text(row['keyword']):
                        keywords[row['photo_id']].add(row['keyword'])
        for name in names:
            if not re.fullmatch(r'photos\.tsv[0-9]*', name):
                continue
            with bundle.open(name) as raw, io.TextIOWrapper(raw, encoding='utf-8-sig', newline='') as stream:
                reader = csv.DictReader(stream, delimiter='\t')
                required = {'photo_id','photo_url','photo_image_url','photo_description','ai_description'}
                if not required <= set(reader.fieldnames or []):
                    raise ValueError('Unexpected photos schema')
                for row in reader:
                    identity = row['photo_id']
                    if not identity or identity in seen:
                        raise ValueError('Missing or duplicate photo ID')
                    seen.add(identity)
                    counts['photo_rows'] += 1
                    description_match = denim_text(row['photo_description']) or denim_text(row['ai_description'])
                    if not (identity in keywords or description_match):
                        continue
                    counts['keyword_matched_photos'] += identity in keywords
                    counts['description_matched_photos'] += description_match
                    # Preserve useful source data, not unnecessary location coordinates.
                    selected = {key:row.get(key,'') for key in ['photo_id','photo_url','photo_image_url',
                                'photo_width','photo_height','photo_description','ai_description','photographer_username']}
                    candidates.append(dict(selected, matched_keywords=sorted(keywords.get(identity,[])),
                                           denim_status='unreviewed', crop_status='unreviewed', research_split=None))
        if not seen:
            raise ValueError('Empty photos table')
        terms_hash = None
        if 'TERMS.md' in names:
            terms = bundle.read('TERMS.md')
            (output/'TERMS.md').write_bytes(terms)
            terms_hash = hashlib.sha256(terms).hexdigest()
    with (output/'denim_candidates.jsonl').open('x', encoding='utf-8') as stream:
        for row in candidates:
            stream.write(json.dumps(row, ensure_ascii=False)+'\n')
    with archive.open('rb') as stream:
        checksum = hashlib.file_digest(stream,'sha256').hexdigest()
    summary = {'schema_version':1, 'complete':True, **dict(counts),
               'candidate_photos':len(candidates), 'archive_bytes':archive.stat().st_size,
               'archive_sha256':checksum, 'packaged_terms_sha256':terms_hash,
               'images_downloaded':0, 'confirmed_denim':0, 'training_ready':0,
               'selection':'jeans or denim as whole word in keywords, human description or AI description',
               'notes':'Metadata matches only. No wearing-photo confirmation, rights transfer, model run, relevance grades or research split.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not Path('/kaggle/working').is_dir():
        raise RuntimeError('Run bulk metadata processing on remote Kaggle')
    print(json.dumps(audit_archive(args.archive,args.output),indent=2))
