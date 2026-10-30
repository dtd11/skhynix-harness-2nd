"""Behavioral tests of the kit, independent of any exam solution."""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cofa-test-')
        self.project = Path(self.tmp.name) / 'project'
        self.project.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, code=0):
        result = subprocess.run([sys.executable, str(ROOT / 'kit.py'), *args],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def call(self, command, *args, code=0):
        return self.cli(command, '--project', str(self.project), *args, code=code)

    def practice(self):
        return self.call('start', '--practice')

    def directory_link(self, link, target):
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            if sys.platform != 'win32':
                self.skipTest('Directory links unavailable on this host')
            # Junctions do not require Windows symbolic-link privileges.
            def quote(value):
                return "'" + str(value).replace("'", "''") + "'"
            script = 'New-Item -ItemType Junction -Path ' + quote(link) + ' -Target ' + quote(target) + ' | Out-Null'
            proc = subprocess.run(['powershell.exe', '-NoProfile', '-Command', script], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_status_requires_explicit_start(self):
        self.call('status', code=2)

    def test_normal_deadline_and_submit_margin(self):
        self.call('start', '--started-at', '2026-10-31T10:00:00+09:00')
        s = self.call('status', '--as-of', '2026-10-31T12:49:00+09:00')
        self.assertTrue(s['hard_work_end'].startswith('2026-10-31T13:00'))
        self.assertTrue(s['recommended_confirm_by'].startswith('2026-10-31T13:00'))
        self.assertTrue(s['recommended_submission_begin'].startswith('2026-10-31T12:50'))
        self.assertEqual(s['phase'], 'stabilize')

    def test_late_start_preserves_oral_reserve(self):
        self.call('start', '--started-at', '2026-10-31T12:50:00+09:00')
        s = self.call('status', '--as-of', '2026-10-31T13:11:00+09:00')
        self.assertTrue(s['hard_work_end'].startswith('2026-10-31T14:00'))
        self.assertTrue(s['recommended_confirm_by'].startswith('2026-10-31T13:20'))
        self.assertEqual(s['phase'], 'handoff')

    def test_too_late_reserve_is_warning_not_extra_time(self):
        self.call('start', '--started-at', '2026-10-31T13:55:00+09:00')
        s = self.call('status', '--as-of', '2026-10-31T13:56:00+09:00')
        self.assertTrue(s['warnings'])
        self.assertLess(s['recommended_work_remaining_minutes'], 0)

    def test_naive_datetime_rejected(self):
        self.call('start', '--started-at', '2026-10-31T10:00:00', code=2)

    def test_start_after_overall_end_rejected(self):
        self.call('start', '--started-at', '2026-10-31T14:01:00+09:00', code=2)

    def test_start_does_not_reset_existing_session(self):
        self.practice()
        before = (self.project / '.cofa/state.json').read_bytes()
        self.call('start', '--practice', code=2)
        self.assertEqual(before, (self.project / '.cofa/state.json').read_bytes())

    def test_install_preserves_agents_and_is_idempotent(self):
        p = self.project / 'AGENTS.md'
        p.write_bytes(b'# Existing\r\nPreserve me.\r\n')
        self.call('install')
        first = p.read_bytes()
        self.assertTrue(first.startswith(b'# Existing\r\nPreserve me.\r\n'))
        self.call('install')
        self.assertEqual(first, p.read_bytes())
        self.assertTrue((self.project / '.agents/skills/cofa-prelim/SKILL.md').exists())
        self.assertFalse((self.project / '.codex/config.toml').exists())
        result = subprocess.run([sys.executable, str(self.project / '.cofa-kit/kit.py'), 'catalogue'],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_install_dry_run_writes_nothing(self):
        self.call('install', '--dry-run')
        self.assertEqual(list(self.project.iterdir()), [])

    def test_install_conflict_aborts_before_writes(self):
        p = self.project / '.agents/skills/cofa-prelim/SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('mine', encoding='utf-8')
        self.call('install', code=2)
        self.assertEqual(p.read_text(), 'mine')
        self.assertFalse((self.project / '.cofa-kit').exists())

    def test_install_refuses_mutation_after_oral(self):
        self.practice()
        self.call('stage', '--to', 'locked')
        self.call('stage', '--to', 'oral')
        self.call('install', code=2)

    def test_failed_check_is_not_success(self):
        self.practice()
        result = self.call('check', '--name', 'unit', '--', sys.executable, '-c',
                           'print("wrong total"); raise SystemExit(7)', code=7)
        self.assertEqual(result['result'], 'fail')
        self.assertEqual(result['exit_code'], 7)
        self.assertIn('wrong total', Path(result['log']).read_text())

    def test_check_timeout_is_recorded(self):
        self.practice()
        result = self.call('check', '--name', 'slow', '--timeout', '0.1', '--',
                           sys.executable, '-c', 'import time;time.sleep(10)', code=124)
        self.assertEqual(result['result'], 'timeout')

    def test_check_stale_after_source_change(self):
        self.practice()
        p = self.project / 'main.py'
        p.write_text('a = 1', encoding='utf-8')
        self.call('check', '--name', 'unit', '--', sys.executable, '-c', 'assert 1+1 == 2')
        p.write_text('a = 2', encoding='utf-8')
        s = self.call('status')
        self.assertFalse(s['evidence'][0]['fresh'])

    def test_source_changed_during_check_cannot_count_as_verified(self):
        self.practice()
        e = self.call('check', '--name', 'mutating', '--', sys.executable, '-c',
                      'from pathlib import Path;Path("source.py").write_text("a=1")')
        self.assertFalse(e['stable_snapshot'])

    def test_verified_requirement_needs_evidence(self):
        self.practice()
        self.call('require', '--id', 'R1', '--text', 'Calculate correct totals')
        self.call('require', '--id', 'R1', '--status', 'verified', code=2)

    def test_handoff_checks_actual_requirements_and_files(self):
        self.practice()
        self.call('require', '--id', 'R1', '--text', 'Correct total')
        e = self.call('check', '--name', 'unit', '--', sys.executable, '-c', 'assert 1+1 == 2')
        self.call('require', '--id', 'R1', '--status', 'verified', '--evidence', e['id'])
        report = self.call('handoff', '--required-file', 'README.md', code=2)
        self.assertFalse(report['ready'])
        (self.project / 'README.md').write_text('run: python main.py', encoding='utf-8')
        e = self.call('check', '--name', 'unit', '--', sys.executable, '-c', 'assert 1+1 == 2')
        self.call('require', '--id', 'R1', '--status', 'verified', '--evidence', e['id'])
        self.assertTrue(self.call('handoff', '--required-file', 'README.md')['ready'])

    def test_web_build_does_not_prove_manual_ui(self):
        self.call('start', '--practice', '--kind', 'web')
        self.call('require', '--id', 'R1', '--text', 'UI works')
        e = self.call('check', '--name', 'build', '--', sys.executable, '-c', 'pass')
        self.call('require', '--id', 'R1', '--status', 'verified', '--evidence', e['id'])
        r = self.call('handoff', code=2)
        self.assertIn('manual-ui evidence missing or stale', r['blockers'])
        self.call('manual', '--name', 'manual-ui', '--result', 'pass', '--note', 'Participant checked main flow in platform preview')
        self.assertTrue(self.call('handoff')['ready'])

    def test_oral_is_irreversible_and_blocks_execution(self):
        self.practice()
        self.call('stage', '--to', 'locked')
        self.call('stage', '--to', 'oral')
        self.call('stage', '--to', 'work', code=2)
        self.call('check', '--name', 'unit', '--', sys.executable, '-c', 'pass', code=2)
        self.call('note', '--kind', 'decision', '--text', 'new code', code=2)

    def test_library_inventory_is_read_only(self):
        p = self.call('libraries', '--profile', 'analytics', '--dry-run')
        self.assertEqual(p['commands'], [])
        self.assertEqual(p['acquisition_policy'], 'git-clone-only')
        self.assertFalse(p['network_used'])
        self.assertEqual({v['name'] for v in p['libraries']}, {'duckdb', 'networkx'})
        self.assertEqual(list(self.project.iterdir()), [])

    def test_requested_library_install_preserves_existing_js_version(self):
        (self.project / 'package.json').write_text(json.dumps({'dependencies': {'@xyflow/react': '^12.0.0'}}))
        p = self.call('libraries', '--profile', 'flow', '--dry-run')
        self.assertEqual(p['commands'], [])
        self.assertEqual(p['libraries'][0]['declared_version'], '^12.0.0')
        self.assertEqual(json.loads((self.project / 'package.json').read_text())['dependencies']['@xyflow/react'], '^12.0.0')

    def test_nested_source_build_folder_is_not_ignored(self):
        self.practice()
        p = self.project / 'src/build/calculation.py'
        p.parent.mkdir(parents=True)
        p.write_text('total = 3', encoding='utf-8')
        self.call('check', '--name', 'unit', '--', sys.executable, '-c', 'pass')
        p.write_text('total = 4', encoding='utf-8')
        self.assertFalse(self.call('status')['evidence'][0]['fresh'])

    def test_running_check_stops_on_submission_lock(self):
        self.practice()
        marker = self.project / '.cofa/child-started'
        child_code = 'from pathlib import Path;import time;Path(".cofa/child-started").write_text("yes");time.sleep(20)'
        proc = subprocess.Popen([sys.executable, str(ROOT / 'kit.py'), 'check', '--project',
                                 str(self.project), '--name', 'long', '--', sys.executable, '-c', child_code],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        try:
            end = time.monotonic() + 5
            while not marker.exists() and time.monotonic() < end:
                time.sleep(0.02)
            self.assertTrue(marker.exists(), 'Child failed to start')
            self.call('stage', '--to', 'locked')
            out, err = proc.communicate(timeout=8)
            self.assertEqual(proc.returncode, 125, out + err)
            self.assertFalse(json.loads(out)['recorded'])
            self.assertFalse((self.project / '.cofa/evidence.json').exists())
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_running_check_stops_at_hard_work_deadline(self):
        self.practice()
        p = self.project / '.cofa/state.json'
        state = json.loads(p.read_text())
        state['hard_work_end'] = (datetime.now(timezone.utc) + timedelta(seconds=0.8)).isoformat()
        p.write_text(json.dumps(state))
        began = time.monotonic()
        result = self.call('check', '--name', 'late', '--', sys.executable, '-c', 'import time;time.sleep(20)', code=125)
        self.assertLess(time.monotonic() - began, 5)
        self.assertEqual(result['result'], 'deadline-expired')
        self.assertFalse((self.project / '.cofa/evidence.json').exists())

    def test_unlisted_skill_is_not_activated(self):
        import shutil
        copy = Path(self.tmp.name) / 'kit-copy'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        extra = copy / 'skills/unlisted/SKILL.md'
        extra.parent.mkdir(parents=True)
        extra.write_text('Unlisted test content', encoding='utf-8')
        result = subprocess.run([sys.executable, str(copy / 'kit.py'), 'install', '--project', str(self.project)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.project / '.agents/skills/unlisted').exists())

    def test_runtime_directory_symlink_cannot_escape_project(self):
        external = Path(self.tmp.name) / 'external'
        external.mkdir()
        self.directory_link(self.project / '.cofa', external)
        self.call('start', '--practice', code=2)
        self.assertEqual(list(external.iterdir()), [])

    def test_library_inventory_does_not_follow_environment_links(self):
        external = Path(self.tmp.name) / 'external'
        external.mkdir()
        self.directory_link(self.project / '.venv-cofa', external)
        p = self.call('libraries', '--profile', 'analytics')
        self.assertFalse(p['packages_installed'])
        self.assertEqual(list(external.iterdir()), [])

    def test_tampered_snapshot_aborts_install(self):
        import shutil
        copy = Path(self.tmp.name) / 'kit-copy'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        (copy / 'skills/cofa-debug/SKILL.md').write_text('changed', encoding='utf-8')
        result = subprocess.run([sys.executable, str(copy / 'kit.py'), 'install', '--project', str(self.project)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_existing_pnpm_lock_is_unchanged_by_inventory(self):
        (self.project / 'package.json').write_text('{}')
        (self.project / 'pnpm-lock.yaml').write_text('lockfileVersion: 9.0')
        p = self.call('libraries', '--profile', 'flow', '--dry-run')
        self.assertEqual(p['commands'], [])
        self.assertEqual((self.project / 'pnpm-lock.yaml').read_text(), 'lockfileVersion: 9.0')

    def test_skill_directory_link_cannot_modify_external_folder(self):
        external = Path(self.tmp.name) / 'external'
        external.mkdir()
        (self.project / '.agents').mkdir()
        self.directory_link(self.project / '.agents/skills', external)
        self.call('install', code=2)
        self.assertEqual(list(external.iterdir()), [])

    def test_real_exit_125_is_recorded_as_failed_command(self):
        self.practice()
        e = self.call('check', '--name', 'real125', '--', sys.executable, '-c', 'raise SystemExit(125)', code=125)
        self.assertEqual(e['result'], 'fail')
        self.assertIn('id', e)

    def test_supervisor_exception_stops_owned_process(self):
        from unittest.mock import patch
        sys.path.insert(0, str(ROOT))
        from kitlib.process import run_local
        self.practice()
        spawned = []
        original = subprocess.Popen
        def spawn(*args, **kwargs):
            process = original(*args, **kwargs)
            spawned.append(process)
            return process
        with (self.project / '.cofa/supervisor-test.log').open('wb') as log:
            with patch('kitlib.process.subprocess.Popen', side_effect=spawn), patch('kitlib.process.load_state', side_effect=ValueError('broken state')):
                with self.assertRaisesRegex(ValueError, 'broken state'):
                    run_local(self.project, [sys.executable, '-c', 'import time;time.sleep(30)'], log, subprocess.STDOUT)
        self.assertTrue(spawned)
        self.assertTrue(all(p.poll() is not None for p in spawned))

    def test_relative_executable_resolves_against_project(self):
        self.practice()
        binary = os.path.relpath(sys.executable, self.project)
        e = self.call('check', '--name', 'relative', '--', binary, '-c', 'print("relative works")')
        self.assertEqual(e['result'], 'pass')

    def test_requirement_priority_update_is_preserved(self):
        self.practice()
        self.call('require', '--id', 'R1', '--text', 'Optional polish', '--priority', 'optional')
        item = self.call('require', '--id', 'R1', '--status', 'implemented')
        self.assertEqual(item['priority'], 'optional')
        item = self.call('require', '--id', 'R1', '--priority', 'must')
        self.assertEqual(item['priority'], 'must')

    def test_non_dry_library_command_does_not_create_packages_or_venv(self):
        p = self.call('libraries', '--profile', 'analytics', '--profile', 'quality')
        self.assertEqual(p['mode'], 'inspect-existing-only')
        self.assertFalse(p['packages_installed'])
        self.assertFalse(p['project_files_changed'])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_registry_download_checks_are_rejected(self):
        self.practice()
        for cmd in ([sys.executable, '-m', 'pip', 'install', 'duckdb'],
                    ['npm', 'install', 'vitest'], ['npx', 'vitest'],
                    ['curl', 'https://example.invalid/file']):
            with self.subTest(cmd=cmd):
                p = self.call('check', '--name', 'blocked', '--', *cmd, code=2)
                self.assertIn('Git-Clone-only', p['error'])
        self.assertFalse((self.project / '.cofa/evidence.json').exists())

    def test_local_commands_and_git_clone_pass_acquisition_guard(self):
        sys.path.insert(0, str(ROOT))
        from kitlib.process import validate_acquisition
        for cmd in [['git', 'clone', 'https://example.invalid/repo.git'],
                    ['git', 'diff'], ['npm', 'test', '--', '--run'],
                    [sys.executable, '-m', 'unittest'], ['node', 'local.js']]:
            validate_acquisition(cmd)

    def test_git_checkout_preserves_bundle_bytes(self):
        import shutil
        git = shutil.which('git')
        if not git:
            self.skipTest('Git is not available')
        source = Path(self.tmp.name) / 'git-source'
        clone = Path(self.tmp.name) / 'git-clone'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        def run(*arguments):
            p = subprocess.run([git, *arguments], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        run('-C', str(source), 'init')
        run('-C', str(source), '-c', 'core.autocrlf=true', 'add', '.')
        run('-C', str(source), '-c', 'user.name=Toolkit Test', '-c', 'user.email=toolkit-test@example.invalid',
            'commit', '-m', 'Local transport fixture')
        run('-c', 'core.autocrlf=false', 'clone', '--no-hardlinks', str(source), str(clone))
        p = subprocess.run([sys.executable, str(clone / 'kit.py'), 'verify-bundle'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertTrue(json.loads(p.stdout)['ok'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
