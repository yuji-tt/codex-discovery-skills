"""Prepare blinded manual evaluation prompts and summarize reviewed JSONL ratings."""
import argparse
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ('objective_goal','mechanism','persistence','plateau','structure','falsifiability','simplicity','implementability','calibration')

def prepare(out):
    cases = yaml.safe_load((ROOT/'evals/cases.yaml').read_text(encoding='utf-8'))['cases']
    out.mkdir(parents=True, exist_ok=True)
    for case in cases:
        folder = ROOT/'skills'/case['skill']
        materials = [folder/'SKILL.md', *sorted((folder/'references').glob('*.md'))]
        context = '\n\n'.join(f'## {p.relative_to(folder)}\n\n{p.read_text(encoding="utf-8")}' for p in materials)
        (out/f'{case["id"]}.skill.md').write_text(f'Apply the following skill to the request. Report concise decision records.\n\n{context}\n\n## Request\n\n{case["prompt"]}\n', encoding='utf-8')
        (out/f'{case["id"]}.baseline.md').write_text(case['prompt']+'\n', encoding='utf-8')
    return len(cases)

def summarize(path):
    known = {c['id'] for c in yaml.safe_load((ROOT/'evals/cases.yaml').read_text(encoding='utf-8'))['cases']}
    groups, seen = {}, set()
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get('id') not in known or row.get('condition') not in ('baseline','skill'):
            raise ValueError('Unknown case or condition')
        if not isinstance(row.get('run_id'),str) or not row['run_id'].strip():
            raise ValueError('Missing run_id')
        key = (row['id'],row['condition'],row['run_id'])
        if key in seen:
            raise ValueError('Duplicate case/condition/run_id')
        seen.add(key)
        scores = row.get('scores',{})
        if set(scores) != set(DIMENSIONS) or any(v is not None and (type(v) is not int or v not in (0,1,2)) for v in scores.values()):
            raise ValueError('Scores must include all dimensions with 0/1/2/null')
        if type(row.get('critical_failure')) is not bool or not isinstance(row.get('evidence'),str) or not row['evidence'].strip():
            raise ValueError('Ratings require critical_failure and evidence')
        group = groups.setdefault(row['condition'], {'records':0,'critical_failures':0,'values':{d:[] for d in DIMENSIONS}})
        group['records'] += 1
        group['critical_failures'] += int(row['critical_failure'])
        for d,v in scores.items():
            if v is not None:
                group['values'][d].append(v)
    if not groups:
        raise ValueError('No ratings; no scores to report')
    for group in groups.values():
        group['dimensions'] = {d:{'n':len(v),'mean':sum(v)/len(v) if v else None} for d,v in group.pop('values').items()}
    return groups

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    prep = sub.add_parser('prepare'); prep.add_argument('--out',type=Path,required=True)
    summary = sub.add_parser('summarize'); summary.add_argument('ratings',type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            print(f'Prepared {prepare(args.out)} paired cases; no model evaluation has been run.')
        else:
            print(json.dumps(summarize(args.ratings),indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1,f'{exc}\n')

if __name__ == '__main__':
    main()
