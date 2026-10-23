"""Remote-only model loading check; synthetic inputs do not evaluate denim retrieval."""

import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

if Path('/kaggle/working').is_dir():
    output_dir = Path('/kaggle/working')
elif Path('/content').is_dir():
    output_dir = Path('/content')
else:
    raise RuntimeError('Run on the remote GPU, not the laptop.')

import torch

if not torch.cuda.is_available():
    raise RuntimeError('CUDA unavailable; no CPU fallback.')

subprocess.run(
    [sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check',
     'open_clip_torch==3.3.0'], check=True,
)

import open_clip
from huggingface_hub import HfApi, snapshot_download
from PIL import Image

repo_id = 'Marqo/marqo-fashionSigLIP'
# Resolve this published commit once; every downloaded file uses its full SHA.
revision = HfApi().model_info(repo_id, revision='c56244c').sha
assert revision and len(revision) == 40
print('Model revision:', revision, flush=True)
snapshot = Path(snapshot_download(
    repo_id, revision=revision,
    allow_patterns=['open_clip_config.json', 'open_clip_model.safetensors'],
    cache_dir=str(output_dir / 'hf_cache'),
))
weights = snapshot / 'open_clip_model.safetensors'
assert weights.is_file() and weights.stat().st_size > 0
with weights.open('rb') as stream:
    weight_sha256 = hashlib.file_digest(stream, 'sha256').hexdigest()
config = json.loads((snapshot / 'open_clip_config.json').read_text())
assert config['model_cfg']['embed_dim'] == 768
assert config['model_cfg']['vision_cfg']['image_size'] == 224

model, _, preprocess = open_clip.create_model_and_transforms(
    'local-dir:' + str(snapshot), device='cuda:0', require_pretrained=True,
)
model.eval()
# No external image upload is needed to check the tensor and model execution path.
batch = torch.stack([
    preprocess(Image.new('RGB', (224, 224), color))
    for color in [(40, 65, 100), (90, 110, 135)]
]).to('cuda:0')
assert batch.shape == (2, 3, 224, 224)
with torch.inference_mode(), torch.autocast('cuda', dtype=torch.float16):
    model.encode_image(batch, normalize=True)  # warm-up
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    embeddings = model.encode_image(batch, normalize=True).float()
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - started
assert embeddings.shape == (2, 768) and torch.isfinite(embeddings).all().item()
assert torch.allclose(embeddings.norm(dim=-1), torch.ones(2, device='cuda:0'), atol=0.01)

report = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'repo_id': repo_id, 'revision': revision, 'weights_sha256': weight_sha256,
    'python': platform.python_version(),
    'packages': {name: importlib.metadata.version(name) for name in
                 ['torch', 'torchvision', 'open_clip_torch', 'timm', 'huggingface_hub', 'safetensors', 'Pillow']},
    'cuda_runtime': torch.version.cuda, 'device': torch.cuda.get_device_name(0),
    'batch_shape': list(batch.shape), 'embedding_shape': list(embeddings.shape),
    'forward_seconds_after_warmup': elapsed,
    'peak_allocated_gib': torch.cuda.max_memory_allocated() / 2**30,
    'input': 'two synthetic solid-color images; not a retrieval evaluation',
    'model_loaded': True, 'training_run': False, 'denim_quality_evaluated': False,
}
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
target = output_dir / ('denim_model_check_' + stamp + '.json')
target.write_text(json.dumps(report, indent=2) + chr(10), encoding='utf-8')
assert json.loads(target.read_text())['model_loaded'] is True
freeze = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], check=True, capture_output=True, text=True)
(output_dir / ('denim_environment_' + stamp + '.txt')).write_text(freeze.stdout, encoding='utf-8')
print(json.dumps(report, indent=2))
print('Report:', target)
