"""Inspect public validation annotations remotely; never download images or assign splits."""

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import urllib.request

SOURCE_URL = 'https://s3.amazonaws.com/ifashionist-dataset/annotations/instances_attributes_val2020.json'
SOURCE_PAGE = 'https://github.com/cvdfoundation/fashionpedia'


def build_candidates(data):
    """Preserve source labels; a pants annotation is not a confirmed denim item."""
    maps = {}
    for key in ['images', 'categories', 'attributes', 'licenses']:
        maps[key] = {item['id']: item for item in data[key]}
        if len(maps[key]) != len(data[key]):
            raise ValueError('Duplicate IDs in ' + key)
    pants_ids = {key for key, value in maps['categories'].items() if value['name'].lower() == 'pants'}
    if not pants_ids:
        raise ValueError('No pants category; review the source taxonomy.')
    rows = []
    seen = set()
    for annotation in data['annotations']:
        if annotation['id'] in seen:
            raise ValueError('Duplicate annotation ID')
        seen.add(annotation['id'])
        if annotation['category_id'] not in pants_ids:
            continue
        image = maps['images'][annotation['image_id']]
        width, height = image['width'], image['height']
        bbox = annotation['bbox']
        if width <= 0 or height <= 0 or len(bbox) != 4 or not all(math.isfinite(v) for v in bbox):
            raise ValueError('Invalid dimensions/bbox for annotation ' + str(annotation['id']))
        x, y, w, h = bbox
        if w <= 0 or h <= 0:
            raise ValueError('Non-positive bbox for annotation ' + str(annotation['id']))
        raw_box = [x, y, x + w, y + h]
        clipped = [max(0, x), max(0, y), min(width, x + w), min(height, y + h)]
        if clipped[0] >= clipped[2] or clipped[1] >= clipped[3]:
            raise ValueError('Box outside image for annotation ' + str(annotation['id']))
        license_info = maps['licenses'].get(image.get('license'))
        attribute_names = [maps['attributes'][key]['name'] for key in annotation['attribute_ids']]
        rows.append({
            'id': 'fashionpedia-val-' + str(annotation['id']),
            'image_id': image['id'], 'annotation_id': annotation['id'],
            'file_name': image['file_name'], 'source_dataset_split': 'val2020',
            'source_page': SOURCE_PAGE, 'original_url': image.get('original_url'),
            'image_size': [width, height], 'source_bbox_xywh': bbox,
            'crop_xyxy_normalized': [clipped[0]/width, clipped[1]/height, clipped[2]/width, clipped[3]/height],
            'bbox_clipped': clipped != raw_box,
            'source_attributes': attribute_names,
            'source_jeans_label': 'jeans' in attribute_names,
            'source_washed_label': 'washed' in attribute_names,
            'has_segmentation': bool(annotation.get('segmentation')),
            'iscrowd': annotation.get('iscrowd'),
            'source_license_metadata': license_info,
            'rights_status': 'source_verification_pending',
            'denim_status': 'unreviewed', 'product_group_id': None,
            'duplicate_group_id': None, 'split': None,
        })
    summary = {
        'source_images': len(data['images']), 'source_annotations': len(data['annotations']),
        'pants_instances': len(rows), 'pants_images': len({row['image_id'] for row in rows}),
        'denim_named_attributes': [a for a in data['attributes'] if 'denim' in a['name'].lower()],
        'pants_attribute_counts': dict(sorted(Counter(a for row in rows for a in row['source_attributes']).items())),
        'pants_license_counts': dict(Counter(
            row['source_license_metadata']['name'] if row['source_license_metadata'] else 'missing'
            for row in rows)),
        'pants_missing_original_url': sum(not row['original_url'] for row in rows),
        'source_jeans_candidates': sum(row['source_jeans_label'] for row in rows),
        'jeans_license_counts': dict(Counter(
            row['source_license_metadata']['name'] if row['source_license_metadata'] else 'missing'
            for row in rows if row['source_jeans_label'])),
        'clipped_bbox_count': sum(row['bbox_clipped'] for row in rows),
        'confirmed_denim_instances': 0, 'training_ready_instances': 0,
        'images_downloaded': 0, 'research_splits_assigned': False,
    }
    assert all(row['split'] is None and row['denim_status'] == 'unreviewed' for row in rows)
    return rows, summary


def main():
    root = Path('/kaggle/working')
    if not root.is_dir():
        raise RuntimeError('Run this acquisition on the remote Kaggle CPU runtime.')
    source = root / 'fashionpedia_val2020.json'
    if source.exists():
        raw = source.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
            raw = response.read(20 * 1024**2 + 1)
    if len(raw) > 20 * 1024**2:
        raise ValueError('Annotation size exceeded 20 MiB; review before downloading more.')
    rows, summary = build_candidates(json.loads(raw))
    source_hash = hashlib.sha256(raw).hexdigest()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    target = root / ('fashionpedia_audit_' + stamp)
    target.mkdir()
    (target / 'source_annotations.json').write_bytes(raw)
    manifest = target / 'pants_candidates.jsonl'
    manifest.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
    assert len(manifest.read_text(encoding='utf-8').splitlines()) == len(rows)
    summary.update({'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
                    'source_url': SOURCE_URL, 'source_sha256': source_hash,
                    'source_bytes': len(raw), 'output_directory': target.name,
                    'annotation_attribution': 'Fashionpedia Consortium, CC BY 4.0; selected metadata and normalized boxes derived here',
                    'annotation_license': 'https://creativecommons.org/licenses/by/4.0/'})
    (target / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))
    print('Output:', target)


if __name__ == '__main__':
    main()
