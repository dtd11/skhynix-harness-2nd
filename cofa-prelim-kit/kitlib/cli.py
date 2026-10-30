import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from .common import ROOT, VERSION, read_json, verify_bundle
from . import checks, dependencies, install, session


def parser():
    p = argparse.ArgumentParser(description='Local COFA helper; platform rules/timers remain authoritative.')
    p.add_argument('--version', action='version', version=VERSION)
    sub = p.add_subparsers(dest='action', required=True)
    sub.add_parser('verify-bundle', help='Check all distributable hashes')
    sub.add_parser('catalogue', help='Show bundled sources and existing-library reference catalogue')
    def project_command(name, helptext):
        c = sub.add_parser(name, help=helptext)
        c.add_argument('--project', type=Path, default=Path.cwd())
        return c
    c = project_command('install', 'Copy skills locally; preserve existing project instructions')
    c.add_argument('--dry-run', action='store_true')
    project_command('doctor', 'Inspect local runtimes; do not install or connect services')
    c = project_command('start', 'Record actual task-start time; does not start the platform exam')
    c.add_argument('--started-at')
    c.add_argument('--overall-end')
    c.add_argument('--practice', action='store_true')
    c.add_argument('--kind', choices=('generic', 'web', 'data'), default='generic')
    c = project_command('status', 'Read deadlines and verification freshness')
    c.add_argument('--as-of', help='Simulate a timestamp for practice; does not alter state')
    c = project_command('stage', 'Record a platform stage already reached by the participant')
    c.add_argument('--to', required=True, choices=('work', 'submission-preview', 'locked', 'oral', 'finished'))
    c = project_command('require', 'Record or update one actual task requirement')
    c.add_argument('--id', required=True)
    c.add_argument('--text')
    c.add_argument('--priority', choices=('must', 'optional'))
    c.add_argument('--status', choices=('todo', 'implemented', 'verified', 'blocked'))
    c.add_argument('--evidence', nargs='+')
    c = project_command('note', 'Record a concise decision or limitation locally')
    c.add_argument('--kind', choices=('decision', 'limitation', 'blocker'), required=True)
    c.add_argument('--text', required=True)
    c = project_command('check', 'Run an explicit permitted command and preserve its full output')
    c.add_argument('--name', required=True)
    c.add_argument('--timeout', type=float, default=120)
    c.add_argument('command', nargs=argparse.REMAINDER)
    c = project_command('manual', 'Record participant observations; never automate GUI checks')
    c.add_argument('--name', required=True)
    c.add_argument('--result', choices=('pass', 'fail'), required=True)
    c.add_argument('--note', required=True)
    c = project_command('handoff', 'Generate local readiness report; never submit through the platform')
    c.add_argument('--required-file', action='append', default=[])
    c = project_command('libraries', 'Read-only inspection of existing libraries; no install/download')
    c.add_argument('--profile', action='append', required=True,
                   choices=('analytics', 'documents', 'optimization', 'quality', 'flow', 'web-test'))
    c.add_argument('--dry-run', action='store_true', help='Compatibility flag; this command is always read-only')
    return p


def doctor(project):
    tools = {}
    for executable, arguments in [('node', ['--version']), ('git', ['--version'])]:
        path = shutil.which(executable)
        if not path:
            tools[executable] = {'available': False}
            continue
        try:
            proc = subprocess.run([path, *arguments], capture_output=True, text=True, timeout=10)
            tools[executable] = {'available': proc.returncode == 0, 'version': proc.stdout.strip()}
        except (OSError, subprocess.TimeoutExpired) as exc:
            tools[executable] = {'available': False, 'error': str(exc)}
    return {'kit': VERSION, 'python': sys.version.split()[0], 'project': str(project),
            'tools': tools, 'package_managers': {n: bool(shutil.which(n)) for n in ['npm', 'pnpm', 'yarn', 'bun']},
            'host_config_modified': False, 'network_used': False,
            'guidance': 'Base needs Python3.10+. Acquisition is Git Clone only. libraries only inspects provided dependencies; no package installation. App server must bind0.0.0.0 and use the actual port in platform preview.'}


def execute(args):
    a = args.action
    if a == 'verify-bundle':
        return verify_bundle(), 0
    if a == 'catalogue':
        return {'sources': read_json(ROOT / 'config/sources.lock.json'),
                'libraries': read_json(ROOT / 'config/libraries.lock.json')}, 0
    project = args.project.resolve()
    if not project.is_dir():
        raise ValueError('Project directory does not exist: ' + str(project))
    if a == 'install':
        return install.install(project, args.dry_run), 0
    if a == 'doctor':
        return doctor(project), 0
    if a == 'start':
        return session.start(project, args.started_at, args.overall_end, args.practice, args.kind), 0
    if a == 'status':
        return session.status(project, args.as_of), 0
    if a == 'stage':
        return session.stage(project, args.to), 0
    if a == 'require':
        return session.require(project, args.id, args.text, args.priority, args.status, args.evidence), 0
    if a == 'note':
        return session.note(project, args.kind, args.text), 0
    if a == 'check':
        command = args.command[1:] if args.command[:1] == ['--'] else args.command
        result = checks.run_check(project, args.name, command, args.timeout)
        return result, max(0, min(255, result['exit_code'])) if result['exit_code'] >= 0 else 1
    if a == 'manual':
        return checks.manual(project, args.name, args.result, args.note), 0
    if a == 'handoff':
        result = session.handoff(project, args.required_file)
        return result, 0 if result['ready'] else 2
    if a == 'libraries':
        return dependencies.inspect_libraries(project, args.profile, args.dry_run), 0
    raise ValueError('Unknown action')


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    args = parser().parse_args(argv)
    try:
        result, code = execute(args)
    except KeyboardInterrupt:
        result, code = {'ok': False, 'error': 'Interrupted; owned running child was stopped.'}, 130
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        result, code = {'ok': False, 'error': str(exc)}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code
