"""Build a private, rank-blind single-rater calibration sheet; never assign grades."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import random


def validate_images(rows):
    seen = set()
    for row in rows:
        if not row.get('id') or row['id'] in seen:
            raise ValueError('Missing or duplicate image ID')
        seen.add(row['id'])
        prefix, encoded = row['data_uri'].split(',', 1)
        if prefix != 'data:image/png;base64':
            raise ValueError('Expected embedded PNG')
        raw = base64.b64decode(encoded, validate=True)
        if not raw.startswith(b'\x89PNG\r\n\x1a\n') or hashlib.sha256(raw).hexdigest() != row['crop_sha256']:
            raise ValueError('Invalid crop bytes or hash')


def packet(queries, candidates):
    if not queries or len(candidates) < 2:
        raise ValueError('Queries and at least two candidates required')
    validate_images(queries + candidates)
    seed = 'denim-atlas-calibration-round1-v1'
    rng = random.Random(seed)
    trials, groups = [], []
    for qi, query in enumerate(queries):
        order = list(range(len(candidates)))
        rng.shuffle(order)
        pairs = [{'query':qi, 'candidate':ci, 'repeat':False} for ci in order]
        # One separated repeat per query measures within-rater repeat agreement only.
        repeated = dict(pairs[0], repeat=True)
        pairs.insert(max(2, len(pairs)//2), repeated)
        groups.append([candidates[ci]['id'] for ci in order])
        trials.extend(pairs)
    for i, trial in enumerate(trials):
        trial['trial_id'] = f't{i+1:04d}'
    result = {'schema_version':1, 'packet_id':seed, 'purpose':'calibration_only',
              'rater_id':'jemin', 'queries':queries, 'candidates':candidates,
              'trials':trials, 'candidate_pools':groups,
              'research_split':None, 'independent_product_groups_verified':False}
    raw = json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode()
    result['packet_sha256'] = hashlib.sha256(raw).hexdigest()
    return result


def build_html(data):
    template = Path(__file__).with_name('judgment_template.html').read_text(encoding='utf-8')
    encoded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    return template.replace('__PACKET_DATA__', encoded)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queries', type=Path, required=True)
    parser.add_argument('--gallery', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = packet(json.loads(args.queries.read_text(encoding='utf-8'))['assets'],
                  json.loads(args.gallery.read_text(encoding='utf-8'))['assets'])
    args.output.mkdir(exist_ok=False)
    (args.output/'packet.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    (args.output/'judge.html').write_text(build_html(data), encoding='utf-8')
    summary = {key:data[key] for key in ['packet_id','packet_sha256','purpose','research_split','independent_product_groups_verified']}
    summary.update(queries=len(data['queries']), candidates=len(data['candidates']),
                   unique_pairs=len(data['queries'])*len(data['candidates']),
                   repeated_pairs=len(data['queries']), total_trials=len(data['trials']), judgments=0)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
