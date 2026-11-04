"""Validate machine regional preferences and export axis-specific development inputs.

These are teacher constraints, never independent human relevance grades.
"""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

AXES = ('silhouette', 'surface')


def checksum(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def validate_packet(packet, assets=None):
    if packet.get('schema_version') != 1 or packet.get('purpose') != 'machine_axis_development':
        raise ValueError('Expected machine-only development packet')
    if packet.get('packet_sha256') != checksum({k: v for k, v in packet.items() if k != 'packet_sha256'}):
        raise ValueError('Packet checksum mismatch')
    observations, groups, pixels, files = {}, {}, {}, {}
    reserved = set(packet['reserved_ids'])
    for row in packet['observations']:
        key, split = row['id'], row['split']
        if key in observations or key in reserved or split not in {'train', 'development'}:
            raise ValueError('Duplicate/reserved observation or invalid split')
        if set(row['regions']) != {'garment', 'hip_thigh'}:
            raise ValueError('Missing corresponding regions')
        if row['source_sha256'] != row['source']['sha256']:
            raise ValueError('Source provenance mismatch')
        for registry, value in ((groups, row['source_group']), (pixels, row['pixel_sha256'])):
            if value in registry and registry[value] != split:
                raise ValueError('Cross-split source group or pixel duplicate')
            registry[value] = split
        if row['source_sha256'] in files and files[row['source_sha256']] != split:
            raise ValueError('Cross-split file duplicate')
        files[row['source_sha256']] = split
        for view in [row['source']] + list(row['regions'].values()):
            path = Path(view['file'])
            if path.is_absolute() or '..' in path.parts or '\\' in view['file'] or ':' in view['file']:
                raise ValueError('Unsafe relative asset path')
            if assets is not None:
                full = (assets / path).resolve()
                if not full.is_relative_to(assets.resolve()):
                    raise ValueError('Asset escapes packet directory')
                if hashlib.sha256(full.read_bytes()).hexdigest() != view['sha256']:
                    raise ValueError('Asset checksum mismatch')
        width, height = row['source']['size']
        for region in row['regions'].values():
            box = region['box_xyxy']
            if (len(box) != 4 or any(type(v) is not int for v in box)
                    or not 0 <= box[0] < box[2] <= width
                    or not 0 <= box[1] < box[3] <= height
                    or region['size'] != [box[2] - box[0], box[3] - box[1]]):
                raise ValueError('Invalid regional geometry')
        if assets is not None:
            with Image.open(assets / row['source']['file']) as source:
                image = ImageOps.exif_transpose(source).convert('RGB')
                if (list(image.size) != row['source']['size']
                        or hashlib.sha256(image.tobytes()).hexdigest() != row['pixel_sha256']):
                    raise ValueError('Decoded source mismatch')
                for region in row['regions'].values():
                    with Image.open(assets / region['file']) as crop:
                        expected = image.crop(region['box_xyxy'])
                        if crop.size != expected.size or crop.convert('RGB').tobytes() != expected.tobytes():
                            raise ValueError('Region is not the recorded source crop')
        observations[key] = row
    cases = {}
    for case in packet['cases']:
        if case['id'] in cases or set(case['candidates']) != {'A', 'B'}:
            raise ValueError('Duplicate case or invalid candidates')
        ids = [case['reference'], *case['candidates'].values()]
        if any(key not in observations for key in ids):
            raise ValueError('Unknown observation')
        rows = [observations[key] for key in ids]
        if len(set(ids)) != 3 or len({row['source_group'] for row in rows}) != 3:
            raise ValueError('Case must cross distinct known source groups')
        if any(row['split'] != case['split'] for row in rows):
            raise ValueError('Case crosses a split')
        cases[case['id']] = case
    return observations, cases


def import_preferences(packet, export, assets=None):
    observations, cases = validate_packet(packet, assets)
    if (export.get('packet_sha256') != packet['packet_sha256']
            or export.get('schema_version') != 1 or export.get('label_source') != 'machine_visual'):
        raise ValueError('Export provenance mismatch; human grades are a separate schema')
    teacher = export.get('teacher', {})
    if not teacher.get('runtime') or not teacher.get('rubric_version') or 'exact_checkpoint' not in teacher:
        raise ValueError('Teacher provenance required, including unknown checkpoint')
    if (teacher['rubric_version'] != packet['rubric_version']
            or teacher.get('rubric_sha256') != packet['rubric_sha256']):
        raise ValueError('Teacher rubric provenance mismatch')
    if teacher['exact_checkpoint'] is None and not teacher.get('checkpoint_limit'):
        raise ValueError('Unexposed checkpoint must be explicitly disclosed')
    constraints, decisions, seen = [], [], set()
    for row in export['ratings']:
        pair = (row['case_id'], row['axis'])
        if pair in seen or row['case_id'] not in cases or row['axis'] not in AXES:
            raise ValueError('Unknown or duplicate case/axis')
        seen.add(pair)
        choice, confidence = row['choice'], row['confidence']
        if choice not in {'A', 'B', 'tie', 'neither', 'unknown'} or confidence not in {'low', 'medium', 'high'}:
            raise ValueError('Invalid preference or ordinal confidence')
        if not isinstance(row.get('reason'), str) or not row['reason'].strip():
            raise ValueError('Visible-evidence reason required')
        useful = row.get('useful_match')
        expected = None if choice == 'unknown' else choice != 'neither'
        if useful is not expected:
            raise ValueError('Acceptance must be explicit; unknown is not negative')
        case = cases[row['case_id']]
        decisions.append(dict(row, split=case['split']))
        if confidence == 'low' or choice in {'neither', 'unknown'}:
            continue
        # A tie constrains two distances, not image identity or two positive grades.
        constraints.append({'case_id': case['id'], 'axis': row['axis'], 'split': case['split'],
                            'reference': case['reference'], 'candidate_a': case['candidates']['A'],
                            'candidate_b': case['candidates']['B'], 'target': choice,
                            'label_source': 'machine_visual', 'confidence': confidence})
    if len(seen) != len(cases) * len(AXES):
        raise ValueError('Incomplete axis export')
    counts = {split: {axis: len({c['reference'] for c in constraints
                                if c['split'] == split and c['axis'] == axis and c['target'] != 'tie'})
                     for axis in AXES}
              for split in ('train', 'development')}
    # shortcut: this is an engineering pilot gate, not statistical adequacy for quality claims.
    ready = all(counts['train'][axis] >= 3 and counts['development'][axis] >= 2 for axis in AXES)
    return {'schema_version': 1, 'purpose': 'teacher_distillation_pilot',
            'packet_sha256': packet['packet_sha256'], 'export_sha256': checksum(export),
            'teacher': teacher, 'observations': list(observations.values()), 'decisions': decisions,
            'constraints': constraints, 'strict_counts': counts, 'ready_for_pilot': ready,
            'independent_quality_evidence': False,
            'limits': 'Machine supervision; development agreement measures teacher reproduction, '
                      'not human acceptability or superiority to a strong general model.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--ratings', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = import_preferences(json.loads(args.packet.read_text(encoding='utf-8')),
                                json.loads(args.ratings.read_text(encoding='utf-8')), args.packet.parent)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ('strict_counts', 'ready_for_pilot',
                                                  'independent_quality_evidence')}))
