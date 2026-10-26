"""Make model-blind A/B retrieval sheets; no human quality score is computed."""

import argparse
import hashlib
import json
from pathlib import Path
import random

try:
    from .extract_features import REVISION, WEIGHT_SHA256, reviewed_crops
except ImportError:
    from extract_features import REVISION, WEIGHT_SHA256, reviewed_crops


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acquisition', type=Path, required=True)
    parser.add_argument('--trained', type=Path, required=True)
    parser.add_argument('--queries', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not Path('/kaggle/working').is_dir() or args.output.exists():
        parser.error('Remote execution and a new output directory required')
    report = json.loads((args.trained/'training_report.json').read_text())
    checkpoint = args.trained/'last_block.pt'
    if (report['base_revision'] != REVISION or report['base_weights_sha256'] != WEIGHT_SHA256
            or hashlib.sha256(checkpoint.read_bytes()).hexdigest() != report['checkpoint_sha256']
            or hashlib.sha256((args.acquisition/'summary.json').read_bytes()).hexdigest() != report['source_summary_sha256']):
        raise ValueError('Training/source provenance mismatch')
    gallery = json.loads((args.trained/'training_examples.json').read_text())
    gallery_paths = []
    for row in gallery:
        identity = row['image_id']
        if not isinstance(identity,str) or not identity.isdecimal(): raise ValueError('Invalid gallery ID')
        path = args.acquisition/'images'/(identity+'.jpg')
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']: raise ValueError('Image checksum mismatch')
        gallery_paths.append(path)
    packet = json.loads((args.queries/'packet.json').read_text(encoding='utf-8'))
    query_ids = {r['id'] for r in packet['queries']}
    manifest = json.loads((args.queries/'manifest.json').read_text(encoding='utf-8'))
    query_rows = [r for r in manifest['assets'] if r['id'] in query_ids]
    queries = reviewed_crops({'schema_version':1,'assets':query_rows},args.queries)
    if {r[0] for r in queries} != query_ids: raise ValueError('Missing reviewed query')
    import torch
    import open_clip
    from huggingface_hub import snapshot_download
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    if not torch.cuda.is_available(): parser.error('CUDA required')
    snapshot = Path(snapshot_download('Marqo/marqo-fashionSigLIP',revision=REVISION,
        allow_patterns=['open_clip_config.json','open_clip_model.safetensors']))
    with (snapshot/'open_clip_model.safetensors').open('rb') as stream:
        if hashlib.file_digest(stream,'sha256').hexdigest() != WEIGHT_SHA256: raise ValueError('Base weight mismatch')
    model,_,preprocess = open_clip.create_model_and_transforms('local-dir:'+str(snapshot),device='cuda:0',require_pretrained=True)
    model.eval().requires_grad_(False)
    target = model.visual.image_size
    if isinstance(target,int): target = (target,target)
    paths = [r[1] for r in queries]+gallery_paths
    def encode():
        features = []
        with torch.no_grad():
            for start in range(0,len(paths),16):
                tensors = []
                for path in paths[start:start+16]:
                    with Image.open(path) as im:
                        tensors.append(preprocess(ImageOps.pad(ImageOps.exif_transpose(im).convert('RGB'),target,color='white')))
                features.append(model.encode_image(torch.stack(tensors).cuda(),normalize=True).float().cpu())
        features = torch.cat(features)
        assert torch.isfinite(features).all() and torch.allclose(features.norm(dim=1),torch.ones(len(paths)),atol=1e-4)
        scores = features[:len(queries)] @ features[len(queries):].T
        return torch.argsort(scores,dim=1,descending=True,stable=True)[:,:5].tolist()
    rankings = {'starting':encode()}
    saved = torch.load(checkpoint,map_location='cpu',weights_only=True)
    expected = 'visual.trunk.blocks.'+str(len(model.visual.trunk.blocks)-1)
    if saved['module'] != expected or report['trained_module'] != expected: raise ValueError('Wrong trained module')
    model.get_submodule(expected).load_state_dict(saved['state_dict'],strict=True)
    rankings['adapted'] = encode()
    args.output.mkdir(parents=True,exist_ok=False)
    font = ImageFont.load_default(size=18)
    rng, mapping, questions = random.Random(29), {}, []
    for i,query in enumerate(queries):
        order = ['starting','adapted']; rng.shuffle(order)
        mapping['Q'+str(i+1)] = dict(zip(['A','B'],order))
        sheet = Image.new('RGB',(1280,710),'white'); draw = ImageDraw.Draw(sheet)
        draw.text((15,12),'Q'+str(i+1)+' - choose closer list: A / B / tie / neither',font=font,fill='black')
        with Image.open(query[1]) as im:
            sheet.paste(ImageOps.contain(im.convert('RGB'),(245,570)),(10,65))
        draw.text((15,650),'QUERY',font=font,fill='black')
        choices = {}
        for row,(label,which) in enumerate(zip(['A','B'],order)):
            y = 50+row*320; draw.text((270,y),label,font=font,fill='black')
            indices = rankings[which][i]; choices[label] = [gallery[j]['image_id'] for j in indices]
            for rank,j in enumerate(indices):
                x=290+rank*195
                with Image.open(gallery_paths[j]) as im:
                    thumb=ImageOps.contain(im.convert('RGB'),(185,260));sheet.paste(thumb,(x+(185-thumb.width)//2,y+30))
                draw.text((x,y+294),str(rank+1),font=font,fill='black')
        sheet.save(args.output/f'Q{i+1}.jpg',quality=93)
        questions.append({'question':'Q'+str(i+1),'query_id':query[0],'query_credit':query_rows[i].get('credit'),
            'candidates':choices,'response':None})
    (args.output/'questions.json').write_text(json.dumps({'purpose':'qualitative_model_blind_comparison','questions':questions,
        'limits':'Three existing calibration queries, no independent held-out claim. Candidate gallery was used for weak text training. No human score yet.'},indent=2),encoding='utf-8')
    (args.output/'model_mapping_private.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8')
    print(json.dumps({'query_sheets':len(queries),'gallery_images':len(gallery),'same_gallery_before_after':True,
        'checkpoint_sha256':report['checkpoint_sha256'],'quality_evaluated':False,'device':torch.cuda.get_device_name(0)}),flush=True)


if __name__ == '__main__':
    main()
