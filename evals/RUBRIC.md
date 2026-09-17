# Behavioral evaluation rubric

No model scores have been measured for this initial suite. Structural validation and harness tests are not evidence of behavioral improvement. Cases are small synthetic probes, not a representative benchmark.

Score each applicable dimension 0 (absent or contradicted), 1 (present but vague or incomplete), or 2 (specific and decision-relevant). Use null for a dimension genuinely irrelevant to the case, with a reason. A routine exact-output task may have mostly null dimensions; judge instruction compliance separately.

| Dimension key | Full-credit observable behavior |
|---|---|
| objective_goal | Separates real goal, optimized proxy, and constraints where relevant |
| mechanism | Identifies causal mediator and meaningful rival explanation |
| persistence | Deepens plausible ideas without excusing valid refutations |
| plateau | Distinguishes an evidenced limit from noise or invalid implementation |
| structure | Maps relationships and assumptions; rejects invalid or unnecessary analogies |
| falsifiability | Names an observation that changes or rejects the claim |
| simplicity | Chooses a small diagnostic before complex redesign |
| implementability | Specifies feasible comparison, measurements, and resource needs |
| calibration | Separates supplied facts, inferences, hypothetical outcomes, and uncertainty |

## Procedure

1. Run `python evals/run.py prepare --out .eval-runs/prompts`. Each skill prompt includes its skill and references, but no expected answer. Baseline prompts contain only the case request. This tests supplied-content behavior, not automatic skill discovery.
2. Run both conditions in fresh tasks with the same model, tools, and budget; randomize order. For discovery testing separately, install the skills and provide only the request, then record whether the correct skill triggered.
3. Save the actual response and metadata: case ID, condition, model, commit, tool availability, run date, and sampling settings if exposed. Use repeated runs for any comparative claim.
4. Have a reviewer apply the case's `must_include` and `must_avoid` criteria and the nine dimensions. Record brief observable evidence, not hidden reasoning. A fabricated experiment, violation of explicit instructions, or invalid analogy presented as established is a critical failure. Second-review disagreements before making claims.
5. Store JSONL records with `id`, `condition` (`baseline` or `skill`), `run_id`, `scores` (all nine keys, values 0/1/2/null), `critical_failure` (boolean), and `evidence` (nonempty text). Include provenance fields above alongside them. Null ratings require an explanation in evidence.
6. Aggregate with `python evals/run.py summarize .eval-runs/ratings.jsonl`. The report shows per-condition counts and per-dimension means over applicable ratings, separately from critical failures. It rejects duplicate run records and invalid ratings. It does not infer statistical significance or causal improvement.

Expected routes guide reviewers, not rigid wording checks. Accept alternative feasible diagnostics that discriminate the same explanations. Do not reward length, terminology matching, or forced use of all modes. API credentials are not needed by this harness; response generation is manual in Codex or through a separately configured runner. Never substitute synthetic outputs for measured model responses.
