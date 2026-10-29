"""Build a private, rank-blind single-rater calibration sheet; never assign grades."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import random
import re


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


def packet(queries, candidates, packet_id='denim-atlas-calibration-round1-v1', pools=None,
           separate_axes=False):
    if not queries or len(candidates) < 2:
        raise ValueError('Queries and at least two candidates required')
    validate_images(queries + candidates)
    candidate_indices = {row['id']:i for i,row in enumerate(candidates)}
    if pools is not None:
        if not isinstance(pools,dict) or set(pools) != {q['id'] for q in queries}:
            raise ValueError('Pools must cover exactly the query IDs')
        for values in pools.values():
            if (not isinstance(values,list) or len(values) < 2
                    or any(not isinstance(c,str) or c not in candidate_indices for c in values)
                    or len(set(values)) != len(values)):
                raise ValueError('Each pool needs at least two distinct known candidate IDs')
    if not isinstance(packet_id,str) or not re.fullmatch(r'[a-z0-9-]{1,80}',packet_id):
        raise ValueError('Expected a safe unique packet ID')
    seed = packet_id
    rng = random.Random(seed)
    trials, groups = [], []
    for qi, query in enumerate(queries):
        order = (list(range(len(candidates))) if pools is None
                 else [candidate_indices[c] for c in pools[query['id']]])
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
    if separate_axes:
        result.update(schema_version=2, comparison_axes=['silhouette', 'surface'])
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
    parser.add_argument('--packet-id', default='denim-atlas-calibration-round1-v1')
    parser.add_argument('--pools', type=Path, help='JSON mapping query IDs to their candidate IDs')
    parser.add_argument('--legacy-overall', action='store_true',
                        help='Reproduce historical joint-grade packets; new packets separate the two axes')
    args = parser.parse_args()
    data = packet(json.loads(args.queries.read_text(encoding='utf-8'))['assets'],
                  json.loads(args.gallery.read_text(encoding='utf-8'))['assets'], args.packet_id,
                  json.loads(args.pools.read_text(encoding='utf-8')) if args.pools else None,
                  separate_axes=not args.legacy_overall)
    args.output.mkdir(exist_ok=False)
    (args.output/'packet.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    (args.output/'judge.html').write_text(build_html(data), encoding='utf-8')
    summary = {key:data[key] for key in ['packet_id','packet_sha256','purpose','research_split','independent_product_groups_verified']}
    summary.update(queries=len(data['queries']), candidates=len(data['candidates']),
                   unique_pairs=sum(map(len,data['candidate_pools'])),
                   repeated_pairs=len(data['queries']), total_trials=len(data['trials']), judgments=0)
    summary['comparison_axes'] = data.get('comparison_axes', ['overall'])
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
