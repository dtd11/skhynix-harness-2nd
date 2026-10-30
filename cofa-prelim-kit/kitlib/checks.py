import subprocess
import time
from .common import ensure_work, event, fingerprint, now, read_json, runtime_path, write_json
from .process import run_local


def store_evidence(project, item):
    ensure_work(project)
    path = runtime_path(project, 'evidence.json')
    items = read_json(path, [])
    item['id'] = 'E' + str(len(items) + 1)
    items.append(item)
    write_json(path, items)
    event(project, 'evidence', {'id': item['id'], 'name': item['name'], 'result': item['result']})
    return item


def run_check(project, name, command, timeout):
    ensure_work(project)
    if not command or timeout <= 0 or not name.strip():
        raise ValueError('Check needs a nonblank name, a command and a positive timeout')
    # Command execution is explicit, shell-free and local. This is not an OS sandbox:
    # the participant must only pass commands permitted by the competition.
    before = fingerprint(project)
    logdir = runtime_path(project, 'logs')
    logdir.mkdir(parents=True, exist_ok=True)
    count = len(read_json(runtime_path(project, 'evidence.json'), [])) + 1
    logpath = runtime_path(project, f'logs/check-{count}.log')
    began = time.monotonic()
    result = 'fail'
    with logpath.open('wb') as log:
        try:
            code, result = run_local(project, command, log, subprocess.STDOUT, timeout)
        except OSError as exc:
            log.write((str(exc) + '\n').encode('utf-8'))
            code = 127
    if result in ('stage-interrupted', 'deadline-expired'):
        return {'name': name, 'result': result, 'exit_code': code, 'recorded': False,
                'log': str(logpath.resolve()),
                'notice': 'Child stopped after local stage/deadline transition; partial log only, no verification evidence.'}
    # Recheck before evidence writes if state changed just after the child exited.
    ensure_work(project)
    after = fingerprint(project)
    return store_evidence(project, {'name': name, 'type': 'executed-command',
                          'command': command, 'result': result, 'exit_code': code,
                          'at': now().isoformat(), 'duration_seconds': round(time.monotonic() - began, 3),
                          'snapshot_before': before, 'snapshot_after': after,
                          'stable_snapshot': before == after, 'log': str(logpath.resolve())})


def manual(project, name, result, note):
    ensure_work(project)
    if not note.strip() or not name.strip():
        raise ValueError('Manual evidence needs a nonblank name and the participant observation')
    stamp = fingerprint(project)
    return store_evidence(project, {'name': name, 'type': 'participant-attestation',
                          'result': result, 'note': note, 'at': now().isoformat(),
                          'snapshot_before': stamp, 'snapshot_after': stamp,
                          'stable_snapshot': True,
                          'notice': 'Participant-reported; no browser or GUI automation was executed.'})
