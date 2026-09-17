import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
validate=load('validator',ROOT/'scripts/validate.py')
runner=load('runner',ROOT/'evals/run.py')

class Checks(unittest.TestCase):
    def test_repository_and_missing_skill(self):
        self.assertEqual(validate.validate(ROOT),[])
        with tempfile.TemporaryDirectory() as tmp:
            copy=Path(tmp)/'repo'
            shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','__pycache__','.eval-runs'))
            (copy/'skills/objective-audit/SKILL.md').unlink()
            self.assertTrue(any('Missing' in x for x in validate.validate(copy)))

    def test_link_and_frontmatter_regressions(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy=Path(tmp)/'repo'
            shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','__pycache__','.eval-runs'))
            p=copy/'skills/objective-audit/SKILL.md'
            p.write_text('---\nname: wrong\n---\n[bad](missing.md)\n',encoding='utf-8')
            errors='\n'.join(validate.validate(copy))
            for expected in ('name mismatch','missing description','broken link'):
                self.assertIn(expected,errors)

    def test_blinded_prompts(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            self.assertEqual(runner.prepare(out),14)
            self.assertEqual(len(list(out.glob('*.md'))),28)
            for p in out.glob('*.md'):
                text=p.read_text(encoding='utf-8')
                self.assertNotIn('must_include',text)
                self.assertNotIn('expected_route',text)
            self.assertNotIn('# Objective Audit',(out/'support-speed.baseline.md').read_text())

    def test_aggregation_rejects_invalid_and_duplicate_scores(self):
        row={'id':'support-speed','condition':'skill','run_id':'synthetic-test-only','scores':{d:2 for d in runner.DIMENSIONS},'critical_failure':False,'evidence':'Synthetic unit test, not a model result.'}
        row['scores']['structure']=None
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'ratings.jsonl'
            p.write_text(json.dumps(row),encoding='utf-8')
            result=runner.summarize(p)['skill']
            self.assertEqual(result['dimensions']['mechanism'],{'n':1,'mean':2})
            self.assertEqual(result['dimensions']['structure'],{'n':0,'mean':None})
            p.write_text(json.dumps(row)+'\n'+json.dumps(row),encoding='utf-8')
            with self.assertRaises(ValueError): runner.summarize(p)
            row['scores']['mechanism']=True
            p.write_text(json.dumps(row),encoding='utf-8')
            with self.assertRaises(ValueError): runner.summarize(p)

    def test_empty_results_do_not_invent_scores(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'empty.jsonl'; p.write_text('')
            with self.assertRaises(ValueError): runner.summarize(p)

if __name__ == '__main__': unittest.main()
