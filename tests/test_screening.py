import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from scripts.audit_screening import audit, image_file


class ScreeningTests(unittest.TestCase):
    def test_paths_cannot_escape(self):
        with self.assertRaises(ValueError):
            image_file(Path(__file__).parent, '../README.md')

    @unittest.skipUnless(importlib.util.find_spec('PIL'), 'Pillow required for image audit')
    def test_audit_duplicates_checksum_and_no_labels(self):
        from PIL import Image
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            image = root/'one.png'
            Image.new('RGB', (20, 30), 'blue').save(image)
            item = {'image_id': 'one', 'file': image.name,
                    'sha256': hashlib.sha256(image.read_bytes()).hexdigest()}
            manifest = root/'images.jsonl'
            manifest.write_text(json.dumps(item)+'\n', encoding='utf-8')
            report = audit({'abo': manifest, 'glami': manifest}, root/'audit')
            self.assertEqual(report['verified_images'], 2)
            self.assertEqual(report['unique_decoded_images'], 1)
            self.assertEqual(report['exact_duplicate_groups'], 1)
            rows = [json.loads(line) for line in (root/'audit/audited_images.jsonl').read_text().splitlines()]
            self.assertTrue(all(row['research_split'] is None and row['denim_status'] == 'unreviewed' for row in rows))
            with self.assertRaises(FileExistsError):
                audit({'abo': manifest}, root/'audit')
            manifest.write_text((json.dumps(item)+'\n')*2, encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Duplicate source image ID'):
                audit({'abo': manifest}, root/'duplicate')
            manifest.write_text('', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Empty source manifest'):
                audit({'abo': manifest}, root/'empty')
            item['sha256'] = '0'*64
            manifest.write_text(json.dumps(item)+'\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                audit({'abo': manifest}, root/'bad')
