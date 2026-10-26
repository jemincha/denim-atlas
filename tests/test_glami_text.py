import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.finetune_glami_text import training_examples


class GlamiTextTests(unittest.TestCase):
    def test_pixel_item_and_caption_duplicates_and_checksums(self):
        from PIL import Image
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory); (root/'images').mkdir()
            metadata, images = [], []
            for i, color, item, caption in [
                (1,'blue','a','Blue straight jeans for women'),
                (2,'blue','b','Different description of jeans'),
                (3,'red','a','Red wide leg denim trousers'),
                (4,'green','c','Blue straight jeans for women'),
                (5,'black','d','Black tapered denim trousers')]:
                path=root/'images'/f'{i}.jpg'; Image.new('RGB',(100,120),color).save(path)
                metadata.append({'image_id':str(i),'item_id':item,'name':caption})
                images.append({'image_id':str(i),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            (root/'jeans_rows.jsonl').write_text('\n'.join(map(json.dumps,metadata)))
            manifest=root/'screening_images.jsonl'
            manifest.write_text('\n'.join(map(json.dumps,images)))
            approved = [str(i) for i in range(1,6)]
            self.assertEqual({r['image_id'] for r in training_examples(root,approved)},{'1','5'})
            self.assertEqual([r['image_id'] for r in training_examples(root,['5'])],['5'])
            with self.assertRaisesRegex(ValueError,'missing'):
                training_examples(root,['999'])
            images[0]['sha256']='0'*64
            manifest.write_text('\n'.join(map(json.dumps,images)))
            with self.assertRaisesRegex(ValueError,'checksum'):
                training_examples(root,approved)
