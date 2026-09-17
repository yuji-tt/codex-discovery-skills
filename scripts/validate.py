"""Offline repository integrity checks; optionally run the installed official validator."""
import argparse
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'objective-audit', 'research-deepener', 'structural-transfer', 'discovery-loop'}

def validate(root):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    for name in sorted(NAMES):
        folder = root / 'skills' / name
        p = folder / 'SKILL.md'
        require(p.is_file(), f'Missing {p.relative_to(root)}')
        if not p.is_file():
            continue
        match = re.match(r'^---\n(.*?)\n---\n', p.read_text(encoding='utf-8'), re.S)
        require(match is not None, f'{name}: missing YAML frontmatter')
        if match:
            try:
                meta = yaml.safe_load(match[1])
                require(isinstance(meta, dict), f'{name}: frontmatter must be mapping')
                if isinstance(meta, dict):
                    require(meta.get('name') == name, f'{name}: name mismatch')
                    require(isinstance(meta.get('description'), str) and bool(meta['description'].strip()), f'{name}: missing description')
            except yaml.YAMLError as exc:
                errors.append(f'{name}: {exc}')
        ui = folder / 'agents/openai.yaml'
        require(ui.is_file(), f'{name}: missing UI metadata')
        if ui.is_file():
            try:
                interface = yaml.safe_load(ui.read_text(encoding='utf-8'))['interface']
                require(25 <= len(interface['short_description']) <= 64, f'{name}: UI description length')
                require(f'${name}' in interface['default_prompt'], f'{name}: default prompt must invoke skill')
            except (yaml.YAMLError, KeyError, TypeError):
                errors.append(f'{name}: invalid UI metadata')
    for p in root.rglob('*.md'):
        if any(part.startswith('.') for part in p.relative_to(root).parts):
            continue
        text = p.read_text(encoding='utf-8')
        require(not re.search(r'\bTODO\b|\bFIXME\b|\bTBD\b', text), f'{p.relative_to(root)}: unresolved placeholder')
        # Inline relative links; fragments and external URLs are intentionally not checked.
        for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
            parsed = urlsplit(target.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            require((p.parent / unquote(parsed.path)).exists(), f'{p.relative_to(root)}: broken link {target}')
    try:
        cases = yaml.safe_load((root / 'evals/cases.yaml').read_text(encoding='utf-8'))['cases']
        require(len(cases) >= 12, 'Need at least 12 cases')
        ids = set()
        for case in cases:
            require(set(('id','domain','skill','prompt','expected_route','must_include','must_avoid')) <= case.keys(), 'Incomplete evaluation case')
            require(case['id'] not in ids, f'Duplicate case {case["id"]}')
            ids.add(case['id'])
            require(case['skill'] in NAMES, f'Unknown skill in {case["id"]}')
            require(all(isinstance(case[k], str) and case[k].strip() for k in ('id','domain','prompt','expected_route')), 'Invalid case text')
            require(all(isinstance(case[k], list) and case[k] and all(isinstance(x,str) and x.strip() for x in case[k]) for k in ('must_include','must_avoid')), 'Invalid case criteria')
    except (OSError, yaml.YAMLError, KeyError, TypeError) as exc:
        errors.append(f'Invalid case suite: {exc}')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--official-creator', type=Path)
    args = parser.parse_args()
    errors = validate(ROOT)
    if args.official_creator:
        validator = args.official_creator / 'scripts/quick_validate.py'
        for name in sorted(NAMES):
            result = subprocess.run([sys.executable, '-X', 'utf8', str(validator), str(ROOT / 'skills' / name)], check=False)
            if result.returncode:
                errors.append(f'{name}: official validation failed')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('PASS: four skills, UI metadata, frontmatter, placeholders, relative links, and evaluation cases')
    return 0

if __name__ == '__main__':
    sys.exit(main())
