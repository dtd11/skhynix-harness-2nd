"""Run explicit commands with best-effort phase/deadline supervision."""
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

from .common import ensure_optional_work, now, parse_time, state_path, load_state


def validate_acquisition(command):
    """Catch common non-clone acquisition commands, not arbitrary script internals."""
    binary = Path(command[0]).name.lower()
    for suffix in ('.exe', '.cmd', '.bat'):
        binary = binary.removesuffix(suffix)
    args = [str(v).lower() for v in command[1:]]
    forbidden = binary in {'npx', 'pnpx', 'bunx', 'curl', 'wget'}
    if binary.startswith('pip') or (binary.startswith('python') and '-m' in args and
            args[args.index('-m') + 1:args.index('-m') + 2] == ['pip']):
        forbidden |= any(v in {'install', 'download', 'wheel'} for v in args)
    if binary in {'npm', 'pnpm', 'yarn', 'bun'}:
        subcommand = next((v for v in args if not v.startswith('-')), '')
        forbidden |= subcommand in {'install', 'i', 'add', 'update', 'upgrade', 'ci', 'exec', 'dlx', 'create'}
        forbidden |= binary in {'yarn', 'bun'} and not subcommand
    if binary == 'uv':
        forbidden |= any(v in {'sync', 'pip', 'tool', 'run', 'add'} for v in args)
    if forbidden:
        raise ValueError('Git-Clone-only acquisition: package installers/URL download commands are disabled. Use provided tools or public Git Clone sources.')


def stop_process_tree(process):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.kill()
    except ProcessLookupError:
        pass
    process.wait()


def run_local(project, command, stdout, stderr, timeout=None):
    ensure_optional_work(project)
    validate_acquisition(command)
    env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'DO_NOT_TRACK': '1'}
    executable = Path(command[0])
    if not executable.is_absolute() and ('/' in command[0] or '\\' in command[0]):
        binary = str((project / executable).resolve())
    else:
        binary = shutil.which(command[0]) or command[0]
    resolved = [binary, *command[1:]]
    process = subprocess.Popen(resolved, cwd=project, env=env, stdin=subprocess.DEVNULL,
                               stdout=stdout, stderr=stderr,
                               start_new_session=os.name != 'nt',
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0)
    began = time.monotonic()
    try:
        while True:
            if state_path(project).exists():
                state = load_state(project)
                if state['stage'] not in ('work', 'submission-preview'):
                    stop_process_tree(process)
                    return 125, 'stage-interrupted'
                if now() >= parse_time(state['hard_work_end']):
                    stop_process_tree(process)
                    return 125, 'deadline-expired'
            code = process.poll()
            if code is not None:
                return code, 'pass' if code == 0 else 'fail'
            if timeout is not None and time.monotonic() - began >= timeout:
                stop_process_tree(process)
                return 124, 'timeout'
            delay = 0.05
            if timeout is not None:
                delay = min(delay, max(0.001, timeout - (time.monotonic() - began)))
            time.sleep(delay)
    finally:
        # An interrupted/corrupted supervisor must not leave its owned child running.
        if process.poll() is None:
            stop_process_tree(process)
