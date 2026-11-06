"""Approved fixed-pool human comparison. Print aggregates; never write labels/reports."""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import zipfile

import numpy as np

from scripts.evaluate import ndcg_at_5, unique_object
from scripts.extract_features import frozen_profile
from scripts.import_judgments import import_ratings
from scripts.run_baselines import vector


def interval(values, denominators=None):
    """Cluster resampling: each row is one anchor, including all its preferences."""
    values = np.asarray(values, dtype=float)
    if not len(values):
        return None
    den = np.ones(len(values)) if denominators is None else np.asarray(denominators, dtype=float)
    if den.sum() == 0:
        return None
    samples = np.random.default_rng(51105).integers(0, len(values), (10000, len(values)))
    ds = den[samples].sum(axis=1)
    bs = values[samples].sum(axis=1)[ds > 0] / ds[ds > 0]
    return [float(values.sum()/den.sum()), *np.quantile(bs, [.025, .975]).tolist()]


def pool_scores(grades, scores):
    if len(grades) != 3 or len(scores) != 3:
        raise ValueError('Frozen endpoint requires exactly three candidates')
    orders = list(itertools.permutations(range(3)))
    random = [ndcg_at_5([grades[i] for i in order]) for order in orders]
    ranked = [random[j] for j, order in enumerate(orders)
              if all(scores[a] >= scores[b] for a, b in zip(order, order[1:]))]
    ndcg = None if random[0] is None else math.fsum(ranked)/len(ranked)
    baseline = None if random[0] is None else math.fsum(random)/6
    correct, count = 0., 0
    for a, b in itertools.combinations(range(3), 2):
        if grades[a] == grades[b]:
            continue
        count += 1
        correct += .5 if scores[a] == scores[b] else float((scores[a] > scores[b]) == (grades[a] > grades[b]))
    return ndcg, baseline, correct, count


def validate_features(packet, features, manifest_sha):
    profile = frozen_profile(features['provenance'])
    if features['provenance']['manifest_sha256'] != manifest_sha:
        raise ValueError('Feature manifest provenance mismatch')
    if features['provenance'].get('input_policy') != 'EXIF RGB -> white aspect-preserving 224 square -> official model preprocessing':
        raise ValueError('Unexpected preprocessing')
    expected = {r['id']:r for r in packet['queries']+packet['candidates']}
    if set(features['assets']) != set(expected):
        raise ValueError('Feature asset set mismatch')
    normalized = {}
    for identity, asset in expected.items():
        row = features['assets'][identity]
        if row['crop_sha256'] != asset['crop_sha256']:
            raise ValueError('Crop hash mismatch')
        v = vector(row['embedding'], profile['dimension'])
        norm = math.hypot(*v)
        if not .999 < norm < 1.001:
            raise ValueError('Expected unit feature')
        normalized[identity] = np.asarray(v)/norm
    return normalized


def summarize(rows):
    eligible = [r for r in rows if r['ndcg'] is not None]
    return {'complete_anchors':len(rows), 'ndcg_anchors':len(eligible),
            'strict_preferences':sum(r['count'] for r in rows),
            'human_tied_preferences':3*len(rows)-sum(r['count'] for r in rows),
            'concordance':interval([r['correct'] for r in rows], [r['count'] for r in rows]),
            'ndcg':interval([r['ndcg'] for r in eligible]),
            'random_ndcg':interval([r['random'] for r in eligible]),
            'ndcg_minus_random':interval([r['ndcg']-r['random'] for r in eligible])}


def compare(packet, ratings, features, provenance, manifest_sha):
    imported = import_ratings(packet, ratings)
    if imported.get('complete_trials') != len(packet['trials']):
        raise ValueError('Confirm all trials before evaluation')
    vectors = {name:validate_features(packet, f, manifest_sha) for name, f in features.items()}
    if len({q['source_group'] for q in packet['queries']}) != len(packet['queries']):
        raise ValueError('One anchor per capture group required')
    result = {}
    for axis, labels in imported['axis_results'].items():
        grades = {(r['query_id'], r['candidate_id']):r['grade'] for r in labels['judged_unique_pairs']}
        repeats = labels['repeat_checks']
        exact = sum(r['exact_agreement'] and 'U' not in r['grades'] for r in repeats)
        blocked = {r['query_id'] for r in labels['conflicts_requiring_review']}
        rows = {name:[] for name in features}
        for q, candidates in zip(packet['queries'], packet['candidate_pools']):
            identity = q['id']
            if identity in blocked or any((identity, c) not in grades for c in candidates):
                continue
            meta = provenance[identity]
            resolution = 'high' if min(int(meta['source_width']), int(meta['source_height'])) >= 720 else 'low'
            for name, embedding in vectors.items():
                scores = [float(embedding[identity] @ embedding[c]) for c in candidates]
                ndcg, random, correct, count = pool_scores([grades[identity,c] for c in candidates], scores)
                rows[name].append(dict(ndcg=ndcg, random=random, correct=correct, count=count,
                                       resolution=resolution, view=meta['view']))
        models = {}
        for name, all_rows in rows.items():
            slices = {s:[r for r in all_rows if r['resolution']==s] for s in ('high','low')}
            slices.update({s:[r for r in all_rows if r['view']==s]
                           for s in ('catalog_wearing','natural_wearing','isolated_product')})
            models[name] = {'all':summarize(all_rows),
                            'slices':{s:summarize(v) for s,v in slices.items()}}
            # Same anchor draws for every model permit paired encoder differences.
        differences = {}
        for a,b in itertools.combinations(rows,2):
            pairs = [(x,y) for x,y in zip(rows[a],rows[b]) if x['ndcg'] is not None]
            differences[a+' minus '+b] = interval([x['ndcg']-y['ndcg'] for x,y in pairs])
        result[axis] = {'repeat_exact_nonunknown':exact,'repeat_total':len(repeats),
                        'unknown_trials':labels['uncertain_trials'],
                        'conflicting_pairs':len(labels['conflicts_requiring_review']),
                        'excluded_anchors':len(packet['queries'])-len(next(iter(rows.values()))),
                        'common_gate':exact>=7 and all(v['all']['ndcg_anchors']>=20 for v in models.values()),
                        'models':models,'paired_ndcg_differences':differences}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--ratings', type=Path, required=True)
    parser.add_argument('--features', type=Path, required=True)
    parser.add_argument('--input-archive', type=Path, required=True)
    args = parser.parse_args()
    read = lambda p:json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    packet = read(args.bundle/'packet.json')
    features = {name:read(args.features/(name+'-features.json')) for name in ('fashion-siglip','clip','dinov2')}
    with (args.bundle/'source_crops.csv').open(encoding='utf-8', newline='') as f:
        provenance = {r['id']:r for r in csv.DictReader(f)}
    # Uploaded manifest omits embedded PNG data URIs; pin its exact bytes, not the UI copy.
    with zipfile.ZipFile(args.input_archive) as archive:
        raw = archive.read('crops.json')
        manifest = json.loads(raw, object_pairs_hook=unique_object)
        if {r['id']:r['crop_sha256'] for r in manifest['assets']} != {
                r['id']:r['crop_sha256'] for r in packet['queries']+packet['candidates']}:
            raise ValueError('Uploaded manifest and packet crop sets differ')
        for row in manifest['assets']:
            if hashlib.sha256(archive.read(row['crop_file'])).hexdigest() != row['crop_sha256']:
                raise ValueError('Uploaded crop bytes changed')
    result = compare(packet, read(args.ratings), features, provenance, hashlib.sha256(raw).hexdigest())
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
