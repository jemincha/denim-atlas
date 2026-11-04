import copy
import unittest

from scripts.extract_features import REVISION, WEIGHT_SHA256
from scripts.regional_experiment import preference_report, validate_cache


class RegionalExperimentTests(unittest.TestCase):
    def test_axis_disagreement_ties_and_folds_remain_separate(self):
        rows = [{'case_id': 'c', 'axis': 'silhouette', 'split': 'train', 'target': 'A'},
                {'case_id': 'c', 'axis': 'surface', 'split': 'train', 'target': 'B'},
                {'case_id': 'd', 'axis': 'surface', 'split': 'development', 'target': 'A'},
                {'case_id': 'e', 'axis': 'surface', 'split': 'train', 'target': 'tie'}]
        result = preference_report([(.7, .3), (.2, .8), (.3, .7), (.50, .51)], rows)
        self.assertEqual(result['summary']['train']['silhouette']['strict_correct'], 1)
        surface = result['summary']['train']['surface']
        self.assertEqual(surface['strict_correct'], 1)
        self.assertEqual(surface['ties_satisfied'], 1)
        self.assertEqual(surface['strict_comparisons'], 1)
        self.assertEqual(result['summary']['development']['surface']['strict_correct'], 0)
        self.assertAlmostEqual(result['comparisons'][2]['loss'], .45)
        self.assertIsNone(result['comparisons'][3]['strict_correct'])

    def test_score_tie_is_not_a_strict_preference_win(self):
        row = {'case_id': 'x', 'axis': 'surface', 'split': 'train', 'target': 'B'}
        part = preference_report([(.5, .5)], [row])['summary']['train']['surface']
        self.assertEqual(part['preference_agreement'], 0)

    def test_invalid_or_incomplete_scores_fail(self):
        row = {'case_id': 'x', 'axis': 'surface', 'split': 'train', 'target': 'A'}
        for values in ([], [(float('nan'), 0)], [(1, 0), (0, 1)]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                preference_report(values, [row])
        row['target'] = 'neither'
        with self.assertRaises(ValueError):
            preference_report([(1, 0)], [row])

    def test_features_require_exact_observations_model_crops_and_finite_unit_vectors(self):
        inputs = {'packet_sha256': 'packet', 'observations': [{'id': 'a', 'regions': {
            name: {'sha256': name} for name in ('garment', 'hip_thigh')}}]}
        cache = {'schema_version': 1, 'provenance': {'packet_sha256': 'packet',
                 'base_revision': REVISION, 'weights_sha256': WEIGHT_SHA256},
                 'observations': {'a': {name: {'embedding': [1.] + [0.]*767,
                                       'crop_sha256': name} for name in ('garment', 'hip_thigh')}}}
        validate_cache(cache, inputs)
        for kind in ('packet', 'revision', 'extra', 'crop', 'nan', 'dimension', 'norm'):
            bad = copy.deepcopy(cache)
            if kind == 'packet':
                bad['provenance']['packet_sha256'] = 'other'
            elif kind == 'revision':
                bad['provenance']['base_revision'] = 'latest'
            elif kind == 'extra':
                bad['observations']['other'] = bad['observations']['a']
            else:
                feature = bad['observations']['a']['garment']
                if kind == 'crop':
                    feature['crop_sha256'] = 'different'
                elif kind == 'nan':
                    feature['embedding'][0] = float('nan')
                elif kind == 'dimension':
                    feature['embedding'].pop()
                else:
                    feature['embedding'][0] = 2.
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                validate_cache(bad, inputs)


if __name__ == '__main__':
    unittest.main()
