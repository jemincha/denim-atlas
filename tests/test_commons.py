import unittest
from scripts.acquire_commons import allowed_license, preview_url


class CommonsTests(unittest.TestCase):
    def test_license_requires_known_canonical_url_not_label(self):
        for path in ['licenses/by/4.0/', 'licenses/by/2.0', 'publicdomain/zero/1.0/deed.en']:
            self.assertTrue(allowed_license({'LicenseUrl':{'value':'https://creativecommons.org/'+path}}))
        for url in ['https://creativecommons.org/licenses/by-sa/4.0/',
                    'https://creativecommons.org/licenses/by-nc/4.0/',
                    'https://creativecommons.org.example.org/licenses/by/4.0/', '']:
            self.assertFalse(allowed_license({'LicenseShortName':{'value':'CC BY 4.0'},'LicenseUrl':{'value':url}}))

    def test_download_host_and_preview_bound(self):
        self.assertEqual(preview_url({'thumburl':'https://upload.wikimedia.org/a.jpg','thumbwidth':480}),
                         'https://upload.wikimedia.org/a.jpg')
        for info in [{'thumburl':'https://example.org/a.jpg'},
                     {'thumburl':'http://upload.wikimedia.org/a.jpg'},
                     {'thumburl':'https://upload.wikimedia.org/a.jpg','thumbheight':3000}]:
            with self.assertRaises(ValueError):
                preview_url(info)
