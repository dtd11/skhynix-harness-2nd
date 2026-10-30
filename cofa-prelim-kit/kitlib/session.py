from datetime import timedelta
from .common import (ROOT, ensure_work, event, fingerprint, load_state, now, parse_time,
                     read_json, runtime_path, safe_path, state_path, write_json)


def start(project, started_at=None, overall_end=None, practice=False, kind='generic'):
    if state_path(project).exists():
        raise ValueError('Session already exists; timers cannot be reset. Use a separate practice directory.')
    rules = read_json(ROOT / 'config/exam.json')
    started = parse_time(started_at) if started_at else now()
    end = parse_time(overall_end) if overall_end else (
        started + timedelta(minutes=240) if practice else parse_time(rules['overall_end']))
    if started >= end:
        raise ValueError('Task start must precede overall end')
    hard = min(started + timedelta(minutes=rules['work_minutes']), end)
    confirm = min(hard, end - timedelta(minutes=rules['oral_minutes'] + rules['recommended_generation_reserve_minutes']))
    begin = confirm - timedelta(minutes=rules['recommended_submission_margin_minutes'])
    s = {'schema': 1, 'stage': 'work', 'kind': kind, 'practice': practice,
         'started_at': started.isoformat(), 'overall_end': end.isoformat(),
         'hard_work_end': hard.isoformat(), 'recommended_confirm_by': confirm.isoformat(),
         'recommended_submission_begin': begin.isoformat(),
         'oral_minutes': rules['oral_minutes'],
         'recommended_generation_reserve_minutes': rules['recommended_generation_reserve_minutes']}
    write_json(state_path(project), s)
    write_json(runtime_path(project, 'requirements.json'), [])
    event(project, 'start', {'practice': practice})
    return {**s, 'notice': 'Local estimates only. Enter actual platform task-start time; this command does not start or control the exam.'}


def evidence(project, stamp=None):
    current = stamp or fingerprint(project)
    items = []
    for e in read_json(runtime_path(project, 'evidence.json'), []):
        items.append({**e, 'fresh': e['snapshot_after'] == current and e['stable_snapshot']})
    return items


def status(project, as_of=None):
    s = load_state(project)
    t = parse_time(as_of) if as_of else now()
    def remaining(key):
        return round((parse_time(s[key]) - t).total_seconds() / 60, 2)
    warnings = []
    if parse_time(s['recommended_confirm_by']) < parse_time(s['started_at']):
        warnings.append('Late start: recommended oral/preparation reserve no longer fits.')
    if t < parse_time(s['started_at']):
        warnings.append('The recorded start is in the future; check it against the platform timer.')
    if t >= parse_time(s['overall_end']):
        phase = 'overall-ended'
    elif s['stage'] in ('locked', 'oral', 'finished'):
        phase = s['stage']
    elif remaining('hard_work_end') <= 0:
        phase = 'work-expired'
    elif t >= parse_time(s['recommended_submission_begin']):
        phase = 'handoff'
    elif remaining('recommended_confirm_by') <= 30:
        phase = 'stabilize'
    else:
        phase = 'implement'
    return {**s, 'as_of': t.isoformat(), 'phase': phase,
            'hard_work_remaining_minutes': remaining('hard_work_end'),
            'recommended_work_remaining_minutes': remaining('recommended_confirm_by'),
            'overall_remaining_minutes': remaining('overall_end'), 'warnings': warnings,
            'requirements': read_json(runtime_path(project, 'requirements.json'), []),
            'evidence': evidence(project),
            'notice': 'Platform timer and current official instructions are authoritative. Preparation reserve is a recommendation, not a guarantee.'}


def stage(project, target):
    s = load_state(project)
    allowed = {'work': {'submission-preview', 'locked'},
               'submission-preview': {'work', 'locked'},
               'locked': {'oral', 'finished'}, 'oral': {'finished'}, 'finished': set()}
    if target not in allowed[s['stage']]:
        raise ValueError('Invalid stage transition: ' + s['stage'] + ' -> ' + target)
    # Merely record what the participant already did in the platform.
    s['stage'] = target
    write_json(state_path(project), s)
    event(project, 'stage', {'stage': target})
    return {'stage': target, 'platform_action_performed': False,
            'ai_work_allowed': target in ('work', 'submission-preview')}


def require(project, rid, text=None, priority=None, state=None, evidence_ids=None):
    ensure_work(project)
    if not rid or not rid.strip():
        raise ValueError('Requirement ID must not be blank')
    p = runtime_path(project, 'requirements.json')
    items = read_json(p, [])
    item = next((r for r in items if r['id'] == rid), None)
    if item is None:
        if not text or not text.strip():
            raise ValueError('A new requirement needs --text')
        item = {'id': rid, 'text': text, 'priority': priority or 'must', 'status': 'todo', 'evidence': []}
        items.append(item)
    elif text:
        item['text'] = text
        item['status'] = 'todo'
        item['evidence'] = []
    if priority is not None:
        item['priority'] = priority
    if evidence_ids is not None:
        item['evidence'] = evidence_ids
    if state == 'verified':
        passing = {e['id'] for e in evidence(project) if e['fresh'] and e['result'] == 'pass'}
        if not item['evidence'] or any(x not in passing for x in item['evidence']):
            raise ValueError('Verified requires linked, passing, current evidence IDs')
    if state:
        item['status'] = state
    write_json(p, items)
    event(project, 'requirement', {'id': rid, 'status': item['status']})
    return item


def note(project, kind, text):
    ensure_work(project)
    if not text.strip():
        raise ValueError('Note must not be blank')
    event(project, kind, {'text': text})
    return {'recorded': kind}


def handoff(project, required_files):
    ensure_work(project)
    requirements = read_json(runtime_path(project, 'requirements.json'), [])
    checks = evidence(project)
    good = {e['id'] for e in checks if e['fresh'] and e['result'] == 'pass'}
    blockers = []
    if not requirements:
        blockers.append('requirements missing')
    for r in requirements:
        if r['priority'] == 'must' and (r['status'] != 'verified' or not r['evidence'] or
                any(e not in good for e in r['evidence'])):
            blockers.append('requirement unverified: ' + r['id'])
    latest = {}
    for e in checks:
        latest[e['name']] = e
    for name, e in latest.items():
        if e['result'] != 'pass':
            blockers.append('latest check failed: ' + name)
    if load_state(project)['kind'] == 'web':
        if not any(e['name'] == 'manual-ui' and e['type'] == 'participant-attestation' and
                   e['fresh'] and e['result'] == 'pass' for e in checks):
            blockers.append('manual-ui evidence missing or stale')
    for relative in required_files:
        if not safe_path(project, relative).is_file():
            blockers.append('required file missing: ' + relative)
    report = {'ready': not blockers, 'blockers': blockers,
              'requirements': requirements, 'evidence': checks,
              'required_files_checked': required_files,
              'platform_submission_performed': False,
              'notice': 'Readiness is a local checklist, not a quality grade or actual submission. Confirm saved state and required filenames in platform.'}
    write_json(runtime_path(project, 'handoff.json'), report)
    lines = ['# Local submission review', '', 'Ready: ' + str(report['ready']), '',
             'Platform submission performed: false', '', '## Remaining issues', '']
    lines += ['- ' + b for b in blockers] or ['- None on the recorded checklist.']
    lines += ['', '## Requirements', ''] + ['- ' + r['id'] + ': ' + r['text'] + ' [' + r['status'] + ']' for r in requirements]
    lines += ['', '## Evidence', ''] + [f"- {e['id']}: {e['name']} / {e['result']} / fresh={e['fresh']} / type={e['type']}" for e in checks]
    runtime_path(project, 'HANDOFF.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report
