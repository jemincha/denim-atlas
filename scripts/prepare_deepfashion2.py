"""Remote metadata screening after authorized dataset acquisition; no images or labels inferred."""

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path


def trousers_candidates(data, image_id, source_split):
    if len(image_id) != 6 or not image_id.isascii() or not image_id.isdecimal():
        raise ValueError('Expected a six-digit source image ID')
    if source_split not in {'train', 'validation'}:
        raise ValueError('Use one original annotated partition per manifest')
    if data.get('source') not in {'shop', 'user'}:
        raise ValueError('Unknown image source')
    pair_id = data.get('pair_id')
    if pair_id is not None and (type(pair_id) is not int or pair_id < 0):
        raise ValueError('Invalid pair_id')
    # Conservative group: keep every style sharing this pair ID together.
    group = f'deepfashion2:{source_split}:pair:{pair_id}' if pair_id else None
    rows = []
    for key, item in sorted(data.items()):
        if not key.startswith('item'):
            continue
        if not isinstance(item, dict):
            raise ValueError('Invalid clothing item')
        if item.get('category_id') != 8:
            continue
        box = item.get('bounding_box', [])
        if (len(box) != 4 or not all(type(v) in {int, float} and math.isfinite(v) for v in box)
                or box[0] < 0 or box[1] < 0 or box[0] >= box[2] or box[1] >= box[3]):
            raise ValueError('Invalid trousers bounding box')
        style = item.get('style')
        if type(style) is not int or style < 0:
            raise ValueError('Invalid style ID')
        rows.append({
            'id': f'deepfashion2-{source_split}-{image_id}-{key}',
            'image_id': image_id, 'image_file': image_id + '.jpg',
            'source_dataset_split': source_split, 'source_domain': data['source'],
            'pair_id': pair_id, 'style_id': style, 'product_group_candidate': group,
            'group_status': 'source_pair_id_unverified' if group else 'missing',
            'bbox_xyxy_pixels': box, 'has_segmentation': bool(item.get('segmentation')),
            'source_viewpoint': item.get('viewpoint'),
            'source_occlusion': item.get('occlusion'), 'source_zoom_in': item.get('zoom_in'),
            'denim_status': 'unreviewed', 'rights_status': 'usage_scope_review_pending',
            'research_split': None,
        })
    return rows


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--annotations', type=Path, required=True)
    parser.add_argument('--source-split', choices=['train', 'validation'], required=True)
    parser.add_argument('--output', type=Path, required=True, help='New output directory; never overwritten')
    args = parser.parse_args()
    if not (Path('/kaggle/working').is_dir() or Path('/content').is_dir()):
        parser.error('Run dataset processing on remote Kaggle/Colab, not the laptop.')
    if not args.annotations.is_dir():
        parser.error('Annotations directory does not exist')
    files = sorted(args.annotations.glob('*.json'))
    if not files:
        parser.error('No annotation JSON files')
    # The completion report is written only after every source file passes validation.
    args.output.mkdir(parents=True, exist_ok=False)
    counts = Counter()
    groups = set()
    with ((args.output / 'candidates.jsonl').open('x', encoding='utf-8') as manifest,
          (args.output / 'source_checksums.jsonl').open('x', encoding='utf-8') as checksums):
        for path in files:
            raw = path.read_bytes()
            data = json.loads(raw, object_pairs_hook=unique_object)
            rows = trousers_candidates(data, path.stem, args.source_split)
            checksums.write(json.dumps({'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest()}) + '\n')
            for row in rows:
                manifest.write(json.dumps(row) + '\n')
                counts['trousers_instances'] += 1
                counts['missing_group_instances'] += row['product_group_candidate'] is None
                if row['product_group_candidate']:
                    groups.add(row['product_group_candidate'])
            counts['images_with_trousers'] += bool(rows)
    summary = {'complete': True, 'source_files': len(files), **counts,
               'source_pair_groups': len(groups), 'source_dataset_split': args.source_split,
               'images_read': 0, 'confirmed_denim_instances': 0, 'research_splits_assigned': False,
               'note': 'Within one original partition only. Pair/style labels are not appearance-relevance labels.'}
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
