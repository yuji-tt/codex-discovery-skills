"""Verify public GitHub installation in a disposable destination using Codex's official helper."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import quote
from urllib.request import Request, urlopen
import zipfile

from validate import NAMES, validate

REPOSITORY = 'yuji-tt/codex-discovery-skills'


def download(url):
    # Deliberately anonymous: this verifies public access, not account permissions.
    request = Request(url, headers={'User-Agent': 'codex-discovery-install-smoke'})
    with urlopen(request, timeout=60) as response:
        return response.read()


def resolve_ref(ref):
    data = json.loads(download(f'https://api.github.com/repos/{REPOSITORY}/commits/{quote(ref, safe="")}'))
    sha = data.get('sha', '')
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('GitHub did not return a valid commit SHA')
    return sha


def public_manifest(sha):
    archive = download(f'https://codeload.github.com/{REPOSITORY}/zip/{sha}')
    result = {}
    # Read entries without extracting remote paths onto the filesystem.
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        for entry in bundle.infolist():
            parts = entry.filename.split('/')
            if not entry.is_dir() and len(parts) >= 4 and parts[1] == 'skills' and parts[2] in NAMES:
                relative = '/'.join(parts[2:])
                result[relative] = hashlib.sha256(bundle.read(entry)).hexdigest()
    if not result:
        raise ValueError('Public archive contains no expected skill files')
    return result


def installed_manifest(destination):
    return {
        path.relative_to(destination).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in destination.rglob('*') if path.is_file()
    }


def find_installer(explicit=None):
    codex_home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    helper = explicit or codex_home / 'skills/.system/skill-installer/scripts/install-skill-from-github.py'
    helper = Path(helper).resolve()
    if not helper.is_file():
        raise ValueError('Official installer not found; pass --installer with its current helper path')
    return helper


def smoke_install(ref, installer, temp_parent=None, creator=None):
    sha = resolve_ref(ref)
    expected = public_manifest(sha)
    parent = Path(temp_parent or tempfile.gettempdir()).resolve()
    if not parent.is_dir():
        raise ValueError('Temporary parent must already be a directory')
    environment = dict(os.environ)
    for name in ('GH_TOKEN', 'GITHUB_TOKEN'):
        environment.pop(name, None)
    environment['PYTHONUTF8'] = '1'
    with tempfile.TemporaryDirectory(prefix='discovery-install-', dir=parent) as scratch:
        destination = Path(scratch).resolve()
        if destination.parent != parent:
            raise ValueError('Temporary installation escaped its intended parent')
        command = [sys.executable, '-X', 'utf8', str(installer), '--repo', REPOSITORY,
                   '--path', *[f'skills/{name}' for name in sorted(NAMES)],
                   '--ref', ref, '--dest', str(destination), '--method', 'download']
        subprocess.run(command, check=True, env=environment)
        errors = validate(destination, installed=True)
        if errors:
            raise ValueError('\n'.join(errors))
        if installed_manifest(destination) != expected:
            raise ValueError('Installed package files differ from the public commit archive; the ref may have moved')
        if creator:
            for name in sorted(NAMES):
                subprocess.run([sys.executable, '-X', 'utf8', str(creator / 'scripts/quick_validate.py'),
                                str(destination / name)], check=True, env=environment)
        if resolve_ref(ref) != sha:
            raise ValueError('Remote ref moved during verification; rerun against the current ref')
    # TemporaryDirectory cleans up on both success and failure. Report only after cleanup.
    if destination.exists():
        raise ValueError('Temporary installation was not removed')
    return {'repository': REPOSITORY, 'ref': ref, 'commit': sha,
            'skills': sorted(NAMES), 'files_verified': len(expected),
            'installer_sha256': hashlib.sha256(installer.read_bytes()).hexdigest(),
            'official_validation': creator is not None, 'temporary_installation_removed': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref', required=True, help='Public branch, tag, or commit to install')
    parser.add_argument('--installer', type=Path, help='Path to the installed official Skill installer helper')
    parser.add_argument('--official-creator', type=Path, help='Also validate installed copies with official quick_validate.py')
    parser.add_argument('--temp-parent', type=Path, help='Existing parent for disposable installation')
    args = parser.parse_args()
    try:
        result = smoke_install(args.ref, find_installer(args.installer), args.temp_parent, args.official_creator)
    except (OSError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'Installation smoke test failed: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
