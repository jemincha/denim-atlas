import json
import platform
from datetime import datetime, timezone
from pathlib import Path

if Path('/kaggle/working').is_dir():
    provider = 'kaggle'
    output_dir = Path('/kaggle/working')
elif Path('/content').is_dir():
    provider = 'colab-compatible'
    output_dir = Path('/content')
else:
    raise RuntimeError('Use the remote Kaggle/Colab runtime, not the laptop.')

import torch
if not torch.cuda.is_available():
    raise RuntimeError('CUDA GPU unavailable. Check the free accelerator setting; no CPU fallback.')

devices = []
for index in range(torch.cuda.device_count()):
    props = torch.cuda.get_device_properties(index)
    devices.append({'index': index, 'name': props.name,
                    'vram_gib': round(props.total_memory / 2**30, 3)})

# Verify a real CUDA operation; multiple GPUs are not pooled as one VRAM space.
with torch.inference_mode():
    probe = torch.ones((8, 8), device='cuda:0')
    assert torch.all(probe @ probe == 8).item()
del probe
torch.cuda.empty_cache()

report = {'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
          'provider': provider, 'python': platform.python_version(),
          'torch': torch.__version__, 'cuda_runtime': torch.version.cuda,
          'devices': devices, 'gpu_operation_verified': True,
          'model_loaded': False, 'training_run': False,
          'account_quota': 'check_provider_UI_separately'}
assert devices and all(device['vram_gib'] > 0 for device in devices)
target = output_dir / ('denim_gpu_check_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
target.write_text(json.dumps(report, indent=2) + chr(10), encoding='utf-8')
assert json.loads(target.read_text(encoding='utf-8'))['gpu_operation_verified'] is True
print(json.dumps(report, indent=2))
print('Report:', target)
