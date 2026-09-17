# Initial validation record

Validated locally on 2026-09-17 with Python 3.13 and PyYAML 6.0.3.

- Created all four skill folders with the installed official Skill Creator initializer and generated their UI metadata with its generator.
- Official `quick_validate.py`: all four skills passed. Validator SHA-256: `6068513d924ed3559e186dfcdead7439129828dcf402167fd925c06dffbf2806`.
- Repository validation: four skills, required frontmatter, matching names, UI metadata, scaffold detection, relative Markdown file links, and 14 case schemas passed.
- Five unit tests passed, covering missing skills, malformed metadata, broken links, prompt preparation without expected-answer fields, score aggregation, duplicate/invalid ratings, and empty results.
- Prepared 14 paired cases (28 prompts). No model-response benchmark or comparative performance evaluation was run.
- PowerShell publication script parsed successfully. Its GitHub-dependent path has not been run because GitHub CLI is unavailable in the creation environment.
- Reviewed skill boundaries, objective/depth tradeoffs, transfer mappings, examples, and the staged Git diff. Whitespace checks passed.

CI is configured but cannot be reported as passed before a remote workflow actually runs. Relative-link validation checks file targets for inline links; it does not validate remote URLs, anchors, or reference-style links.

## Publication recovery

Install GitHub CLI, authenticate as `yuji-tt` with `gh auth login`, and run the included [publication script](scripts/publish.ps1) from PowerShell:

```powershell
./scripts/publish.ps1
```

The script creates the public repository when no origin exists, pushes the clean `main` commit, fetches it, compares commit IDs, checks public visibility, and lists the remote tree. It stops on failure and does not overwrite an existing repository. Release creation is an optional command printed after verification; run it only after remote CI passes.
