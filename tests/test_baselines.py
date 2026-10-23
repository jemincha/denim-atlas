import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.extract_features import mean_rgb, reviewed_crops
from scripts.run_baselines import rank_baselines


def fixture():
    assets = [{'id': key, 'research_split': 'test', 'product_group': 'p-' + key,
               'duplicate_group': 'd-' + key, 'image_group': 'i-' + key}
              for key in ['q', 'a', 'b']]
    benchmark = {'schema_version': 1, 'assets': assets, 'pools': [
        {'query_id': 'q', 'candidates': [{'id': 'b', 'grade': 3}, {'id': 'a', 'grade': 0}]}]}
    features = {'schema_version': 1, 'assets': {
        'q': {'embedding': [2, 0], 'mean_rgb': [0, 0, 0]},
        'a': {'embedding': [1, 0], 'mean_rgb': [1, 1, 1]},
        'b': {'embedding': [0, 1], 'mean_rgb': [0, 0, 0]}}}
    return benchmark, features


class BaselineTests(unittest.TestCase):
    def test_normalized_cosine_and_color_weight_endpoints(self):
        benchmark, features = fixture()
        b0, b1 = rank_baselines(benchmark, features, 0)
        self.assertEqual(b0, {'q': ['a', 'b']})
        self.assertEqual(b1, b0)
        self.assertEqual(rank_baselines(benchmark, features, 1)[1], {'q': ['b', 'a']})
        self.assertEqual(rank_baselines(benchmark, features, 0.5)[1], {'q': ['b', 'a']})

    def test_grades_do_not_change_ranks_and_ties_use_ids(self):
        benchmark, features = fixture()
        features['assets']['b'] = copy.deepcopy(features['assets']['a'])
        before = rank_baselines(benchmark, features, 0.5)
        self.assertEqual(before, ({'q': ['a', 'b']}, {'q': ['a', 'b']}))
        for row in benchmark['pools'][0]['candidates']:
            row['grade'] = 3 - row['grade']
        self.assertEqual(rank_baselines(benchmark, features, 0.5), before)

    def test_invalid_features_and_weights_fail(self):
        for benchmark in [None, {}, {'schema_version': 1, 'assets': [], 'pools': None}]:
            with self.subTest(benchmark=benchmark), self.assertRaises(ValueError):
                rank_baselines(benchmark, {}, 0.5)
        for field, value in [('embedding', [0, 0]), ('embedding', [1]),
                             ('embedding', [float('nan'), 0]), ('embedding', [True, 0]),
                             ('mean_rgb', [0, 0, 2]), ('mean_rgb', [0, 0])]:
            benchmark, features = fixture()
            features['assets']['a'][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                rank_baselines(benchmark, features, 0.5)
        benchmark, features = fixture()
        for weight in [-1, 2, float('nan'), True]:
            with self.subTest(weight=weight), self.assertRaises(ValueError):
                rank_baselines(benchmark, features, weight)
        del features['assets']['a']
        with self.assertRaises(ValueError):
            rank_baselines(benchmark, features, 0.5)

    def test_cli_end_to_end_and_output_protection(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root) as directory:
            directory = Path(directory)
            benchmark, features = fixture()
            (directory / 'b.json').write_text(json.dumps(benchmark), encoding='utf-8')
            (directory / 'f.json').write_text(json.dumps(features), encoding='utf-8')
            command = [sys.executable, str(root / 'scripts/run_baselines.py'),
                       '--benchmark', str(directory / 'b.json'), '--features', str(directory / 'f.json'),
                       '--color-weight', '0.5', '--output', str(directory / 'run')]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads((directory / 'run/summary.json').read_text())
            b0 = json.loads((directory / 'run/b0-report.json').read_text())
            b1 = json.loads((directory / 'run/b1-report.json').read_text())
            self.assertTrue(summary['complete'])
            self.assertEqual(b1['by_split']['test']['mean_ndcg_at_5'], 1)
            self.assertLess(b0['by_split']['test']['mean_ndcg_at_5'], 1)
            self.assertEqual(b0['benchmark_sha256'], b1['benchmark_sha256'])
            ranking_raw = (directory / 'run/b1-rankings.json').read_bytes()
            self.assertEqual(b1['rankings_sha256'], hashlib.sha256(ranking_raw).hexdigest())
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual((directory / 'run/b1-rankings.json').read_bytes(), ranking_raw)


class CropTests(unittest.TestCase):
    def test_review_checksum_and_path_boundary(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root) as directory:
            directory = Path(directory)
            image_root = directory / 'images'
            image_root.mkdir()
            (image_root / 'crop.jpg').write_bytes(b'fixture bytes, no real photo')
            digest = hashlib.sha256((image_root / 'crop.jpg').read_bytes()).hexdigest()
            row = {'id': 'q', 'usage_status': 'approved', 'denim_status': 'confirmed',
                   'crop_status': 'reviewed', 'crop_file': 'crop.jpg', 'crop_sha256': digest}
            manifest = {'schema_version': 1, 'assets': [row]}
            self.assertEqual(reviewed_crops(manifest, image_root)[0][0], 'q')
            for field, value in [('usage_status', 'pending'), ('denim_status', 'unknown'),
                                 ('crop_status', None), ('crop_sha256', 'wrong'),
                                 ('crop_file', '../outside.jpg'), ('crop_file', str(image_root / 'crop.jpg'))]:
                invalid = copy.deepcopy(manifest)
                invalid['assets'][0][field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    reviewed_crops(invalid, image_root)
            manifest['assets'].append(row)
            with self.assertRaises(ValueError):
                reviewed_crops(manifest, image_root)

    def test_mean_rgb_preserves_observed_channels(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Optional Pillow is only required on the image-processing runtime')
        image = Image.new('RGB', (2, 1))
        image.putdata([(0, 128, 255), (255, 128, 0)])
        self.assertEqual(mean_rgb(image), [0.5, 128 / 255, 0.5])
        with self.assertRaises(ValueError):
            mean_rgb(Image.new('RGBA', (1, 1)))


if __name__ == '__main__':
    unittest.main()
