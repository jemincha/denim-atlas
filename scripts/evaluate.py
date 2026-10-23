"""Validate reviewed splits and evaluate a fully judged fixed candidate pool."""

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path


def identifier(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('IDs and groups must be nonempty strings')
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def validate_assets(rows):
    """Require reviewed groups; never promote importer candidate groups automatically."""
    if not isinstance(rows, list) or not rows:
        raise ValueError('assets must be a nonempty list')
    assets, owners = {}, {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Each asset must be an object')
        asset_id = identifier(row.get('id'))
        if asset_id in assets:
            raise ValueError('Duplicate asset: ' + asset_id)
        split = row.get('research_split')
        if split not in {'train', 'validation', 'test'}:
            raise ValueError('Every asset needs a research_split')
        for field in ('product_group', 'duplicate_group', 'image_group'):
            group = identifier(row.get(field))
            key = (field, group)
            if key in owners and owners[key] != split:
                raise ValueError(f'Split leakage: {field}={group}')
            owners[key] = split
        assets[asset_id] = row
    return assets


def ndcg_at_5(grades):
    """Grades must be the complete pool, ordered by the method being scored."""
    if not grades or any(type(g) is not int or g not in range(4) for g in grades):
        raise ValueError('Complete integer relevance grades 0..3 required')

    def dcg(values):
        return math.fsum((2 ** grade - 1) / math.log2(rank + 2)
                         for rank, grade in enumerate(values[:5]))

    ideal = dcg(sorted(grades, reverse=True))
    return dcg(grades) / ideal if ideal else None


def evaluate(benchmark, rankings):
    if (not isinstance(benchmark, dict) or type(benchmark.get('schema_version')) is not int
            or benchmark['schema_version'] != 1):
        raise ValueError('Expected benchmark schema_version 1')
    assets = validate_assets(benchmark.get('assets'))
    pools = benchmark.get('pools')
    if not isinstance(pools, list) or not pools:
        raise ValueError('pools must be a nonempty list')
    if not isinstance(rankings, dict):
        raise ValueError('Rankings must map query IDs to full candidate permutations')
    judgments = {}
    for pool in pools:
        if not isinstance(pool, dict):
            raise ValueError('Each pool must be an object')
        query_id = identifier(pool.get('query_id'))
        if query_id in judgments or query_id not in assets:
            raise ValueError('Duplicate or unknown query: ' + query_id)
        query = assets[query_id]
        if query['research_split'] == 'train':
            raise ValueError('Evaluation queries must be validation or test')
        candidates = pool.get('candidates')
        if not isinstance(candidates, list) or not candidates:
            raise ValueError('Each query needs a nonempty judged pool')
        grades = {}
        for candidate in candidates:
            if not isinstance(candidate, dict):
                raise ValueError('Each candidate must be an object')
            candidate_id = identifier(candidate.get('id'))
            grade = candidate.get('grade')
            if candidate_id in grades or candidate_id not in assets:
                raise ValueError('Duplicate or unknown candidate: ' + candidate_id)
            if type(grade) is not int or grade not in range(4):
                raise ValueError('Unjudged/uncertain is not grade 0; require integer 0..3')
            asset = assets[candidate_id]
            if candidate_id == query_id or any(asset[field] == query[field] for field in
                    ('product_group', 'duplicate_group', 'image_group')):
                raise ValueError('Candidate must be a different product and image: ' + candidate_id)
            if asset['research_split'] != query['research_split']:
                raise ValueError('Query and candidate must belong to the same research split')
            grades[candidate_id] = grade
        judgments[query_id] = grades
    if set(rankings) != set(judgments):
        raise ValueError('Ranking query set must exactly match the benchmark')
    results = []
    for query_id, grades in judgments.items():
        order = rankings[query_id]
        if not isinstance(order, list) or any(not isinstance(v, str) for v in order):
            raise ValueError('Each ranking must be a list of candidate IDs')
        if len(order) != len(grades) or set(order) != set(grades):
            raise ValueError('Ranking must contain every pool candidate exactly once: ' + query_id)
        results.append({'query_id': query_id, 'research_split': assets[query_id]['research_split'],
                        'candidate_count': len(grades),
                        'ndcg_at_5': ndcg_at_5([grades[v] for v in order])})
    by_split = {}
    for split in sorted({row['research_split'] for row in results}):
        subset = [row for row in results if row['research_split'] == split]
        scores = [row['ndcg_at_5'] for row in subset if row['ndcg_at_5'] is not None]
        by_split[split] = {'query_count': len(subset), 'scored_queries': len(scores),
                           'zero_positive_queries': len(subset) - len(scores),
                           'mean_ndcg_at_5': math.fsum(scores) / len(scores) if scores else None}
    return {'metric': 'ndcg@5', 'gain': '2^grade - 1', 'by_split': by_split,
            'per_query': results, 'asset_counts': dict(Counter(
                row['research_split'] for row in assets.values())),
            'scope': 'Fully judged fixed pools; no full-catalog or independence claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', type=Path, required=True)
    parser.add_argument('--rankings', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New report; never overwritten')
    args = parser.parse_args()
    try:
        benchmark_raw = args.benchmark.read_bytes()
        rankings_raw = args.rankings.read_bytes()
        report = evaluate(json.loads(benchmark_raw, object_pairs_hook=unique_object),
                          json.loads(rankings_raw, object_pairs_hook=unique_object))
        report['benchmark_sha256'] = hashlib.sha256(benchmark_raw).hexdigest()
        report['rankings_sha256'] = hashlib.sha256(rankings_raw).hexdigest()
        serialized = json.dumps(report, indent=2, allow_nan=False) + '\n'
        with args.output.open('x', encoding='utf-8') as output:
            output.write(serialized)
    except (OSError, ValueError, TypeError) as error:
        parser.exit(2, f'Evaluation failed: {error}\n')
    print(serialized, end='')


if __name__ == '__main__':
    main()
