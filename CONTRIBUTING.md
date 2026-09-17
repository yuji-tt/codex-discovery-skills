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

## Verify public installation before a release

Run the installed official Codex Skill installer through the smoke-test wrapper:

```sh
python scripts/smoke_install.py --ref main
```

The wrapper locates the helper under the configured Codex home. If it is elsewhere, pass `--installer /path/to/install-skill-from-github.py`. Optionally add `--official-creator /path/to/skill-creator` to run the official validator on every installed copy. No normal installed skills are changed: the wrapper uses a unique temporary destination and removes it even after failure.

The test downloads all four packages anonymously from public GitHub, validates their metadata and relative reference files, and compares every installed file with the public archive at the resolved commit. It rejects a ref that moves during verification and prints the commit, installer hash, and cleanup result. It never substitutes the local checkout for the downloaded packages. Anonymous GitHub rate limits and network availability apply; a download failure is not a passed test.

After publication, repeat with the release tag, for example `python scripts/smoke_install.py --ref v0.1.0`. A tag can be moved by a maintainer, so preserve published tags and record the resolved commit; use the full commit SHA when strict content pinning is required. If a release fails, fix forward rather than rewriting its tag.

For copies installed by a separate invocation, run `python scripts/validate.py --skills-dir /path/to/temporary/skills`. This package-only mode does not require evaluation files from the checkout. The default command still validates the whole repository. Offline unit tests cover missing packages/references, content mismatch, moving refs, and cleanup; CI runs these deterministic tests. Run the network smoke test against merged `main` before tagging and against the public release afterward, and record both actual results in the release verification report.
