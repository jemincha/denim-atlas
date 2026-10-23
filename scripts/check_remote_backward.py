"""Run after check_remote_model.py in the same remote kernel; synthetic smoke check."""

import copy

assert torch.cuda.is_available() and report['model_loaded']
assert report['denim_quality_evaluated'] is False
torch.manual_seed(17)
model.requires_grad_(False)
model.visual.requires_grad_(True)
model.visual.train()
optimizer = torch.optim.AdamW(model.visual.parameters(), lr=1e-5)
scaler = torch.amp.GradScaler('cuda')
optimizer.zero_grad(set_to_none=True)
torch.cuda.reset_peak_memory_stats()
started = time.perf_counter()
with torch.autocast('cuda', dtype=torch.float16):
    features = model.encode_image(batch, normalize=True).float()
    # Arbitrary synthetic objective checks gradients, not denim relevance learning.
    loss = (features[0] - features[1]).square().mean()
assert torch.isfinite(loss).item()
scaler.scale(loss).backward()
scaler.unscale_(optimizer)
gradients = [p.grad for p in model.visual.parameters() if p.grad is not None]
assert gradients and all(torch.isfinite(g).all().item() for g in gradients)
assert any(torch.count_nonzero(g).item() for g in gradients)
scaler.step(optimizer)
scaler.update()
torch.cuda.synchronize()
step_seconds = time.perf_counter() - started
peak_gib = torch.cuda.max_memory_allocated() / 2**30
optimizer.zero_grad(set_to_none=True)

stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
checkpoint = output_dir / ('denim_synthetic_smoke_' + stamp + '.pt')
torch.save({
    'visual': model.visual.state_dict(), 'optimizer': optimizer.state_dict(),
    'scaler': scaler.state_dict(), 'torch_rng': torch.get_rng_state(),
    'cuda_rng': torch.cuda.get_rng_state_all(), 'step': 1,
    'model_revision': revision, 'purpose': 'synthetic smoke check only',
}, checkpoint)
# Deliberately change a parameter and LR, then verify actual restoration.
parameter = next(model.visual.parameters())
expected = parameter.detach().clone()
optimizer_lr = optimizer.param_groups[0]['lr']
scaler_state = copy.deepcopy(scaler.state_dict())
with torch.no_grad():
    parameter.zero_()
optimizer.param_groups[0]['lr'] = 0.1
saved = torch.load(checkpoint, map_location='cpu', weights_only=True)
model.visual.load_state_dict(saved['visual'], strict=True)
optimizer.load_state_dict(saved['optimizer'])
scaler.load_state_dict(saved['scaler'])
torch.set_rng_state(saved['torch_rng'])
torch.cuda.set_rng_state_all(saved['cuda_rng'])
assert torch.equal(parameter, expected)
assert optimizer.param_groups[0]['lr'] == optimizer_lr
assert scaler.state_dict() == scaler_state
assert saved['step'] == 1 and saved['model_revision'] == revision
assert torch.equal(torch.get_rng_state(), saved['torch_rng'])

backward_report = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'revision': revision, 'device': torch.cuda.get_device_name(0),
    'batch_shape': list(batch.shape), 'precision': 'fp32 parameters, fp16 autocast and GradScaler',
    'trainable_parameters': sum(p.numel() for p in model.visual.parameters()),
    'synthetic_loss': loss.item(), 'step_seconds': step_seconds,
    'peak_allocated_gib': peak_gib,
    'backward_verified': True, 'checkpoint_roundtrip_verified': True,
    'checkpoint_bytes': checkpoint.stat().st_size,
    'checkpoint': checkpoint.name,
    'resume_scope': 'same-kernel visual weights, AdamW, scaler, torch RNG; not interrupted-job determinism',
    'denim_training_run': False, 'denim_quality_evaluated': False,
}
target = output_dir / ('denim_backward_check_' + stamp + '.json')
target.write_text(json.dumps(backward_report, indent=2) + chr(10), encoding='utf-8')
assert json.loads(target.read_text())['checkpoint_roundtrip_verified'] is True
print(json.dumps(backward_report, indent=2))
print('Report:', target)
