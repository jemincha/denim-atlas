"""Remote last-block adaptation to weak catalog-cut labels, not overall denim relevance."""

import argparse
from collections import defaultdict
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import random
import time

try:
    from .evaluate import ndcg_at_5
    from .extract_features import REVISION, WEIGHT_SHA256
except ImportError:
    from evaluate import ndcg_at_5
    from extract_features import REVISION, WEIGHT_SHA256


def proxy_metrics(similarities, rows):
    """Each query ranks its fold, excluding itself and linked source families."""
    if len(similarities) != len(rows) or any(len(v)!=len(rows) for v in similarities):
        raise ValueError('Square fold score matrix required')
    classes = defaultdict(list)
    for i,row in enumerate(rows):
        order = sorted((j for j,r in enumerate(rows) if r['source_group']!=row['source_group']),
                       key=lambda j:(-similarities[i][j],rows[j]['image_id']))
        if any(not math.isfinite(v) for v in similarities[i]): raise ValueError('Nonfinite score')
        grades = [int(rows[j]['source_fit']==row['source_fit']) for j in order]
        score = ndcg_at_5(grades)
        if score is None: raise ValueError('Each validation class needs another source group')
        classes[row['source_fit']].append((score,sum(grades[:5])/min(5,len(grades))))
    per_class = {c:{'queries':len(v),'ndcg_at_5':sum(x[0] for x in v)/len(v),
                    'precision_at_5':sum(x[1] for x in v)/len(v)} for c,v in sorted(classes.items())}
    return {'macro_ndcg_at_5':sum(v['ndcg_at_5'] for v in per_class.values())/len(per_class),
            'macro_precision_at_5':sum(v['precision_at_5'] for v in per_class.values())/len(per_class),
            'per_class':per_class}


def batch_triplet_loss(vectors, labels, groups):
    import torch
    scores = vectors @ vectors.T
    positive = (labels[:,None]==labels[None,:]) & (groups[:,None]!=groups[None,:])
    negative = labels[:,None]!=labels[None,:]
    valid = positive[:,:,None] & negative[:,None,:]
    if not valid.any().item(): raise ValueError('No cross-group positive/negative triplets')
    return torch.relu(0.1-scores[:,:,None]+scores[:,None,:])[valid].mean()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acquisition',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--review',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seed',type=int,default=17)
    args = parser.parse_args()
    if not 0 <= args.seed < 2**32: parser.error('seed must be an unsigned 32-bit integer')
    if not Path('/kaggle/working').is_dir() or args.output.exists():
        parser.error('Kaggle execution and a new output directory required')
    raw = args.manifest.read_bytes(); plan = json.loads(raw)
    review = json.loads(args.review.read_text(encoding='utf-8'))
    if (plan.get('purpose')!='weak_source_fit_proxy' or review.get('decision')!='proceed_weak_source_fit'
            or review.get('manifest_sha256')!=hashlib.sha256(raw).hexdigest()):
        raise ValueError('Exact-manifest visual/proxy review required')
    if hashlib.sha256((args.acquisition/'summary.json').read_bytes()).hexdigest()!=plan['summary']['source_summary_sha256']:
        raise ValueError('Acquisition provenance mismatch')
    rows = plan['examples']; owners = {}; by_label = defaultdict(lambda:defaultdict(list))
    for i,r in enumerate(rows):
        if (not r['image_id'].isdecimal() or r['proxy_split'] not in {'train','validation'}
                or r['observed_color'] is not None or r['wash'] is not None):
            raise ValueError('Unexpected fit-only example')
        if owners.setdefault(r['source_group'],r['proxy_split'])!=r['proxy_split']:
            raise ValueError('Source group crosses folds')
        if r['proxy_split']=='train':by_label[r['source_fit']][r['source_group']].append(i)
    if len(by_label)!=5 or any(len(g)<4 for g in by_label.values()):
        raise ValueError('Need five cut classes with at least four training source groups each')
    import torch
    import open_clip
    from huggingface_hub import snapshot_download
    from PIL import Image, ImageOps
    if not torch.cuda.is_available(): parser.error('CUDA required; no local/CPU fallback')
    if importlib.metadata.version('open_clip_torch')!='3.3.0': raise ValueError('Expected OpenCLIP 3.3.0')
    # Analytic self-check: eight valid triplets have mean hinge 0.6, or 0 when aligned.
    x = torch.tensor([[1.,0.],[0.,1.],[1.,0.],[0.,1.]],requires_grad=True)
    y = torch.tensor([0,0,1,1]); g = torch.arange(4)
    check = batch_triplet_loss(x,y,g); assert abs(check.item()-0.6)<1e-6
    check.backward(); assert torch.isfinite(x.grad).all() and x.grad.abs().sum()>0
    aligned = torch.tensor([[1.,0.],[1.,0.],[0.,1.],[0.,1.]])
    assert batch_triplet_loss(aligned,y,g).item()==0
    try: batch_triplet_loss(aligned,torch.zeros(4,dtype=torch.long),g)
    except ValueError: pass
    else: raise AssertionError('Empty triplets must be rejected')
    torch.manual_seed(args.seed);torch.cuda.manual_seed_all(args.seed);rng=random.Random(args.seed)
    snapshot = Path(snapshot_download('Marqo/marqo-fashionSigLIP',revision=REVISION,
        allow_patterns=['open_clip_config.json','open_clip_model.safetensors']))
    with (snapshot/'open_clip_model.safetensors').open('rb') as stream:
        if hashlib.file_digest(stream,'sha256').hexdigest()!=WEIGHT_SHA256:raise ValueError('Base weight mismatch')
    model,_,preprocess = open_clip.create_model_and_transforms('local-dir:'+str(snapshot),device='cuda:0',require_pretrained=True)
    model.eval().requires_grad_(False)
    name = 'visual.trunk.blocks.'+str(len(model.visual.trunk.blocks)-1)
    module = model.get_submodule(name);module.requires_grad_(True)
    optimizer = torch.optim.AdamW(module.parameters(),lr=1e-6,weight_decay=0.01)
    target = model.visual.image_size
    if isinstance(target,int):target=(target,target)
    tensors=[]
    for row in rows:
        path=args.acquisition/'images'/(row['image_id']+'.jpg')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Image checksum mismatch')
        with Image.open(path) as im:
            rgb=ImageOps.exif_transpose(im).convert('RGB')
            if hashlib.sha256(str(rgb.size).encode()+rgb.tobytes()).hexdigest()!=row['pixel_sha256']:
                raise ValueError('Decoded pixel mismatch')
            tensors.append(preprocess(ImageOps.pad(rgb,target,color='white')))
    tensors=torch.stack(tensors)
    labels_sorted=sorted(by_label)
    labels=torch.tensor([labels_sorted.index(r['source_fit']) for r in rows],device='cuda:0')
    group_ids={v:i for i,v in enumerate(sorted(owners))}
    groups=torch.tensor([group_ids[r['source_group']] for r in rows],device='cuda:0')
    def digest():
        h=hashlib.sha256()
        for key,value in module.state_dict().items():
            h.update(key.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()
    def metrics():
        vectors=[]
        with torch.inference_mode():
            for start in range(0,len(rows),16):
                vectors.append(model.encode_image(tensors[start:start+16].cuda(),normalize=True).float().cpu())
        vectors=torch.cat(vectors);assert torch.isfinite(vectors).all()
        values={}
        for fold in ['train','validation']:
            ids=[i for i,r in enumerate(rows) if r['proxy_split']==fold]
            scores=(vectors[ids]@vectors[ids].T).tolist()
            values[fold]=proxy_metrics(scores,[rows[i] for i in ids])
        return values,vectors
    before_hash=digest(); before,base_vectors=metrics()
    print(json.dumps({'step':0,'proxy_metrics':before}),flush=True)
    args.output.mkdir(parents=True,exist_ok=False)
    torch.cuda.reset_peak_memory_stats(); started=time.perf_counter();history=[];validation_history=[]
    for step in range(120):
        ids=[]
        for label in labels_sorted:
            source_groups=by_label[label]
            ids.extend(rng.choice(source_groups[k]) for k in rng.sample(sorted(source_groups),4))
        optimizer.zero_grad(set_to_none=True)
        vectors=model.encode_image(tensors[ids].cuda(),normalize=True).float()
        loss=batch_triplet_loss(vectors,labels[ids],groups[ids]);assert torch.isfinite(loss).item()
        loss.backward();norm=torch.nn.utils.clip_grad_norm_(module.parameters(),1.,error_if_nonfinite=True)
        optimizer.step();history.append({'step':step+1,'loss':loss.item(),'gradient_norm':norm.item()})
        if (step+1)%20==0:
            current,_=metrics();validation_history.append({'step':step+1,'metrics':current})
            print(json.dumps({'step':step+1,'loss':loss.item(),'proxy_metrics':current}),flush=True)
    after,after_vectors=metrics();after_hash=digest();assert after_hash!=before_hash
    checkpoint=args.output/'last_block.pt'
    torch.save({'module':name,'state_dict':module.state_dict(),'optimizer':optimizer.state_dict(),
        'step':120,'base_revision':REVISION,'base_weights_sha256':WEIGHT_SHA256,
        'purpose':'weak_source_fit_proxy','manifest_sha256':hashlib.sha256(raw).hexdigest()},checkpoint)
    saved=torch.load(checkpoint,map_location='cpu',weights_only=True)
    with torch.no_grad():next(module.parameters()).zero_()
    module.load_state_dict(saved['state_dict'],strict=True);assert digest()==after_hash
    torch.save({'image_ids':[r['image_id'] for r in rows],'before':base_vectors,'after':after_vectors},args.output/'vectors.pt')
    report={'schema_version':1,'purpose':'weak_source_fit_proxy','overall_similarity_evaluated':False,
        'human_labels_used':False,'training_images':sum(r['proxy_split']=='train' for r in rows),
        'validation_images':sum(r['proxy_split']=='validation' for r in rows),'source_summary':plan['summary'],
        'steps':120,'batch_size':20,'groups_per_class_per_batch':4,'seed':args.seed,'precision':'fp32',
        'learning_rate':1e-6,'weight_decay':0.01,'cosine_margin':0.1,
        'loss':'Mean hinge over all cross-source-group positive / other-cut negative triplets in a balanced batch',
        'base_revision':REVISION,'base_weights_sha256':WEIGHT_SHA256,'trained_module':name,
        'trainable_parameters':sum(p.numel() for p in module.parameters()),'before':before,'after':after,
        'validation_history':validation_history,'history':history,'module_sha256_before':before_hash,
        'module_sha256_after':after_hash,'checkpoint_sha256':hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        'checkpoint_bytes':checkpoint.stat().st_size,'checkpoint_roundtrip_verified':True,
        'loss_analytic_self_check_passed':True,'manifest_sha256':hashlib.sha256(raw).hexdigest(),
        'review_sha256':hashlib.sha256(args.review.read_bytes()).hexdigest(),
        'training_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'seconds_training_validation_save':time.perf_counter()-started,
        'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,'device':torch.cuda.get_device_name(0),
        'packages':{k:importlib.metadata.version(k) for k in ['torch','open_clip_torch','timm','Pillow']},
        'preprocessing':'Fixed white letterbox; original color; no random crop or color jitter; dropout remains disabled',
        'selection':'Final step 120 fixed before results; no test or human-query tuning',
        'limits':'Catalog-cut proxy labels only, not human-verified silhouette or overall appearance. Validation excludes known source families, not certified independent products. No color/wash learning claim; no pristine test set.'}
    (args.output/'training_report.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['history','validation_history']},indent=2),flush=True)


if __name__ == '__main__': main()
