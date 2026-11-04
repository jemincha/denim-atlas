"""Audit cached GLAMI source detail without downloading images or loading models."""

import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image


def audit(root, reviewed):
    rows = [json.loads(line) for line in (root / 'screening_images.jsonl').read_text().splitlines()]
    expected = {str(r['image_id']): r['sha256'] for r in reviewed}
    found, sizes, reviewed_sizes, images = set(), Counter(), Counter(), []
    for row in rows:
        name = str(row['image_id'])
        if not name.isdecimal() or row['file'] != 'images/' + name + '.jpg' or name in found:
            raise ValueError('Invalid or duplicate source image')
        found.add(name)
        path = root / row['file']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row['sha256'] or name in expected and digest != expected[name]:
            raise ValueError('Source checksum mismatch: ' + name)
        with Image.open(path) as image:
            image.load()
            size = '{}x{}'.format(*image.size)
        sizes[size] += 1
        if name in expected:
            reviewed_sizes[size] += 1
        images.append({'id': 'glami:' + name, 'size': size, 'sha256': digest})
    if not set(expected) <= found:
        raise ValueError('Missing reviewed observations')
    metadata = [json.loads(line) for line in (root / 'jeans_rows.jsonl').read_text().splitlines()]
    keys = sorted({key for row in metadata for key in row})
    return {'schema_version': 1, 'cached_images_verified': len(found),
            'reviewed_images_verified': len(expected), 'source_sizes': dict(sizes),
            'reviewed_source_sizes': dict(reviewed_sizes), 'metadata_fields': keys,
            'url_fields': [key for key in keys if 'url' in key.lower()],
            'images': images, 'new_downloads': 0, 'model_inference': False,
            'limits': 'Pixel dimensions do not establish garment or wash readability. '
                      'Upscaling cannot recover absent detail; image rights remain source-specific.'}


if __name__ == '__main__':
    sources = list(Path('/kaggle/input').rglob('screening_images.jsonl'))
    if len(sources) != 1:
        raise ValueError('Expected exactly one cached acquisition')
    reviewed = json.loads(Path(__file__).with_name('reviewed_examples.json').read_text())
    result = audit(sources[0].parent, reviewed)
    output = Path('/kaggle/working/source_audit.json')
    output.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if k != 'images'}, indent=2))
