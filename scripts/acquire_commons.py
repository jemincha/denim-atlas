"""Bounded Commons wearing-photo screening: metadata + at most 24 small previews."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

USER_AGENT = 'DenimAtlasResearch/0.1 (https://github.com/jemincha/denim-atlas)'


def allowed_license(metadata):
    url = metadata.get('LicenseUrl', {}).get('value', '')
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'} or parsed.netloc != 'creativecommons.org':
        return False
    return bool(re.fullmatch(r'/licenses/by/(2\.0|2\.5|3\.0|4\.0)/?(deed\.[a-z_-]+)?', parsed.path)
                or re.fullmatch(r'/publicdomain/zero/1\.0/?(deed\.[a-z_-]+)?', parsed.path))


def preview_url(info):
    url = info.get('thumburl', '')
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc not in {'upload.wikimedia.org', 'thumb.wikimedia.org'}:
        raise ValueError('Unexpected Commons preview host')
    if max(info.get('thumbwidth', 0), info.get('thumbheight', 0)) > 1600:
        raise ValueError('Preview exceeds pilot dimensions')
    return url


def read_url(url, maximum):
    with urlopen(Request(url, headers={'User-Agent': USER_AGENT}), timeout=40) as response:
        raw = response.read(maximum+1)
    if len(raw) > maximum:
        raise ValueError('Response exceeds bound')
    return raw


def main():
    from PIL import Image, ImageDraw, ImageOps
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'previews').mkdir()
    pages, source_hashes = {}, {}
    for category in ['Men wearing jeans', 'Women wearing jeans']:
        params = {'action':'query', 'format':'json', 'generator':'categorymembers',
                  'gcmtitle':'Category:'+category, 'gcmtype':'file', 'gcmlimit':50,
                  'prop':'imageinfo', 'iiprop':'url|size|extmetadata', 'iiurlwidth':480}
        raw = read_url('https://commons.wikimedia.org/w/api.php?'+urlencode(params), 5000000)
        source_hashes[category] = hashlib.sha256(raw).hexdigest()
        (args.output/(category.replace(' ', '_')+'.json')).write_bytes(raw)
        result = json.loads(raw)
        if 'error' in result:
            raise ValueError(str(result['error']))
        pages.update(result.get('query', {}).get('pages', {}))
    candidates = [p for p in pages.values() if allowed_license(p.get('imageinfo',[{}])[0].get('extmetadata',{}))]
    # shortcut: first 24 eligible page IDs test supply only; not representative sampling.
    candidates.sort(key=lambda p:p['pageid'])
    records, errors = [], []
    sheet = Image.new('RGB', (1200, 1000), 'white')
    draw = ImageDraw.Draw(sheet)
    for page in candidates[:24]:
        info = page['imageinfo'][0]
        try:
            url = preview_url(info)
            raw = read_url(url, 1500000)
            with Image.open(io.BytesIO(raw)) as image:
                image.verify()
            with Image.open(io.BytesIO(raw)) as image:
                image = ImageOps.exif_transpose(image).convert('RGB')
                dimensions = list(image.size)
                image.thumbnail((190,210))
                index = len(records)
                x,y = (index%6)*200, (index//6)*250
                sheet.paste(image, (x+(200-image.width)//2,y))
                draw.text((x+4,y+215), f'{index:02d} page {page["pageid"]}', fill='black')
            filename = f'previews/{page["pageid"]}.image'
            (args.output/filename).write_bytes(raw)
            records.append({'id':f'commons:{page["pageid"]}', 'review_index':index,
                            'title':page['title'], 'source_page':info['descriptionurl'],
                            'original_url':info['url'], 'preview_url':url, 'file':filename,
                            'sha256':hashlib.sha256(raw).hexdigest(), 'size':dimensions,
                            'rights_metadata':info['extmetadata'],
                            'usage_status':'license_screened_not_fully_reviewed',
                            'denim_status':'unreviewed', 'crop_status':'unreviewed', 'research_split':None})
        except Exception as error:
            errors.append({'pageid':page['pageid'], 'error':str(error)})
            print('Preview failure:',page['pageid'],str(error),flush=True)
            # Do not continue issuing image requests after a network/service rejection.
            if isinstance(error, OSError):
                break
    sheet.save(args.output/'contact.jpg', quality=92)
    (args.output/'screening_images.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf-8')
    summary = {'complete':not errors, 'checked_at_utc':datetime.now(timezone.utc).isoformat(),
               'metadata_images':len(pages), 'license_eligible':len(candidates),
               'downloaded_previews':len(records), 'errors':errors,
               'licenses':dict(Counter(r['rights_metadata']['LicenseShortName']['value'] for r in records)),
               'preview_bytes':sum((args.output/r['file']).stat().st_size for r in records),
               'metadata_sha256':source_hashes, 'confirmed_denim':0, 'training_ready':0,
               'notes':'Two bounded category pages; CC0/CC BY metadata screen. No original images, model inference, product groups or human relevance labels.'}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)


if __name__ == '__main__':
    main()
