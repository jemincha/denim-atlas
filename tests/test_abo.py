import unittest

from scripts.acquire_abo import image_path, jeans_candidate
from scripts.acquire_glami import jeans_candidate as glami_candidate


class AboTests(unittest.TestCase):
    def test_title_screening_does_not_infer_from_marketing_or_color(self):
        def item(title):
            return {'item_name': [{'language_tag': 'en_US', 'value': title}]}
        for title in ['Slim fit jeans', 'Denim straight leg pants']:
            self.assertTrue(jeans_candidate(item(title)))
        for title in ['Denim jacket', 'Jeans shorts', 'Blue sofa', 'Jeans skirt',
                      'Jeans denim phone case', 'Jeans sneakers', 'iPhone jeans cover']:
            self.assertFalse(jeans_candidate(item(title)))
        self.assertFalse(jeans_candidate({'bullet_point': [{'value': 'wear with jeans'}]}))

    def test_image_paths_cannot_escape_official_tree(self):
        self.assertEqual(image_path('ab/ab1234.jpg'), 'ab/ab1234.jpg')
        for value in ['../../private', 'https://example.com/a.jpg', 'ab/../a.jpg', '/ab/ab12.jpg', None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                image_path(value)

    def test_glami_pants_taxonomy_needs_text_screening(self):
        self.assertTrue(glami_candidate({'category_name': 'womens-pants', 'name': 'Slim Jeans'}))
        self.assertFalse(glami_candidate({'category_name': 'womens-denim-jackets', 'name': 'Denim'}))
        self.assertFalse(glami_candidate({'category_name': 'mens-pants', 'name': 'Chinos'}))


if __name__ == '__main__':
    unittest.main()
