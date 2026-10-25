import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from scripts.audit_unsplash import audit_archive, denim_text


class UnsplashTests(unittest.TestCase):
    def test_screen_is_whole_word_case_insensitive(self):
        self.assertTrue(denim_text('Blue JEANS'))
        self.assertTrue(denim_text('denim jacket'))  # Candidate, not a pants label.
        self.assertFalse(denim_text('Jean-Paul'))
        self.assertFalse(denim_text('jeanswear'))

    def test_join_preserves_unreviewed_state_and_no_location(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root=Path(directory)
            archive=root/'data.zip'
            with zipfile.ZipFile(archive,'w') as bundle:
                bundle.writestr('keywords.tsv000','photo_id\tkeyword\na\tjeans\na\tjeans\nx\tdenim\n')
                bundle.writestr('photos.tsv000','photo_id\tphoto_url\tphoto_image_url\tphoto_description\tai_description\tphoto_location_latitude\na\tu\ti\t\t\t1\nb\tu\ti\tDENIM coat\t\t2\nc\tu\ti\ttree\t\t3\n')
                bundle.writestr('TERMS.md','fixture')
            summary=audit_archive(archive,root/'audit')
            self.assertEqual(summary['photo_rows'],3)
            self.assertEqual(summary['candidate_photos'],2)
            self.assertEqual(summary['images_downloaded'],0)
            rows=[json.loads(line) for line in (root/'audit/denim_candidates.jsonl').read_text().splitlines()]
            self.assertEqual(rows[0]['matched_keywords'],['jeans'])
            self.assertTrue(all(row['research_split'] is None and row['denim_status']=='unreviewed' for row in rows))
            self.assertNotIn('photo_location_latitude',rows[0])
            with self.assertRaises(FileExistsError):
                audit_archive(archive,root/'audit')
