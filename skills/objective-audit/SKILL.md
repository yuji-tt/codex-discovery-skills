---
name: objective-audit
description: Audit whether optimizing a stated objective or proxy advances the real
  goal. Use for suspicious metric gains, incentive failures, population mismatch,
  or before further optimization when goal alignment is uncertain; do not reframe
  routine tasks without evidence.
---

# Objective Audit

Separate the true goal (desired outcome), stated objective (requested formulation), proxy metric (observable surrogate), optimization target (quantity directly selected or trained against), evaluation metric (success check), and constraints (non-negotiable limits). Mark unknowns instead of silently equating them.

Maintain both explanations: objective misspecification and an appropriate objective with a weak solution, representation, or mechanism. Search for a concrete case where the proxy improves while the goal worsens or stays unchanged. A hypothetical loophole is a diagnostic lead, not proof of mismatch.

Check incentives, omitted variables, unintended satisfaction, evaluation versus target populations, censoring and aggregation, and silently discarded competing goals. Use [objective diagnostics](references/objective-diagnostics.md) when any check exposes ambiguity.

Choose the smallest counterexample, experiment, ablation, or diagnostic that gives different predictions under the two explanations. Specify comparison, observable outcome, and what each result changes. Preserve the objective until evidence supports a revision; a proposed revision must preserve user constraints and explicit priorities. User instructions take precedence over this protocol.

Return a short decision record: goal/metric map, competing explanations, discriminating test, decision threshold, and remaining uncertainty. If goal alignment is sufficiently established for the next action, stop auditing and proceed.
