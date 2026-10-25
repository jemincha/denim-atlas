"""Compare frozen rankings with private calibration judgments, never held-out claims."""

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .evaluate import ndcg_at_5, unique_object
    from .extract_features import REVISION, WEIGHT_SHA256
    from .import_judgments import import_ratings
    from .run_baselines import rank_pools, vector
except ImportError:
    from evaluate import ndcg_at_5, unique_object
    from extract_features import REVISION, WEIGHT_SHA256
    from import_judgments import import_ratings
    from run_baselines import rank_pools, vector


def analyze(packet, ratings, features):
    imported = import_ratings(packet, ratings)
    provenance = features.get('provenance', {})
    if (provenance.get('revision') != REVISION
            or provenance.get('weights_sha256') != WEIGHT_SHA256
            or provenance.get('training_run') is not False):
        raise ValueError('Expected pinned frozen Marqo features')
    for row in packet['queries'] + packet['candidates']:
        feature = features.get('assets',{}).get(row['id'],{})
        if feature.get('crop_sha256') != row['crop_sha256']:
            raise ValueError('Feature crop checksum mismatch: '+row['id'])
        vector(feature.get('embedding'), 768)
    pools = {q['id']:packet['candidate_pools'][i] for i,q in enumerate(packet['queries'])}
    # Fixed w=0.5 was used before these labels existed; no search against rater scores.
    rankings = rank_pools(pools, features, 0.5)
    grades = {(r['query_id'],r['candidate_id']):r['grade']
              for r in imported['judged_unique_pairs']}
    results = []
    for name, ranking in zip(('b0','b1'),rankings):
        for query, candidates in ranking.items():
            ordered = [grades.get((query,c)) for c in candidates]
            complete = all(g is not None for g in ordered)
            results.append({'baseline':name, 'query_id':query,
                'fully_judged_pool':complete, 'candidate_count':len(candidates),
                'calibration_ndcg_at_5':ndcg_at_5(ordered) if complete else None,
                'top5':[{'candidate_id':c,'grade':grades.get((query,c))} for c in candidates[:5]],
                'ranking':candidates})
    return {'schema_version':1, 'purpose':'calibration_only', 'color_weight':0.5,
            'packet_sha256':packet['packet_sha256'], 'usable_pairs':len(grades),
            'held_out_evaluation':False, 'product_independence_verified':False,
            'training_run':False, 'feature_provenance':provenance, 'results':results,
            'note':'Descriptive single-rater pilot only. Incomplete pools get no metric; unknown is not zero.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('packet','ratings','features','output'):
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    raw = {key:getattr(args,key).read_bytes() for key in ('packet','ratings','features')}
    result = analyze(*(json.loads(raw[key], object_pairs_hook=unique_object)
                       for key in ('packet','ratings','features')))
    result['input_sha256'] = {key:hashlib.sha256(value).hexdigest() for key,value in raw.items()}
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2,allow_nan=False)
    print('Calibration comparison written:',args.output)
