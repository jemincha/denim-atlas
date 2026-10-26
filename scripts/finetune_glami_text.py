"""Remote weak image/text adaptation; no human similarity or held-out quality claim."""

import argparse
import hashlib
import html
import importlib.metadata
import io
import json
from pathlib import Path
import random
import re
import time

try:
    from .extract_features import REVISION, WEIGHT_SHA256
except ImportError:
    from extract_features import REVISION, WEIGHT_SHA256


def training_examples(root, approved_ids):
    """Keep one image per known item, decoded image and normalized caption."""
    from PIL import Image, ImageOps
    root = root.resolve(strict=True)
    if (not isinstance(approved_ids, list) or not approved_ids
            or any(not isinstance(k,str) or not re.fullmatch(r'[0-9]+',k) for k in approved_ids)
            or len(set(approved_ids)) != len(approved_ids)):
        raise ValueError('Expected nonempty unique visually approved IDs')
    approved_ids = set(approved_ids)
    records = {}
    for line in (root/'jeans_rows.jsonl').read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        records.setdefault(row['image_id'], []).append(row)
    seen_items, seen_pixels, seen_text = set(), set(), set()
    result, encountered = [], set()
    for line in (root/'screening_images.jsonl').read_text(encoding='utf-8').splitlines():
        image = json.loads(line)
        identity = image['image_id']
        if identity not in approved_ids:
            continue
        encountered.add(identity)
        if not re.fullmatch(r'[0-9]+', identity):
            raise ValueError('Unexpected image ID')
        path = root/'images'/(identity+'.jpg')
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError('Image path outside source root')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != image['sha256']:
            raise ValueError('Source image checksum mismatch')
        with Image.open(io.BytesIO(raw)) as source:
            decoded = ImageOps.exif_transpose(source).convert('RGB')
            if min(decoded.size) < 80:
                continue
            pixels = hashlib.sha256(str(decoded.size).encode()+decoded.tobytes()).hexdigest()
        candidates = records[identity]
        item_ids = {str(r['item_id']) for r in candidates if r.get('item_id')}
        item_ids |= {str(r['itemid']) for r in candidates if r.get('itemid')}
        row = candidates[0]
        caption = html.unescape(re.sub('<[^>]*>', ' ', row.get('name','')+' '+row.get('description','')))
        caption = ' '.join(caption.split())[:400]
        caption_key = caption.casefold()
        if len(caption) < 16 or item_ids & seen_items or pixels in seen_pixels or caption_key in seen_text:
            continue
        seen_items.update(item_ids); seen_pixels.add(pixels); seen_text.add(caption_key)
        result.append({'image_id':identity,'file':str(path),'caption':caption,
                       'sha256':image['sha256'],'pixel_sha256':pixels,'item_ids':sorted(item_ids)})
    if encountered != approved_ids:
        raise ValueError('Approved image missing from acquisition')
    random.Random(17).shuffle(result)
    return result[:512]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, required=True)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not Path('/kaggle/working').is_dir():
        parser.error('Remote Kaggle GPU only')
    if args.output.exists():
        parser.error('Output must be new')
    summary_raw = (args.input_root/'summary.json').read_bytes()
    review = json.loads(args.review.read_text(encoding='utf-8'))
    if (review.get('decision') != 'proceed_weak_text_pilot'
            or review.get('source_summary_sha256') != hashlib.sha256(summary_raw).hexdigest()):
        raise ValueError('Sample visual review for this exact acquisition is required')
    examples = training_examples(args.input_root, review.get('approved_image_ids'))
    if len(examples) < 32:
        raise ValueError('Need at least 32 deduplicated image/text examples')
    import torch
    import open_clip
    from open_clip.loss import ClipLoss
    from huggingface_hub import snapshot_download
    from PIL import Image, ImageOps
    if not torch.cuda.is_available():
        parser.error('CUDA required; no laptop or CPU fallback')
    if importlib.metadata.version('open_clip_torch') != '3.3.0':
        parser.error('Expected open_clip_torch==3.3.0')
    torch.manual_seed(17); torch.cuda.manual_seed_all(17)
    snapshot = Path(snapshot_download('Marqo/marqo-fashionSigLIP', revision=REVISION,
        allow_patterns=['open_clip_config.json','open_clip_model.safetensors',
                        'tokenizer.json','tokenizer_config.json','special_tokens_map.json','spiece.model']))
    if not (snapshot/'tokenizer.json').is_file():
        raise ValueError('Pinned local tokenizer files are required for image/text training')
    with (snapshot/'open_clip_model.safetensors').open('rb') as stream:
        if hashlib.file_digest(stream,'sha256').hexdigest() != WEIGHT_SHA256:
            raise ValueError('Base checkpoint mismatch')
    model,_,preprocess = open_clip.create_model_and_transforms(
        'local-dir:'+str(snapshot), device='cuda:0', require_pretrained=True)
    tokenizer = open_clip.get_tokenizer('local-dir:'+str(snapshot))
    model.eval().requires_grad_(False)
    module_name = 'visual.trunk.blocks.'+str(len(model.visual.trunk.blocks)-1)
    module = model.get_submodule(module_name)
    module.requires_grad_(True)
    optimizer = torch.optim.AdamW(module.parameters(), lr=1e-6, weight_decay=0.01)
    loss_fn = ClipLoss()
    tensors, texts = [], []
    target_size = model.visual.image_size
    if isinstance(target_size, int): target_size = (target_size, target_size)
    for row in examples:
        with Image.open(row['file']) as image:
            image = ImageOps.exif_transpose(image).convert('RGB')
            tensors.append(preprocess(ImageOps.pad(image, target_size, color='white')))
        texts.append(row['caption'])
    tensors = torch.stack(tensors)
    text_features = []
    with torch.no_grad():
        for start in range(0,len(texts),16):
            text_features.append(model.encode_text(tokenizer(texts[start:start+16]).cuda(),normalize=True).detach().float())
    text_features = torch.cat(text_features)
    scale = model.logit_scale.detach().float().exp().clamp(max=100)
    batches = [list(range(start,min(start+16,len(examples)))) for start in range(0,len(examples),16)]
    batches = [b for b in batches if len(b) >= 2]
    def fitting_loss():
        values = []
        with torch.no_grad():
            for ids in batches:
                encoded = model.encode_image(tensors[ids].cuda(),normalize=True).float()
                values.append((len(ids),loss_fn(encoded,text_features[ids],scale).item()))
        return sum(n*v for n,v in values)/sum(n for n,_ in values)
    def digest():
        h = hashlib.sha256()
        for name,value in module.state_dict().items():
            h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()
    before_hash, before_loss = digest(), fitting_loss()
    print(json.dumps({'training_images':len(examples),'fixed_batch_loss_before':before_loss,'precision':'fp32'}),flush=True)
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'training_examples.json').write_text(json.dumps(examples,ensure_ascii=False),encoding='utf-8')
    history, started = [], time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    rng = random.Random(17)
    for epoch in range(2):
        order = list(range(len(examples))); rng.shuffle(order)
        for start in range(0,len(order),16):
            ids = order[start:start+16]
            if len(ids) < 2: continue
            optimizer.zero_grad(set_to_none=True)
            encoded = model.encode_image(tensors[ids].cuda(),normalize=True).float()
            loss = loss_fn(encoded,text_features[ids],scale)
            if not torch.isfinite(loss).item(): raise ValueError('Nonfinite loss')
            loss.backward()
            norm = torch.nn.utils.clip_grad_norm_(module.parameters(),1.0,error_if_nonfinite=True)
            optimizer.step()
            history.append({'step':len(history)+1,'epoch':epoch+1,'loss':loss.item(),'gradient_norm':norm.item()})
            if len(history)%8 == 0: print(json.dumps(history[-1]),flush=True)
    after_hash, after_loss = digest(), fitting_loss()
    if before_hash == after_hash: raise ValueError('No trained parameter update')
    checkpoint = args.output/'last_block.pt'
    torch.save({'module':module_name,'state_dict':module.state_dict(),
        'optimizer':optimizer.state_dict(),
        'steps':len(history),'base_revision':REVISION,'base_weights_sha256':WEIGHT_SHA256,
        'purpose':'weak_glami_image_text_training_only'},checkpoint)
    saved = torch.load(checkpoint,map_location='cpu',weights_only=True)
    with torch.no_grad(): next(module.parameters()).zero_()
    module.load_state_dict(saved['state_dict'],strict=True)
    if digest() != after_hash: raise ValueError('Checkpoint block restoration failed')
    report = {'schema_version':1,'purpose':'weak_image_text_adaptation','training_run':True,
        'held_out_similarity_evaluation':False,'real_training_images':len(examples),
        'epochs':2,'steps':len(history),'batch_size':16,'learning_rate':1e-6,'seed':17,
        'precision':'fp32; prior FP16 attempt stopped on nonfinite gradient norm',
        'loss':'open_clip ClipLoss, frozen source-description text embeddings',
        'all_training_fixed_batch_loss_before':before_loss,'all_training_fixed_batch_loss_after':after_loss,
        'base_revision':REVISION,'base_weights_sha256':WEIGHT_SHA256,'trained_module':module_name,
        'tokenizer_files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in snapshot.iterdir() if p.name in {'tokenizer.json','tokenizer_config.json','special_tokens_map.json','spiece.model'}},
        'trainable_parameters':sum(p.numel() for p in module.parameters()),
        'module_sha256_before':before_hash,'module_sha256_after':after_hash,
        'checkpoint_roundtrip_verified':True,'checkpoint_bytes':checkpoint.stat().st_size,
        'checkpoint_sha256':hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        'source_summary_sha256':hashlib.sha256(summary_raw).hexdigest(),'visual_review':review,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'history':history,'seconds':time.perf_counter()-started,
        'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,'device':torch.cuda.get_device_name(0),
        'packages':{k:importlib.metadata.version(k) for k in ['torch','open_clip_torch','timm','Pillow','transformers','tokenizers']},
        'limits':'Training IDs visually screened by Codex, without human relevance labels. Full acquired corpus is not individually cleared. Captions may be multilingual/noisy. Known item, exact decoded image and caption dedup only; near duplicates unresolved. Same-data fitting metrics do not show unseen retrieval improvement. Fixed white letterbox; no color jitter or random crops.'}
    (args.output/'training_report.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='history'},indent=2),flush=True)


if __name__ == '__main__':
    main()
