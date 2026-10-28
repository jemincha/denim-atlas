"""Bounded remote VLM appearance descriptions; outputs are unverified weak labels."""

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time

try:
    from .evaluate import unique_object
except ImportError:
    from evaluate import unique_object


MODEL = 'Qwen/Qwen3-VL-2B-Instruct'
REVISION = '89644892e4d85e24eaac8bacfd4f463576704203'
WEIGHT_SHA256 = '7de1838c87a5349b016c26a1c3f7d2bc400a3d485f95ef39a7059ffd734977a0'
ENUMS = {
    'view':{'front','back','side','mixed','unknown'},
    'color_family':{'blue','gray','black','white','beige','brown','green','pink','red','multicolor','other','unknown'},
    'observed_tone':{'cool','neutral','warm','unknown'},
    'lightness':{'dark','medium','light','mixed','unknown'},
    'fade_strength':{'none','subtle','moderate','strong','unknown'},
    'front_hip_whiskers':{'visible','absent','unknown'},
    'front_thigh_lightening':{'visible','absent','unknown'},
    'knee_lightening':{'visible','absent','unknown'},
    'rips':{'visible','absent','unknown'},
    'detail_readability':{'enough','limited','insufficient'},
}
PROMPT = '''Describe only the visible denim trousers, not the shirt, person or background.
Match the photographed appearance including its lighting. Do not reconstruct original fabric
color, pre-wear condition or manufacturing/washing process. Do not infer unseen details.
If multiple trouser targets are ambiguous, set target_ambiguous true and all visual fields unknown.
Return one JSON object with exactly these fields and values:
target_ambiguous: boolean
view: front/back/side/mixed/unknown
color_family: blue/gray/black/white/beige/brown/green/pink/red/multicolor/other/unknown
observed_tone: cool/neutral/warm/unknown
lightness: dark/medium/light/mixed/unknown
fade_strength: none/subtle/moderate/strong/unknown (apparent light-dark fading only)
front_hip_whiskers: visible/absent/unknown (horizontal faded lines below front pockets)
front_thigh_lightening: visible/absent/unknown
knee_lightening: visible/absent/unknown
rips: visible/absent/unknown
detail_readability: enough/limited/insufficient
Use unknown instead of absent for hidden, cropped or unreadable regions. For a back or
side view, both front_hip_whiskers and front_thigh_lightening must be unknown. If detail is
insufficient, fade_strength and the four detail fields must be unknown. If target_ambiguous
is true, all visual fields must be unknown and detail_readability insufficient.
No confidence numbers, prose, markdown or relevance/similarity scores.'''


def parse_annotation(text):
    value = json.loads(text.strip(),object_pairs_hook=unique_object)
    if not isinstance(value,dict) or set(value)!=set(ENUMS)|{'target_ambiguous'}:
        raise ValueError('Expected exact appearance schema')
    if type(value['target_ambiguous']) is not bool: raise ValueError('Ambiguity must be boolean')
    for field,choices in ENUMS.items():
        if not isinstance(value[field],str) or value[field] not in choices:
            raise ValueError('Unknown enum: '+field)
    front = ['front_hip_whiskers','front_thigh_lightening']
    details = front+['knee_lightening','rips','fade_strength']
    if value['view'] in {'back','side'} and any(value[k]!='unknown' for k in front):
        raise ValueError('Unobserved front details asserted')
    if value['detail_readability']=='insufficient' and any(value[k]!='unknown' for k in details):
        raise ValueError('Unreadable details asserted')
    # Thigh/knee lightening can be illumination; whiskers are explicitly defined as faded lines.
    if value['fade_strength']=='none' and value['front_hip_whiskers']=='visible':
        raise ValueError('Visible fading conflicts with no fading')
    if value['target_ambiguous'] and (value['detail_readability']!='insufficient'
            or any(value[k]!='unknown' for k in ENUMS if k!='detail_readability')):
        raise ValueError('Ambiguous target must remain unknown')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--image-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if not Path('/kaggle/working').is_dir() or args.output.exists():
        parser.error('Remote Kaggle and a new output directory required')
    raw = args.manifest.read_bytes();plan = json.loads(raw,object_pairs_hook=unique_object)
    rows = plan.get('examples',[])
    if not 1<=len(rows)<=24 or len({r['id'] for r in rows})!=len(rows):
        raise ValueError('Pilot requires 1..24 unique reviewed images')
    root=args.image_root.resolve(strict=True);paths=[]
    for row in rows:
        rel=Path(row['file'])
        if rel.is_absolute() or '..' in rel.parts or row.get('usage_scope')!='private_research_reviewed':
            raise ValueError('Reviewed local paths and private research scope required')
        path=(root/rel).resolve(strict=True)
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Image path/hash mismatch')
        paths.append(path)
    import torch
    from huggingface_hub import snapshot_download
    from transformers import AutoProcessor, Qwen3VLForConditionalGeneration
    from PIL import Image, ImageOps
    if not torch.cuda.is_available(): parser.error('CUDA required; no local or CPU model fallback')
    if importlib.metadata.version('transformers')!='5.16.1':raise ValueError('Expected Transformers 5.16.1')
    snapshot=Path(snapshot_download(MODEL,revision=REVISION,
        allow_patterns=['*.json','*.safetensors','*.model','merges.txt','vocab.json','LICENSE','README.md']))
    weights={}
    for path in sorted(snapshot.glob('*.safetensors')):
        with path.open('rb') as stream:weights[path.name]=hashlib.file_digest(stream,'sha256').hexdigest()
    if weights!={'model.safetensors':WEIGHT_SHA256}:raise ValueError('Unexpected pinned model weights')
    processor=AutoProcessor.from_pretrained(snapshot,trust_remote_code=False)
    model=Qwen3VLForConditionalGeneration.from_pretrained(snapshot,dtype=torch.float16,
        attn_implementation='sdpa',trust_remote_code=False).to('cuda:0').eval()
    args.output.mkdir(parents=True,exist_ok=False)
    torch.cuda.reset_peak_memory_stats();started=time.perf_counter();results=[]
    for row,path in zip(rows,paths):
        with Image.open(path) as im:image=ImageOps.exif_transpose(im).convert('RGB')
        messages=[{'role':'user','content':[{'type':'image','image':image},{'type':'text','text':PROMPT}]}]
        inputs=processor.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,
            return_dict=True,return_tensors='pt').to(model.device)
        with torch.inference_mode():generated=model.generate(**inputs,max_new_tokens=320,do_sample=False)
        text=processor.batch_decode(generated[:,inputs['input_ids'].shape[-1]:],skip_special_tokens=True,
            clean_up_tokenization_spaces=False)[0]
        item={'id':row['id'],'image_sha256':row['sha256'],'raw_response':text,
              'status':'unverified_machine_description','human_verified':False}
        try:item['attributes']=parse_annotation(text);item['schema_valid']=True
        except ValueError as error:item['schema_valid']=False;item['error']=str(error)
        results.append(item)
        (args.output/'annotations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'processed':len(results),'schema_valid':item['schema_valid']}),flush=True)
        del inputs,generated
    valid=[r for r in results if r['schema_valid']]
    summary={'schema_version':1,'purpose':'appearance_weak_annotation_feasibility','model':MODEL,
        'revision':REVISION,'model_weight_sha256':weights,'model_license_card':'Apache-2.0; image terms remain separate',
        'images':len(rows),'schema_valid_images':len(valid),'schema_invalid_images':len(rows)-len(valid),
        'unknown_counts':{k:sum(r['attributes'][k]=='unknown' for r in valid) for k in ENUMS},
        'color_counts':dict(Counter(r['attributes']['color_family'] for r in valid)),
        'fade_counts':dict(Counter(r['attributes']['fade_strength'] for r in valid)),
        'manifest_sha256':hashlib.sha256(raw).hexdigest(),'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds_inference':time.perf_counter()-started,
        'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,'device':torch.cuda.get_device_name(0),
        'precision':'float16, sdpa; T4 does not require bfloat16 or FlashAttention',
        'packages':{k:importlib.metadata.version(k) for k in ['torch','transformers','Pillow','huggingface_hub']},
        'human_labels_created':0,'training_performed':False,'ranking_performed':False,
        'limits':'Schema validity and model consistency are not visual-label accuracy. All predictions are unverified weak descriptions; unknown is not negative. Small biased catalog/wearing pilot, limited resolution, no confidence calibration or human agreement claim.'}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps(summary),flush=True)


if __name__ == '__main__':main()
