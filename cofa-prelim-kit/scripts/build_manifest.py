"""Rebuild the public distribution file manifest after intentional changes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
skip = {'.git', '__pycache__', '.cofa', '.cofa-kit', 'node_modules', '.venv-cofa'}
files = {}
for p in sorted(root.rglob('*')):
    if not p.is_file() or p.name == 'bundle-lock.json' or any(x in skip for x in p.relative_to(root).parts):
        continue
    if p.is_symlink():
        raise SystemExit('Do not publish symlinks: ' + str(p))
    files[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
(root / 'bundle-lock.json').write_text(json.dumps({'algorithm': 'sha256', 'files': files}, indent=2) + '\n', encoding='utf-8')
print('Manifest:', len(files), 'files')
