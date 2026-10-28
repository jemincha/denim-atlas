"""Remote real-label fine-tuning pilot; training-set fitting, no held-out claim."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import time

try:
    from .extract_features import REVISION, WEIGHT_SHA256, reviewed_crops
    from .evaluate import unique_object, ndcg_at_5
    from .import_judgments import import_ratings
except ImportError:
    from extract_features import REVISION, WEIGHT_SHA256, reviewed_crops
    from evaluate import unique_object, ndcg_at_5
    from import_judgments import import_ratings


def training_triplets(packet, ratings):
    labels = import_ratings(packet, ratings)['judged_unique_pairs']
    queries = sorted({r['query_id'] for r in labels})
    triples = []
    for query in queries:
        positive = sorted(r['candidate_id'] for r in labels
                          if r['query_id'] == query and r['grade'] >= 2)
        negative = sorted(r['candidate_id'] for r in labels
                          if r['query_id'] == query and r['grade'] == 0)
        triples.extend((query,p,n) for p in positive for n in negative)
    if not triples:
        raise ValueError('Need a query with both grade >=2 and grade 0 candidates')
    return triples


def initial_checkpoint(root):
    report = json.loads((root/'training_report.json').read_text(encoding='utf-8'),object_pairs_hook=unique_object)
    path = root/'last_block.pt'
    if (report.get('base_revision') != REVISION or report.get('base_weights_sha256') != WEIGHT_SHA256
            or hashlib.sha256(path.read_bytes()).hexdigest() != report.get('checkpoint_sha256')):
        raise ValueError('Initial checkpoint provenance mismatch')
    return path, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--initial-run', type=Path, help='Continue a checksum-verified trained block with fresh optimizer')
    parser.add_argument('--steps', type=int, default=40)
    args = parser.parse_args()
    if not 1 <= args.steps <= 1000:
        parser.error('steps must be 1..1000')
    if not Path('/kaggle/working').is_dir():
        parser.error('Kaggle GPU only; no local training')
    if args.output.exists():
        parser.error('Output already exists')
    source = args.input_root
    packet_raw = (source/'packet.json').read_bytes()
    ratings_raw = (source/'ratings.json').read_bytes()
    packet = json.loads(packet_raw,object_pairs_hook=unique_object)
    ratings = json.loads(ratings_raw,object_pairs_hook=unique_object)
    triples = training_triplets(packet,ratings)
    manifest_raw = (source/'manifest.json').read_bytes()
    crops = reviewed_crops(json.loads(manifest_raw,object_pairs_hook=unique_object),source)
    pinned = {r['id']:r['crop_sha256'] for r in packet['queries']+packet['candidates']}
    if {identity:checksum for identity,_,checksum in crops} != pinned:
        raise ValueError('Training crops do not match the rated packet')
    import torch
    import torch.nn.functional as F
    import open_clip
    from huggingface_hub import snapshot_download
    from PIL import Image, ImageOps
    if not torch.cuda.is_available():
        parser.error('CUDA required; no CPU fallback')
    if importlib.metadata.version('open_clip_torch') != '3.3.0':
        parser.error('Expected open_clip_torch==3.3.0')
    rng = random.Random(17)
    torch.manual_seed(17)
    torch.cuda.manual_seed_all(17)
    snapshot = Path(snapshot_download('Marqo/marqo-fashionSigLIP',revision=REVISION,
        allow_patterns=['open_clip_config.json','open_clip_model.safetensors']))
    with (snapshot/'open_clip_model.safetensors').open('rb') as stream:
        assert hashlib.file_digest(stream,'sha256').hexdigest() == WEIGHT_SHA256
    model,_,preprocess = open_clip.create_model_and_transforms(
        'local-dir:'+str(snapshot),device='cuda:0',require_pretrained=True)
    model.eval().requires_grad_(False)
    blocks = model.visual.trunk.blocks
    module_name = 'visual.trunk.blocks.'+str(len(blocks)-1)
    module = model.get_submodule(module_name)
    parent = None
    if args.initial_run:
        path, parent = initial_checkpoint(args.initial_run)
        saved = torch.load(path,map_location='cpu',weights_only=True)
        if saved['module'] != module_name or parent['trained_module'] != module_name:
            raise ValueError('Initial trainable module mismatch')
        module.load_state_dict(saved['state_dict'],strict=True)
    module.requires_grad_(True)
    optimizer = torch.optim.AdamW(module.parameters(),lr=1e-5,weight_decay=0.01)
    tensors = {}
    target = model.visual.image_size
    if isinstance(target,int): target = (target,target)
    for identity,path,checksum in crops:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == checksum
        with Image.open(path) as image:
            assert image.mode == 'RGB'
            tensors[identity] = preprocess(ImageOps.pad(image,target,color='white'))
    def digest():
        h = hashlib.sha256()
        for name,value in module.state_dict().items():
            h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()
    labels = {(r['query_id'],r['candidate_id']):r['grade'] for r in import_ratings(packet,ratings)['judged_unique_pairs']}
    def fitting_metrics():
        with torch.inference_mode():
            encoded = {key:model.encode_image(value.unsqueeze(0).cuda(),normalize=True).float()[0]
                       for key,value in tensors.items()}
            losses = [torch.relu(0.1-(encoded[q]*encoded[p]).sum()+(encoded[q]*encoded[n]).sum())
                      for q,p,n in triples]
        scores = []
        for i,query in enumerate(packet['queries']):
            q=query['id']; pool=packet['candidate_pools'][i]
            complete=all((q,c) in labels for c in pool)
            ordered=sorted(pool,key=lambda c:(-float(encoded[q]@encoded[c]),c))
            scores.append({'query_id':q,'fully_judged_pool':complete,
                'training_pool_ndcg_at_5':ndcg_at_5([labels[q,c] for c in ordered]) if complete else None})
        return torch.stack(losses).mean().item(),scores
    before_hash = digest()
    if parent and before_hash != parent['module_sha256_after']:
        raise ValueError('Initial block digest mismatch')
    before_loss,before_scores = fitting_metrics()
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'triplets.json').write_text(json.dumps({'purpose':'training_only_overfit_pilot',
        'triplets':triples,'packet_sha256':packet['packet_sha256']}),encoding='utf-8')
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    history = []
    order = list(triples);rng.shuffle(order)
    for step in range(args.steps):
        query,positive,negative = order[step % len(order)]
        batch = torch.stack([tensors[k] for k in (query,positive,negative)]).cuda()
        optimizer.zero_grad(set_to_none=True)
        encoded = model.encode_image(batch,normalize=True).float()
        loss = torch.relu(0.1-F.cosine_similarity(encoded[0:1],encoded[1:2])
                          +F.cosine_similarity(encoded[0:1],encoded[2:3])).mean()
        assert torch.isfinite(loss).item()
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(module.parameters(),1.0,error_if_nonfinite=True)
        optimizer.step()
        history.append({'step':step+1,'sample_hinge_loss':loss.item(),'gradient_norm':norm.item()})
        if (step+1)%10 == 0: print(json.dumps(history[-1]),flush=True)
    after_hash = digest()
    after_loss,after_scores = fitting_metrics()
    assert after_hash != before_hash, 'No learned parameter update'
    checkpoint = args.output/'last_block.pt'
    torch.save({'module':module_name,'state_dict':module.state_dict(),
        'optimizer':optimizer.state_dict(),
        'torch_rng':torch.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all(),
        'step':args.steps,'model_revision':REVISION,'weights_sha256':WEIGHT_SHA256,
        'packet_sha256':packet['packet_sha256'],'purpose':'training_only_overfit_pilot'},checkpoint)
    saved = torch.load(checkpoint,map_location='cpu',weights_only=True)
    with torch.no_grad(): next(module.parameters()).zero_()
    module.load_state_dict(saved['state_dict'],strict=True)
    assert digest() == after_hash, 'Checkpoint restoration mismatch'
    report = {'schema_version':1,'training_run':True,'held_out_evaluation':False,
        'purpose':'training_only_overfit_pilot','base_revision':REVISION,
        'base_weights_sha256':WEIGHT_SHA256,'trained_module':module_name,
        'trainable_parameters':sum(p.numel() for p in module.parameters()),
        'real_images':len(crops),'queries':len(packet['queries']),
        'triplet_combinations':len(triples),'optimizer_steps':args.steps,'seed':17,'precision':'fp32',
        'initial_checkpoint_sha256':parent['checkpoint_sha256'] if parent else None,
        'source_summary_sha256':parent.get('source_summary_sha256') if parent else None,
        'optimizer_initialization':'fresh; parent optimizer intentionally not restored',
        'preprocessing':'fixed white letterbox, original color; no random crop/jitter',
        'learning_rate':1e-5,'cosine_margin':0.1,'weight_decay':0.01,
        'all_training_triplets_hinge_before':before_loss,
        'all_training_triplets_hinge_after':after_loss,'history':history,
        'training_pool_results_before':before_scores,'training_pool_results_after':after_scores,
        'module_sha256_before':before_hash,'module_sha256_after':after_hash,
        'checkpoint_roundtrip_verified':True,'checkpoint_bytes':checkpoint.stat().st_size,
        'checkpoint_verification_scope':'Trainable block weights restored in same kernel; interrupted-job determinism not tested',
        'training_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checkpoint_sha256':hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        'seconds':time.perf_counter()-started,'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,
        'device':torch.cuda.get_device_name(0),'packages':{k:importlib.metadata.version(k)
            for k in ['torch','torchvision','open_clip_torch','timm','Pillow']},
        'input_sha256':{'packet':hashlib.sha256(packet_raw).hexdigest(),
            'ratings':hashlib.sha256(ratings_raw).hexdigest(),'manifest':hashlib.sha256(manifest_raw).hexdigest()},
        'limits':'All three calibration queries used for training. Product groups unresolved; no unseen-quality claim. No color jitter or random crops.'}
    (args.output/'training_report.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='history'},indent=2),flush=True)


if __name__ == '__main__':
    main()
