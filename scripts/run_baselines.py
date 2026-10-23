"""Score identical judged pools with frozen cosine B0 and a simple RGB control B1."""

import argparse
import hashlib
import json
import math
from pathlib import Path

try:
    from .evaluate import evaluate, unique_object, validate_benchmark
except ImportError:
    from evaluate import evaluate, unique_object, validate_benchmark


def vector(value, length=None):
    if (not isinstance(value, list) or not value or
            any(type(v) not in {int, float} or not math.isfinite(v) for v in value)
            or (length is not None and len(value) != length)):
        raise ValueError('Expected a finite numeric vector of consistent dimension')
    return value


def rank_baselines(benchmark, features, color_weight):
    if (type(color_weight) not in {int, float} or not math.isfinite(color_weight)
            or not 0 <= color_weight <= 1):
        raise ValueError('color_weight must be finite in [0, 1]')
    # Validate pools and groups before scoring, without using grades to choose ranks.
    _, judgments = validate_benchmark(benchmark)
    original = {query_id: list(grades) for query_id, grades in judgments.items()}
    if (not isinstance(features, dict) or type(features.get('schema_version')) is not int
            or features['schema_version'] != 1):
        raise ValueError('Expected feature schema_version 1')
    observations = features.get('assets')
    if not isinstance(observations, dict):
        raise ValueError('Expected feature assets keyed by ID')
    required = set(original)
    required.update(value for pool in original.values() for value in pool)
    normalized, colors = {}, {}
    dimension = None
    for asset_id in sorted(required):
        row = observations.get(asset_id)
        if not isinstance(row, dict):
            raise ValueError('Missing features: ' + asset_id)
        embedding = vector(row.get('embedding'), dimension)
        dimension = len(embedding)
        norm = math.hypot(*embedding)
        if not math.isfinite(norm) or norm == 0:
            raise ValueError('Embedding must have finite nonzero norm')
        normalized[asset_id] = [v / norm for v in embedding]
        rgb = vector(row.get('mean_rgb'), 3)
        if any(v < 0 or v > 1 for v in rgb):
            raise ValueError('mean_rgb must be in [0, 1]')
        colors[asset_id] = rgb
    b0, b1 = {}, {}
    for query_id, candidates in original.items():
        scores = {}
        for candidate_id in candidates:
            cosine = math.fsum(a * b for a, b in zip(
                normalized[query_id], normalized[candidate_id]))
            visual = (max(-1, min(1, cosine)) + 1) / 2
            distance = math.dist(colors[query_id], colors[candidate_id]) / math.sqrt(3)
            scores[candidate_id] = (visual, (1 - color_weight) * visual + color_weight * (1 - distance))
        b0[query_id] = sorted(candidates, key=lambda key: (-scores[key][0], key))
        b1[query_id] = sorted(candidates, key=lambda key: (-scores[key][1], key))
    return b0, b1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', type=Path, required=True)
    parser.add_argument('--features', type=Path, required=True)
    parser.add_argument('--color-weight', type=float, required=True,
                        help='Predeclare or select on validation only; never optimize on test')
    parser.add_argument('--output', type=Path, required=True, help='New run directory')
    args = parser.parse_args()
    try:
        benchmark_raw, features_raw = args.benchmark.read_bytes(), args.features.read_bytes()
        benchmark = json.loads(benchmark_raw, object_pairs_hook=unique_object)
        features = json.loads(features_raw, object_pairs_hook=unique_object)
        rankings = rank_baselines(benchmark, features, args.color_weight)
        reports = [evaluate(benchmark, ranking) for ranking in rankings]
        args.output.mkdir(parents=True, exist_ok=False)
        for name, ranking, report in zip(('b0', 'b1'), rankings, reports):
            ranking_text = json.dumps(ranking, indent=2, allow_nan=False) + '\n'
            ranking_raw = ranking_text.encode('utf-8')
            (args.output / (name + '-rankings.json')).write_bytes(ranking_raw)
            report.update(benchmark_sha256=hashlib.sha256(benchmark_raw).hexdigest(),
                          rankings_sha256=hashlib.sha256(ranking_raw).hexdigest())
            (args.output / (name + '-report.json')).write_text(
                json.dumps(report, indent=2, allow_nan=False) + '\n', encoding='utf-8')
        summary = {'complete': True, 'color_weight': args.color_weight,
                   'benchmark_sha256': hashlib.sha256(benchmark_raw).hexdigest(),
                   'features_sha256': hashlib.sha256(features_raw).hexdigest(),
                   'feature_provenance': features.get('provenance'),
                   'b0': 'cosine mapped to [0,1]',
                   'b1': '(1-w)*B0 + w*(1 - Euclidean(mean_RGB)/sqrt(3))',
                   'note': 'No uncertainty estimate; fixed pools only. Weight selection must precede test evaluation.'}
        (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, f'Baseline run failed: {error}\n')
    print('Completed baseline reports:', args.output)


if __name__ == '__main__':
    main()
