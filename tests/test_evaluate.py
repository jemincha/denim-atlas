import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.evaluate import evaluate, ndcg_at_5, unique_object, validate_assets


def fixture():
    assets = [{'id': name, 'research_split': 'test', 'product_group': 'product-' + name,
               'duplicate_group': 'duplicate-' + name, 'image_group': 'image-' + name}
              for name in ['q', 'a', 'b', 'c']]
    return {'schema_version': 1, 'assets': assets,
            'pools': [{'query_id': 'q', 'candidates': [
                {'id': 'a', 'grade': 3}, {'id': 'b', 'grade': 1}, {'id': 'c', 'grade': 0}]}]}


class EvaluationTests(unittest.TestCase):
    def test_metric_against_hand_calculation(self):
        expected = (1 + 7 / math.log2(3)) / (7 + 1 / math.log2(3))
        self.assertAlmostEqual(ndcg_at_5([1, 3, 0]), expected)
        self.assertEqual(ndcg_at_5([3, 1, 0]), 1)
        self.assertIsNone(ndcg_at_5([0, 0]))
        self.assertEqual(ndcg_at_5([0, 0, 0, 0, 0, 3]), 0)
        for bad in [[], [None], [True], [1.0], [-1], [4]]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                ndcg_at_5(bad)

    def test_zero_positive_queries_reported_separately(self):
        benchmark = fixture()
        benchmark['pools'].append({'query_id': 'b', 'candidates': [{'id': 'a', 'grade': 0}]})
        report = evaluate(benchmark, {'q': ['a', 'b', 'c'], 'b': ['a']})
        self.assertEqual(report['by_split']['test'], {
            'query_count': 2, 'scored_queries': 1, 'zero_positive_queries': 1, 'mean_ndcg_at_5': 1})
        self.assertIsNone(report['per_query'][1]['ndcg_at_5'])

    def test_group_leakage_even_for_assets_outside_pools(self):
        for field in ['product_group', 'duplicate_group', 'image_group']:
            benchmark = fixture()
            extra = copy.deepcopy(benchmark['assets'][1])
            extra.update(id='extra', research_split='train')
            for other in ['product_group', 'duplicate_group', 'image_group']:
                if other != field:
                    extra[other] = 'new-' + other
            benchmark['assets'].append(extra)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Split leakage'):
                evaluate(benchmark, {'q': ['a', 'b', 'c']})

    def test_validation_and_test_not_averaged_and_all_zero_mean_is_null(self):
        benchmark = fixture()
        validation = fixture()
        for asset in validation['assets']:
            for field in ['id', 'product_group', 'duplicate_group', 'image_group']:
                asset[field] = 'v-' + asset[field]
            asset['research_split'] = 'validation'
        benchmark['assets'].extend(validation['assets'])
        benchmark['pools'].append({'query_id': 'v-q', 'candidates': [{'id': 'v-a', 'grade': 0}]})
        report = evaluate(benchmark, {'q': ['a', 'b', 'c'], 'v-q': ['v-a']})
        self.assertEqual(report['by_split']['test']['mean_ndcg_at_5'], 1)
        self.assertIsNone(report['by_split']['validation']['mean_ndcg_at_5'])
        self.assertEqual(report['by_split']['validation']['zero_positive_queries'], 1)

    def test_self_unknown_and_duplicate_queries_rejected(self):
        for query_id in ['missing', 'a']:
            benchmark = fixture()
            benchmark['pools'][0]['query_id'] = query_id
            with self.subTest(query_id=query_id), self.assertRaises(ValueError):
                evaluate(benchmark, {query_id: ['a', 'b', 'c']})
        benchmark = fixture()
        benchmark['pools'].append(copy.deepcopy(benchmark['pools'][0]))
        with self.assertRaises(ValueError):
            evaluate(benchmark, {'q': ['a', 'b', 'c']})

    def test_rejects_incomplete_or_unknown_groups_and_duplicate_assets(self):
        for field in ['product_group', 'duplicate_group', 'image_group', 'research_split']:
            benchmark = fixture()
            benchmark['assets'][0][field] = None
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_assets(benchmark['assets'])
        benchmark = fixture()
        benchmark['assets'].append(benchmark['assets'][0])
        with self.assertRaises(ValueError):
            validate_assets(benchmark['assets'])

    def test_rankings_must_be_exact_permutations(self):
        for ranking in [{}, {'q': ['a', 'b']}, {'q': ['a', 'a', 'c']},
                        {'q': ['a', 'b', 'unknown']}, {'q': ['a', 'b', 'c'], 'extra': []},
                        {'q': ['q', 'b', 'c']}, {'q': None}]:
            with self.subTest(ranking=ranking), self.assertRaises(ValueError):
                evaluate(fixture(), ranking)

    def test_no_uncertain_grades_or_repeated_candidates(self):
        for grade in [None, True, 1.5, '2', -1, 4]:
            benchmark = fixture()
            benchmark['pools'][0]['candidates'][0]['grade'] = grade
            with self.subTest(grade=grade), self.assertRaises(ValueError):
                evaluate(benchmark, {'q': ['a', 'b', 'c']})
        benchmark = fixture()
        benchmark['pools'][0]['candidates'].append({'id': 'a', 'grade': 3})
        with self.assertRaises(ValueError):
            evaluate(benchmark, {'q': ['a', 'b', 'c']})

    def test_no_same_product_duplicate_or_original_image_candidates(self):
        for field in ['product_group', 'duplicate_group', 'image_group']:
            benchmark = fixture()
            benchmark['assets'][1][field] = benchmark['assets'][0][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                evaluate(benchmark, {'q': ['a', 'b', 'c']})

    def test_no_cross_split_pool_or_training_query(self):
        for index in [0, 1]:
            benchmark = fixture()
            benchmark['assets'][index]['research_split'] = 'train'
            with self.subTest(index=index), self.assertRaises(ValueError):
                evaluate(benchmark, {'q': ['a', 'b', 'c']})

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"q":[],"q":[]}', object_pairs_hook=unique_object)

    def test_cli_success_and_failure_do_not_overwrite_reports(self):
        script = Path(__file__).resolve().parents[1] / 'scripts' / 'evaluate.py'
        with tempfile.TemporaryDirectory(dir=script.parent.parent) as directory:
            root = Path(directory)
            benchmark, rankings, output = [root / name for name in ['b.json', 'r.json', 'out.json']]
            benchmark.write_text(json.dumps(fixture()), encoding='utf-8')
            rankings.write_text(json.dumps({'q': ['a', 'b', 'c']}), encoding='utf-8')
            command = [sys.executable, str(script), '--benchmark', str(benchmark),
                       '--rankings', str(rankings), '--output', str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            saved = output.read_bytes()
            report = json.loads(saved)
            self.assertEqual(report['by_split']['test']['mean_ndcg_at_5'], 1)
            self.assertEqual(len(report['benchmark_sha256']), 64)
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), saved)
            output.unlink()
            rankings.write_text('{"q":["a"]}', encoding='utf-8')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
