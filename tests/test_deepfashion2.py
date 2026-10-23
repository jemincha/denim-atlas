import copy
import json
import unittest

from scripts.prepare_deepfashion2 import trousers_candidates, unique_object


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.data = {'source': 'shop', 'pair_id': 12,
                     'item1': {'category_id': 8, 'style': 1, 'bounding_box': [10, 20, 50, 100]}}

    def test_preserves_observations_without_inventing_denim_or_relevance(self):
        row = trousers_candidates(self.data, '000001', 'train')[0]
        self.assertEqual(row['bbox_xyxy_pixels'], [10, 20, 50, 100])
        self.assertEqual(row['denim_status'], 'unreviewed')
        self.assertIsNone(row['research_split'])
        self.assertEqual(row['rights_status'], 'usage_scope_review_pending')
        self.assertNotIn('relevance', row)

    def test_styles_and_domains_share_conservative_pair_group(self):
        left = trousers_candidates(self.data, '000001', 'train')[0]
        other = copy.deepcopy(self.data)
        other['source'] = 'user'
        other['item1']['style'] = 2
        right = trousers_candidates(other, '000002', 'train')[0]
        self.assertEqual(left['product_group_candidate'], right['product_group_candidate'])
        self.assertNotEqual(left['id'], right['id'])

    def test_missing_pair_and_zero_style_do_not_create_identity_positive(self):
        self.data['pair_id'] = 0
        self.data['item1']['style'] = 0
        row = trousers_candidates(self.data, '000001', 'validation')[0]
        self.assertIsNone(row['product_group_candidate'])
        self.assertEqual(row['group_status'], 'missing')

    def test_invalid_geometry_ids_domain_and_style_are_rejected(self):
        for box in [[0, 0, 0, 1], [-1, 0, 4, 5], [0, 0, float('nan'), 5]]:
            with self.subTest(box=box):
                self.data['item1']['bounding_box'] = box
                with self.assertRaises(ValueError):
                    trousers_candidates(self.data, '000001', 'train')
        with self.assertRaises(ValueError):
            trousers_candidates(self.data, '../001', 'train')
        self.data['item1']['bounding_box'] = [0, 0, 4, 5]
        self.data['item1']['style'] = -1
        with self.assertRaises(ValueError):
            trousers_candidates(self.data, '000001', 'train')
        self.data['source'] = 'unknown'
        with self.assertRaises(ValueError):
            trousers_candidates(self.data, '000001', 'train')

    def test_excludes_other_clothes_and_rejects_duplicate_json_keys(self):
        self.data['item1']['category_id'] = 1
        self.assertEqual(trousers_candidates(self.data, '000001', 'train'), [])
        with self.assertRaises(ValueError):
            json.loads('{"pair_id":1,"pair_id":2}', object_pairs_hook=unique_object)


if __name__ == '__main__':
    unittest.main()
