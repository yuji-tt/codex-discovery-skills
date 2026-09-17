# Contributing

Explain the observed failure, the intended decision change, and a case that distinguishes improvement from added verbosity. Prefer a narrow correction over another universal rule. Follow [AGENTS.md](AGENTS.md).

Use Python 3.10 or later and install `requirements-dev.txt`. Run:

```sh
python scripts/validate.py
python -m unittest discover -s tests
python scripts/validate.py --official-creator /path/to/installed/skill-creator
```

The final command invokes that installed official creator's `scripts/quick_validate.py` for each skill in addition to repository checks. On a default installation the creator lives under `$CODEX_HOME/skills/.system/skill-creator`, or `~/.codex/skills/.system/skill-creator`. CI runs the independent repository checks without downloading a mutable validator; contributors must run the installed official validator locally and record its version or date in the PR.

For meaningful behavioral changes, update [cases](evals/cases.yaml), run affected prompts using the [rubric](evals/RUBRIC.md), and distinguish actual observations from planned tests. Report model/configuration, commit, available tools, and limitations. Do not commit private prompts, credentials, or unreviewed model outputs.
