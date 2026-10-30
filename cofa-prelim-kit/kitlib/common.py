import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KST = timezone(timedelta(hours=9))
VERSION = '1.1.0'
IGNORED_DIRS = {'.git', 'node_modules', '__pycache__', '.pytest_cache', '.ruff_cache', '.mypy_cache'}
ROOT_IGNORED_DIRS = {'.cofa', '.cofa-kit', '.venv', '.venv-cofa', '.next', 'dist', 'build', 'coverage'}


def now():
    return datetime.now(KST)


def parse_time(value):
    try:
        t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError) as e:
        raise ValueError('Use ISO date/time with explicit timezone, e.g. 2026-10-31T10:00:00+09:00') from e
    if t.tzinfo is None:
        raise ValueError('Timezone offset is required')
    return t.astimezone(KST)


def read_json(path, default=None):
    if not path.exists():
        if default is not None:
            return default
        raise ValueError('File not found: ' + str(path))
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('x', encoding='utf-8') as handle:
        handle.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    try:
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def safe_path(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Expected a project-relative path: ' + str(relative))
    target = root / rel
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes the project (possibly via symlink): ' + str(relative))
    return target


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def fingerprint(project):
    """Source freshness marker. Known generated/dependency directories are skipped."""
    h = hashlib.sha256()
    for directory, dirs, files in os.walk(project, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS and
                         not (Path(directory) == project and d in ROOT_IGNORED_DIRS) and
                         not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            p = Path(directory) / name
            if p.is_symlink():
                # Link targets can change independently; do not follow them silently.
                h.update(str(p.relative_to(project)).encode('utf-8'))
                h.update(os.readlink(p).encode('utf-8'))
                continue
            h.update(p.relative_to(project).as_posix().encode('utf-8'))
            h.update(bytes.fromhex(sha256(p)))
    return h.hexdigest()


def runtime_path(project, relative):
    p = safe_path(project, '.cofa/' + relative)
    base = project / '.cofa'
    if base.resolve() != base.absolute() or p.is_symlink():
        raise ValueError('Runtime paths must not be symbolic links/junctions')
    return p


def state_path(project):
    return runtime_path(project, 'state.json')


def load_state(project):
    s = read_json(state_path(project))
    if s.get('schema') != 1:
        raise ValueError('Unsupported session schema')
    return s


def ensure_work(project):
    s = load_state(project)
    if s['stage'] not in ('work', 'submission-preview'):
        raise ValueError('Submission is locked / oral stage. No AI work or task mutations through this helper.')
    if now() >= parse_time(s['hard_work_end']):
        raise ValueError('Estimated official work limit has elapsed. Follow platform submission instructions.')
    return s


def ensure_optional_work(project):
    if state_path(project).exists():
        ensure_work(project)


def event(project, kind, data):
    path = runtime_path(project, 'events.jsonl')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps({'at': now().isoformat(), 'kind': kind, **data}, ensure_ascii=False) + '\n')


def verify_bundle(root=ROOT):
    manifest = read_json(root / 'bundle-lock.json')
    errors = []
    for relative, expected in manifest['files'].items():
        p = safe_path(root, relative)
        if not p.is_file():
            errors.append('missing: ' + relative)
        elif p.is_symlink() or sha256(p) != expected:
            errors.append('changed: ' + relative)
    if errors:
        raise ValueError('Bundle integrity failed: ' + '; '.join(errors[:12]))
    return {'ok': True, 'checked_files': len(manifest['files']), 'version': VERSION,
            'scope': 'Checks local manifest consistency, not publisher authenticity.'}
