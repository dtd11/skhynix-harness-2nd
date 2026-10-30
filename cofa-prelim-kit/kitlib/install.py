import os
from .common import ROOT, ensure_optional_work, safe_path, verify_bundle

BEGIN = '<!-- cofa-prelim-kit:begin -->'
END = '<!-- cofa-prelim-kit:end -->'


def managed_text(existing, payload):
    text = existing.decode('utf-8-sig')
    block = BEGIN + '\n' + payload.strip() + '\n' + END
    starts, ends = text.count(BEGIN), text.count(END)
    if starts != ends or starts > 1:
        raise ValueError('Malformed or duplicate COFA managed block; inspect before reinstalling')
    if starts:
        a, b = text.index(BEGIN), text.index(END)
        if b < a:
            raise ValueError('Malformed COFA managed block order')
        text = text[:a] + block + text[b + len(END):]
    else:
        text += ('\n' if text.endswith('\n') or not text else '\n\n') + block + '\n'
    # Existing CRLF outside the managed block is preserved.
    bom = b'\xef\xbb\xbf' if existing.startswith(b'\xef\xbb\xbf') else b''
    return bom + text.encode('utf-8')


def install(project, dry_run=False):
    if not project.is_dir():
        raise ValueError('Project directory must already exist')
    if project == ROOT or project.is_relative_to(ROOT):
        raise ValueError('Choose the actual task project outside the source kit directory')
    ensure_optional_work(project)
    info = verify_bundle()
    import json
    manifest = json.loads((ROOT / 'bundle-lock.json').read_text(encoding='utf-8'))
    writes = {}
    conflicts = []
    # Copy exactly the distributable files, not caches or arbitrary local files.
    for relative in [*manifest['files'], 'bundle-lock.json']:
        source = safe_path(ROOT, relative)
        target = safe_path(project, '.cofa-kit/' + relative)
        if target.exists() and (not target.is_file() or target.read_bytes() != source.read_bytes()):
            conflicts.append(str(target.relative_to(project)))
        writes[target] = source.read_bytes()
    for source_relative in manifest['files']:
        if not source_relative.startswith('skills/'):
            continue
        source = safe_path(ROOT, source_relative)
        relative = source_relative[len('skills/'):]
        target = safe_path(project, '.agents/skills/' + relative)
        if target.exists() and (not target.is_file() or target.read_bytes() != source.read_bytes()):
            conflicts.append(str(target.relative_to(project)))
        writes[target] = source.read_bytes()
    if conflicts:
        raise ValueError('Existing different files were not overwritten: ' + ', '.join(conflicts[:10]))
    for name, payload in [('AGENTS.md', (ROOT / 'assets/AGENTS-block.md').read_text(encoding='utf-8')),
                          ('.gitignore', '.cofa/\n.cofa-kit/\n.venv-cofa/')]:
        target = safe_path(project, name)
        old = target.read_bytes() if target.exists() else b''
        writes[target] = managed_text(old, payload)
    for target in writes:
        if target.with_name(target.name + '.cofa-tmp').exists():
            raise ValueError('Temporary-file conflict; inspect ' + str(target))
    if not dry_run:
        backup = safe_path(project, '.cofa/AGENTS.before-kit.md')
        agents = safe_path(project, 'AGENTS.md')
        if agents.exists() and not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(agents.read_bytes())
        for target, content in writes.items():
            if target.exists() and target.read_bytes() == content:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_name(target.name + '.cofa-tmp')
            if tmp.exists():
                raise ValueError('Temporary-file conflict; inspect ' + str(tmp))
            try:
                with tmp.open('xb') as handle:
                    handle.write(content)
                os.replace(tmp, target)
            finally:
                if tmp.exists():
                    tmp.unlink()
    return {'installed': not dry_run, 'dry_run': dry_run, 'files_planned': len(writes),
            'integrity': info, 'project': str(project),
            'entrypoint': str(project / '.cofa-kit/kit.py'),
            'global_config_changed': False, 'packages_installed': False}
