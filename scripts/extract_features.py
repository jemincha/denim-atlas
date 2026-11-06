"""Remote frozen feature extraction from usage-approved, reviewed garment crops."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform

try:
    from .evaluate import identifier, unique_object
except ImportError:
    from evaluate import identifier, unique_object


REVISION = 'c56244cc94f92419e8369fa71efdaf403b124ce8'
WEIGHT_SHA256 = '88908200434959fa3154ef79d408aac33341e8797fe5ca8ca6f0463aab32e6b3'
ENCODERS = {
    'fashion-siglip': {'model': 'Marqo/marqo-fashionSigLIP', 'revision': REVISION,
                       'weight_file': 'open_clip_model.safetensors',
                       'weights_sha256': WEIGHT_SHA256, 'dimension': 768},
    'clip': {'model': 'openai/clip-vit-base-patch32',
             'revision': '3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268',
             'weight_file': 'pytorch_model.bin',
             'weights_sha256': 'a63082132ba4f97a80bea76823f544493bffa8082296d62d71581a4feff1576f',
             'dimension': 512},
    'dinov2': {'model': 'facebook/dinov2-small',
               'revision': 'ed25f3a31f01632728cabb09d1542f84ab7b0056',
               'weight_file': 'model.safetensors',
               'weights_sha256': 'ae1e99fcefd534ed978cdeb8326f08030c96e28b7a81ffcbc98a857c84d14be1',
               'dimension': 384},
}


def frozen_profile(provenance):
    """Accept recorded legacy Marqo features, never unpinned or adapted features."""
    name = provenance.get('encoder', 'Marqo/marqo-fashionSigLIP')
    profile = next((p for p in ENCODERS.values() if p['model'] == name), None)
    if (profile is None or provenance.get('training_run') is not False
            or any(provenance.get(k) != profile[k] for k in ('revision', 'weights_sha256'))):
        raise ValueError('Expected a pinned frozen encoder')
    return profile


def reviewed_crops(manifest, root):
    """Validate all paths and approvals before any model download or image encoding."""
    if (not isinstance(manifest, dict) or type(manifest.get('schema_version')) is not int
            or manifest['schema_version'] != 1):
        raise ValueError('Expected crop manifest schema_version 1')
    rows = manifest.get('assets')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Expected nonempty crop assets')
    root = root.resolve(strict=True)
    result, seen = [], set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Crop records must be objects')
        asset_id = identifier(row.get('id'))
        if asset_id in seen:
            raise ValueError('Duplicate crop ID: ' + asset_id)
        seen.add(asset_id)
        if (row.get('usage_status') != 'approved' or row.get('denim_status') != 'confirmed'
                or row.get('crop_status') != 'reviewed'):
            raise ValueError('Image usage, denim and crop review required: ' + asset_id)
        relative = Path(identifier(row.get('crop_file')))
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Crop path must stay within image root')
        path = (root / relative).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Invalid crop path')
        expected = row.get('crop_sha256')
        with path.open('rb') as stream:
            checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
        if checksum != expected:
            raise ValueError('Crop checksum mismatch: ' + asset_id)
        result.append((asset_id, path, checksum))
    return result


def mean_rgb(image):
    from PIL import ImageStat
    if image.mode != 'RGB':
        raise ValueError('Reviewed crop must be opaque RGB')
    return [value / 255 for value in ImageStat.Stat(image).mean]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--image-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New feature JSON file')
    parser.add_argument('--encoder', choices=sorted(ENCODERS), default='fashion-siglip')
    parser.add_argument('--pad-to-square', action='store_true',
                        help='Use the same full-garment 224 square for the frozen comparison')
    args = parser.parse_args()
    if not (Path('/kaggle/working').is_dir() or Path('/content').is_dir()):
        parser.error('Model extraction runs on remote Kaggle/Colab, not the laptop')
    if args.output.exists():
        parser.error('Output already exists')
    raw = args.manifest.read_bytes()
    crops = reviewed_crops(json.loads(raw, object_pairs_hook=unique_object), args.image_root)
    import torch
    import open_clip
    from huggingface_hub import snapshot_download
    from PIL import Image, ImageOps

    if not torch.cuda.is_available():
        parser.error('CUDA unavailable; no CPU fallback')
    profile = ENCODERS[args.encoder]
    if args.encoder == 'fashion-siglip' and importlib.metadata.version('open_clip_torch') != '3.3.0':
        parser.error('Install open_clip_torch==3.3.0 in the remote runtime first')
    snapshot = Path(snapshot_download(profile['model'], revision=profile['revision'],
                    allow_patterns=['open_clip_config.json', 'config.json',
                                    'preprocessor_config.json', profile['weight_file']]))
    with (snapshot / profile['weight_file']).open('rb') as stream:
        weight_checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
    if weight_checksum != profile['weights_sha256']:
        raise ValueError('Unexpected model weights checksum')
    if args.encoder == 'fashion-siglip':
        model, _, preprocess = open_clip.create_model_and_transforms(
            'local-dir:' + str(snapshot), device='cuda:0', require_pretrained=True)
        encode = lambda tensor: model.encode_image(tensor, normalize=True)
    else:
        from transformers import AutoImageProcessor, AutoModel, CLIPVisionModelWithProjection
        if importlib.metadata.version('transformers') != '5.16.1':
            parser.error('Requires transformers==5.16.1')
        processor = AutoImageProcessor.from_pretrained(snapshot, trust_remote_code=False)
        kind = CLIPVisionModelWithProjection if args.encoder == 'clip' else AutoModel
        # Official CLIP publishes .bin; verify it above and use restricted tensor loading.
        model = kind.from_pretrained(snapshot, trust_remote_code=False,
                                     weights_only=True).to('cuda:0')
        preprocess = lambda image: processor(images=image, return_tensors='pt')['pixel_values'][0]
        encode = lambda tensor: (model(pixel_values=tensor).image_embeds if args.encoder == 'clip'
                                 else model(pixel_values=tensor).last_hidden_state[:, 0])
    model.eval().requires_grad_(False)
    observations = {}
    for asset_id, path, checksum in crops:
        # Detect changed inputs after preflight; the manifest pins the reviewed crop bytes.
        with path.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != checksum:
                raise ValueError('Crop changed during extraction: ' + asset_id)
        with Image.open(path) as source:
            image = ImageOps.exif_transpose(source)
            rgb = mean_rgb(image)
            # A complete-garment square prevents model-specific center crops removing hems.
            prepared = ImageOps.pad(image, (224, 224), color='white') if args.pad_to_square else image
            tensor = preprocess(prepared).unsqueeze(0).to('cuda:0')
        with torch.inference_mode(), torch.autocast('cuda', dtype=torch.float16):
            embedding = torch.nn.functional.normalize(encode(tensor).float(), dim=-1)
        if embedding.shape != (1, profile['dimension']) or not torch.isfinite(embedding).all().item():
            raise ValueError('Invalid embedding: ' + asset_id)
        observations[asset_id] = {'embedding': embedding[0].cpu().tolist(),
                                  'mean_rgb': rgb, 'crop_sha256': checksum}
    result = {'schema_version': 1, 'assets': observations, 'provenance': {
        'encoder': profile['model'], 'revision': profile['revision'],
        'weights_sha256': weight_checksum, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
        'python': platform.python_version(), 'device': torch.cuda.get_device_name(0),
        'cuda_runtime': torch.version.cuda,
        'packages': {name: importlib.metadata.version(name) for name in
                     ['torch', 'torchvision', 'open_clip_torch', 'timm', 'huggingface_hub', 'Pillow']},
        'preprocess': repr(preprocess) if args.encoder == 'fashion-siglip' else repr(processor),
        'input_policy': ('EXIF RGB -> white aspect-preserving 224 square -> official model preprocessing'
                         if args.pad_to_square else 'EXIF RGB -> official model preprocessing'),
        'batch_size': 1,
        'color': 'mean of all pixels in EXIF-oriented reviewed RGB crop, divided by 255',
        'training_run': False}}
    with args.output.open('x', encoding='utf-8') as output:
        output.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print('Frozen features written:', args.output)


if __name__ == '__main__':
    main()
