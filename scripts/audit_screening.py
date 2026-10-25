"""Verify remote screening images and build contact sheets, without assigning labels."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


def image_file(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Image path missing or outside source directory')
    return path


def audit(sources, output):
    from PIL import Image, ImageDraw, ImageOps
    output.mkdir(exist_ok=False)
    rows, thumbnails, seen = [], [], set()
    for source, manifest in sources.items():
        lines = manifest.read_text(encoding='utf-8').splitlines()
        if not lines:
            raise ValueError('Empty source manifest: ' + source)
        for line in lines:
            item = json.loads(line)
            identity = source + ':' + str(item['image_id'])
            if identity in seen:
                raise ValueError('Duplicate source image ID: ' + identity)
            seen.add(identity)
            path = image_file(manifest.parent, item['file'])
            checksum = hashlib.sha256(path.read_bytes()).hexdigest()
            if checksum != item['sha256']:
                raise ValueError('Checksum mismatch: ' + identity)
            with Image.open(path) as original:
                image = ImageOps.exif_transpose(original).convert('RGBA')
                background = Image.new('RGBA', image.size, 'white')
                background.alpha_composite(image)
                image = background.convert('RGB')
            pixel_hash = hashlib.sha256(str(image.size).encode() + b'\0' + image.tobytes()).hexdigest()
            row = dict(item, id=identity, source=source, source_manifest=str(manifest),
                       image_file=str(path), oriented_size=list(image.size), pixel_sha256=pixel_hash,
                       short_side=min(image.size), research_split=None,
                       denim_status='unreviewed', crop_status='unreviewed')
            rows.append(row)
            image.thumbnail((148, 188))
            thumbnails.append(image.copy())
    groups = defaultdict(list)
    for row in rows:
        groups[row['pixel_sha256']].append(row['id'])
    duplicates = [ids for ids in groups.values() if len(ids) > 1]
    sheets = []
    for start in range(0, len(rows), 48):
        sheet = Image.new('RGB', (960, 1320), 'white')
        draw = ImageDraw.Draw(sheet)
        for offset, (row, thumbnail) in enumerate(zip(rows[start:start+48], thumbnails[start:start+48])):
            x, y = (offset % 6)*160, (offset//6)*165
            thumbnail.thumbnail((150, 130))
            sheet.paste(thumbnail, (x+(160-thumbnail.width)//2, y))
            draw.text((x+3, y+132), str(start+offset).zfill(3)+' '+row['source'], fill='black')
            draw.text((x+3, y+146), str(row['oriented_size']), fill='black')
            row['review_index'] = start+offset
        name = f'contact_{start//48:02d}.jpg'
        sheet.save(output/name, quality=92)
        sheets.append(name)
    (output/'audited_images.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows), encoding='utf-8')
    (output/'exact_duplicate_groups.json').write_text(json.dumps(duplicates, indent=2), encoding='utf-8')
    summary = {'schema_version': 1, 'verified_images': len(rows),
               'sources': dict(Counter(row['source'] for row in rows)),
               'unique_decoded_images': len(groups), 'exact_duplicate_groups': len(duplicates),
               'short_side_below_224': dict(Counter(row['source'] for row in rows if row['short_side'] < 224)),
               'contact_sheets': sheets, 'confirmed_denim': 0, 'reviewed_crops': 0,
               'notes': 'Exact decoded-pixel equality only; no near-duplicate/product identity or relevance inferred.',
               'source_manifest_sha256': {s: hashlib.sha256(p.read_bytes()).hexdigest() for s,p in sources.items()}}
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--abo', required=True, type=Path)
    parser.add_argument('--glami', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not Path('/kaggle/working').is_dir():
        raise RuntimeError('Run the bulk image audit on Kaggle, not the laptop')
    print(json.dumps(audit({'abo': args.abo, 'glami': args.glami}, args.output), indent=2))
