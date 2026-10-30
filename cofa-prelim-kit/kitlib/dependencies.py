import importlib.metadata
import json
import shutil
import subprocess
import sys
from .common import ROOT, ensure_optional_work, read_json


def inspect_libraries(project, profiles, dry_run=False):
    ensure_optional_work(project)
    lock = read_json(ROOT / 'config/libraries.lock.json')
    names = []
    for profile in profiles:
        if profile not in lock['profiles']:
            raise ValueError('Unknown library profile: ' + profile)
        names += lock['profiles'][profile]
    selected = [v for v in lock['libraries'] if v['name'] in set(names)]
    package = read_json(project / 'package.json', {})
    declared = {**package.get('dependencies', {}), **package.get('devDependencies', {})}
    items = []
    for value in selected:
        item = {'name': value['name'], 'ecosystem': value['ecosystem'],
                'public_source': value['repository'], 'reference_version': value['version'],
                'runtime_requirement_of_reference_version': value['runtime']}
        if value['ecosystem'] == 'python':
            try:
                item['installed_version'] = importlib.metadata.version(value['name'])
                item['metadata_present'] = True
            except importlib.metadata.PackageNotFoundError:
                item['installed_version'] = None
                item['metadata_present'] = False
        else:
            item['declared_version'] = declared.get(value['name'])
            item['metadata_present'] = False
            node = shutil.which('node')
            if node:
                # Built-in fs/path/module only: inspect resolution without loading package code.
                code = '''const fs=require('node:fs'),p=require('node:path'),m=require('node:module');
const req=m.createRequire(p.join(process.argv[1],'package.json'));
try{let d=p.dirname(req.resolve(process.argv[2]));for(;;){const f=p.join(d,'package.json');
if(fs.existsSync(f)){const j=JSON.parse(fs.readFileSync(f,'utf8'));if(j.name===process.argv[2]){
console.log(JSON.stringify({metadata_present:true,installed_version:j.version}));process.exit(0)}}
const up=p.dirname(d);if(up===d)break;d=up;} }catch{}
console.log(JSON.stringify({metadata_present:false,installed_version:null}));'''
                try:
                    proc = subprocess.run([node, '-e', code, str(project), value['name']],
                                          capture_output=True, text=True, timeout=8, check=False)
                    if proc.returncode == 0:
                        item.update(json.loads(proc.stdout))
                    else:
                        item['probe_error'] = 'Local Node metadata probe failed'
                except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                    item['probe_error'] = str(exc)
            else:
                item['probe_error'] = 'Node is not available'
        items.append(item)
    return {'profiles': profiles, 'libraries': items, 'commands': [],
            'mode': 'inspect-existing-only', 'dry_run': dry_run,
            'acquisition_policy': 'git-clone-only', 'network_used': False,
            'packages_installed': False, 'project_files_changed': False,
            'python_runtime': sys.version.split()[0],
            'probe_scope': 'Metadata only in the current Python interpreter/project Node resolution. Presence is not execution verification; missing metadata does not prove absence of vendored code.',
            'missing_library_action': 'Use provided tools/standard library. Git-cloned source is not automatically a runnable package; do not fetch dependencies from registries.'}
