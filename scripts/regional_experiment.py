"""Remote-only frozen-region features and two-head teacher-distillation pilot."""

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import time

try:
    from .extract_features import REVISION, WEIGHT_SHA256
    from .regional_supervision import AXES, import_preferences
except ImportError:
    from extract_features import REVISION, WEIGHT_SHA256
    from regional_supervision import AXES, import_preferences


CONFIG = {'seed': 37, 'projection_dim': 64, 'steps': 200, 'learning_rate': 0.0003,
          'weight_decay': 0.01, 'cosine_margin': 0.05, 'tie_tolerance': 0.02}


def validate_cache(cache, inputs):
    provenance = cache['provenance']
    if (cache.get('schema_version') != 1 or provenance['packet_sha256'] != inputs['packet_sha256']
            or provenance['base_revision'] != REVISION or provenance['weights_sha256'] != WEIGHT_SHA256):
        raise ValueError('Feature/model provenance mismatch')
    if set(cache['observations']) != {r['id'] for r in inputs['observations']}:
        raise ValueError('Feature observation set mismatch')
    for row in inputs['observations']:
        item = cache['observations'][row['id']]
        if set(item) != {'garment', 'hip_thigh'}:
            raise ValueError('Missing corresponding regional features')
        for name, feature in item.items():
            values = feature['embedding']
            if (feature['crop_sha256'] != row['regions'][name]['sha256'] or len(values) != 768
                    or any(type(v) not in (int, float) or not math.isfinite(v) for v in values)
                    or abs(sum(v*v for v in values) - 1) > 0.002):
                raise ValueError('Invalid pinned regional feature')


def preference_report(similarities, constraints):
    """Score each fold/axis without converting relative preferences to graded relevance."""
    rows = []
    for row, (score_a, score_b) in zip(constraints, similarities, strict=True):
        if not all(math.isfinite(v) for v in (score_a, score_b)):
            raise ValueError('Non-finite similarity')
        delta = score_a - score_b
        target = row['target']
        if target not in {'A', 'B', 'tie'}:
            raise ValueError('Only usable preferences can be scored')
        signed = delta if target == 'A' else -delta if target == 'B' else None
        loss = abs(delta) if signed is None else max(0, CONFIG['cosine_margin'] - signed)
        rows.append({'case_id': row['case_id'], 'axis': row['axis'], 'split': row['split'],
                     'target': target, 'similarity_a': score_a, 'similarity_b': score_b,
                     'signed_margin': signed, 'loss': loss,
                     'strict_correct': None if signed is None else signed > 1e-6,
                     'tie_satisfied': abs(delta) <= CONFIG['tie_tolerance'] if target == 'tie' else None})
    summary = {}
    for fold in ('train', 'development'):
        summary[fold] = {}
        for axis in AXES:
            part = [r for r in rows if r['split'] == fold and r['axis'] == axis]
            strict = [r for r in part if r['target'] != 'tie']
            summary[fold][axis] = {'constraints': len(part), 'strict_comparisons': len(strict),
                'strict_correct': sum(r['strict_correct'] for r in strict),
                'preference_agreement': sum(r['strict_correct'] for r in strict)/len(strict) if strict else None,
                'mean_loss': sum(r['loss'] for r in part)/len(part) if part else None,
                'mean_signed_margin': sum(r['signed_margin'] for r in strict)/len(strict) if strict else None,
                'ties': sum(r['target'] == 'tie' for r in part),
                'ties_satisfied': sum(r['tie_satisfied'] is True for r in part)}
    return {'summary': summary, 'comparisons': rows}


def extract(inputs, root):
    import torch
    import open_clip
    from huggingface_hub import snapshot_download
    from PIL import Image, ImageOps

    if not torch.cuda.is_available() or importlib.metadata.version('open_clip_torch') != '3.3.0':
        raise RuntimeError('Requires remote CUDA and open_clip_torch==3.3.0')
    snapshot = Path(snapshot_download('Marqo/marqo-fashionSigLIP', revision=REVISION,
        allow_patterns=['open_clip_config.json', 'open_clip_model.safetensors']))
    if hashlib.sha256((snapshot/'open_clip_model.safetensors').read_bytes()).hexdigest() != WEIGHT_SHA256:
        raise ValueError('Unexpected backbone checksum')
    model, _, preprocess = open_clip.create_model_and_transforms(
        'local-dir:' + str(snapshot), device='cuda:0', require_pretrained=True)
    model.eval().requires_grad_(False)
    target = model.visual.image_size
    if isinstance(target, int):
        target = (target, target)
    features = {}
    for row in inputs['observations']:
        features[row['id']] = {}
        for name, region in row['regions'].items():
            path = root/region['file']
            if hashlib.sha256(path.read_bytes()).hexdigest() != region['sha256']:
                raise ValueError('Crop changed during extraction')
            with Image.open(path) as source:
                image = ImageOps.exif_transpose(source).convert('RGB')
                tensor = preprocess(ImageOps.pad(image, target, color='white')).unsqueeze(0).cuda()
            with torch.inference_mode(), torch.autocast('cuda', dtype=torch.float16):
                vector = model.encode_image(tensor, normalize=True).float()[0].cpu().tolist()
            features[row['id']][name] = {'embedding': vector, 'crop_sha256': region['sha256']}
    cache = {'schema_version': 1, 'observations': features, 'provenance': {
        'packet_sha256': inputs['packet_sha256'], 'base_revision': REVISION,
        'weights_sha256': WEIGHT_SHA256, 'device': torch.cuda.get_device_name(0),
        'preprocessing': 'EXIF RGB -> white aspect-preserving pad -> pinned OpenCLIP transform; no color jitter',
        'transform': repr(preprocess), 'encoder_precision': 'CUDA autocast fp16; normalized vectors stored fp32',
        'packages': {key: importlib.metadata.version(key) for key in
                     ['torch', 'torchvision', 'open_clip_torch', 'timm', 'Pillow', 'huggingface_hub']}}}
    validate_cache(cache, inputs)
    del model
    torch.cuda.empty_cache()
    return cache


def adapt(inputs, cache, output):
    import torch
    from torch import nn
    from torch.nn import functional as F

    validate_cache(cache, inputs)
    torch.manual_seed(CONFIG['seed'])
    torch.use_deterministic_algorithms(True)
    ids = [r['id'] for r in inputs['observations']]
    index = {key: i for i, key in enumerate(ids)}
    constraints = inputs['constraints']
    device = 'cuda:0'
    garment = torch.tensor([cache['observations'][key]['garment']['embedding'] for key in ids], device=device)
    region = torch.tensor([cache['observations'][key]['hip_thigh']['embedding'] for key in ids], device=device)
    features = {'silhouette': garment, 'surface': F.normalize(torch.cat((garment, region), dim=1), dim=1)}
    heads = nn.ModuleDict({axis: nn.Linear(value.shape[1], CONFIG['projection_dim'], bias=False)
                           for axis, value in features.items()}).to(device)
    optimizer = torch.optim.AdamW(heads.parameters(), lr=CONFIG['learning_rate'], weight_decay=CONFIG['weight_decay'])

    def similarities(vectors):
        pairs = []
        for row in constraints:
            v = vectors[row['axis']]
            anchor = v[index[row['reference']]]
            pairs.append(((anchor*v[index[row['candidate_a']]]).sum(),
                          (anchor*v[index[row['candidate_b']]]).sum()))
        return pairs

    def metrics(vectors):
        with torch.no_grad():
            pairs = [(a.item(), b.item()) for a, b in similarities(vectors)]
        return preference_report(pairs, constraints)

    def projected():
        return {axis: F.normalize(heads[axis](value), dim=1) for axis, value in features.items()}

    # Dev features are frozen inputs; only train decisions enter the loss below.
    def objective(pairs):
        axis_losses = []
        for axis in AXES:
            losses = []
            for row, (a, b) in zip(constraints, pairs, strict=True):
                if row['split'] != 'train' or row['axis'] != axis:
                    continue
                delta = a-b
                if row['target'] == 'tie':
                    losses.append(delta.abs())
                else:
                    sign = 1 if row['target'] == 'A' else -1
                    losses.append(F.relu(CONFIG['cosine_margin']-sign*delta))
            if not losses:
                raise ValueError('Each head needs training supervision')
            axis_losses.append(torch.stack(losses).mean())
        return torch.stack(axis_losses).mean()

    before = {key: tensor.detach().clone() for key, tensor in heads.state_dict().items()}
    reports = {'E0_garment': metrics({'silhouette': garment, 'surface': garment}),
               'E1_regional': metrics(features), 'E2_initial_projection': metrics(projected())}
    initial_loss = objective(similarities(projected())).item()
    guard_pairs = similarities(projected())
    dev_scores = [value for row, pair in zip(constraints, guard_pairs, strict=True)
                  if row['split'] == 'development' for value in pair]
    guard_gradients = torch.autograd.grad(objective(guard_pairs), dev_scores, allow_unused=True)
    if any(value is not None for value in guard_gradients):
        raise RuntimeError('Development scores enter the training objective')
    history = []
    for step in range(CONFIG['steps']):
        optimizer.zero_grad(set_to_none=True)
        loss = objective(similarities(projected()))
        if not torch.isfinite(loss):
            raise ValueError('Non-finite training loss')
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(heads.parameters(), 1, error_if_nonfinite=True)
        optimizer.step()
        if (step+1) % 20 == 0:
            history.append({'step': step+1, 'train_loss_before_step': loss.item(), 'gradient_norm': norm.item()})
    reports['E2_trained_projection'] = metrics(projected())
    final_loss = objective(similarities(projected())).item()
    changed = any(not torch.equal(before[key], value) for key, value in heads.state_dict().items())
    if not changed:
        raise RuntimeError('No head parameters changed')
    state = {key: value.detach().cpu() for key, value in heads.state_dict().items()}
    checkpoint = output/'regional_heads.pt'
    torch.save({'state_dict': state, 'config': CONFIG, 'packet_sha256': inputs['packet_sha256'],
                'base_revision': REVISION, 'weights_sha256': WEIGHT_SHA256,
                'purpose': 'machine_teacher_distillation_only'}, checkpoint)
    restored = torch.load(checkpoint, map_location=device, weights_only=True)
    for layer in heads.values():
        nn.init.zeros_(layer.weight)
    heads.load_state_dict(restored['state_dict'], strict=True)
    if metrics(projected()) != reports['E2_trained_projection']:
        raise RuntimeError('Checkpoint restoration changed predictions')
    return {'experiments': reports, 'initial_train_loss': initial_loss, 'final_train_loss': final_loss,
            'config': CONFIG, 'trainable_parameters': sum(p.numel() for p in heads.parameters()),
            'checkpoint_sha256': hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
            'checkpoint_roundtrip_verified': True, 'development_loss_gradient_guard': True,
            'parameters_changed': changed, 'history': history}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not Path('/kaggle/working').is_dir():
        parser.error('Run on Kaggle CUDA; no model/training fallback on the laptop')
    os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
    packet = json.loads((args.inputs/'packet.json').read_text())
    ratings = json.loads((args.inputs/'teacher_ratings.json').read_text())
    inputs = import_preferences(packet, ratings, args.inputs)
    if not inputs['ready_for_pilot']:
        parser.error('Pilot supervision gate not met')
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    cache = extract(inputs, args.inputs)
    (args.output/'features.json').write_text(json.dumps(cache, allow_nan=False))
    encoding_seconds = time.perf_counter()-start
    result = adapt(inputs, cache, args.output)
    result.update(schema_version=1, purpose='machine_teacher_distillation_only',
                  independent_quality_evidence=False, packet_sha256=inputs['packet_sha256'],
                  teacher_export_sha256=inputs['export_sha256'], teacher=inputs['teacher'],
                  feature_provenance=cache['provenance'], encoding_seconds=encoding_seconds,
                  total_seconds=time.perf_counter()-start,
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  selection='Fixed final step200; no development-driven checkpoint or parameter selection',
                  limits='Only3 development anchors per axis, machine labels and selected catalog-heavy material. '
                         'Teacher reproduction, not human quality or general-model superiority.')
    (args.output/'report.json').write_text(json.dumps(result, indent=2, allow_nan=False))
    print(json.dumps({key: value for key, value in result.items() if key not in {'experiments', 'history'}}, indent=2))
    print(json.dumps({name: value['summary'] for name, value in result['experiments'].items()}, indent=2))


if __name__ == '__main__':
    main()
