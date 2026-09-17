# When a proxy rewards the wrong outcome

This synthetic scenario illustrates a diagnostic decision; the counts are invented inputs, not results from a deployed service.

## Request and metric map

A support team wants to optimize one-hour ticket closure. In the supplied scenario, 100 tickets per policy are observed. The old policy closes 60 within an hour; the new policy closes 90. Within seven days, 15 old-policy tickets and 40 new-policy tickets produce a repeat contact.

The true goal is durable resolution with acceptable customer effort. The stated objective is faster closure, the proxy is one-hour closure rate, the optimization target is the reward for closing a ticket, and the present evaluation is that same closure rate. Privacy, staffing, and service commitments are constraints. Durable resolution is not identical to absence of repeat contact: frustrated users may leave silently.

## Audit and competing explanations

Premature closure is an incentivized behavior that can improve the proxy without resolving the issue. Ticket difficulty, customer mix, or tracking changes could also explain the difference. The supplied unrandomized counts identify a counterexample to equating closure with success, but do not establish a causal effect of the policy.

The missing variables are actual resolution, repeat effort, abandonment, and case complexity. Include all assigned tickets in denominators, not only completed tickets; report cohorts and delayed outcomes. Silently excluding hard tickets would create another loophole.

## Small discriminating test

For a limited authorized trial, compare policies on randomized comparable tickets, preventing agents from selecting the easy queue. Measure one-hour closure, seven-day repeat contacts, and independently sampled resolution confirmation, including nonresponders as an explicitly unknown group. Keep staffing constant and check for spillovers if agents handle both policies.

Before running, choose a minimum practically important resolution difference, a customer-effort guardrail, and a stopping rule based on a suitable uncertainty interval. If faster closure worsens independently assessed resolution or effort beyond those thresholds, revise the incentive. If closure and resolution improve together, retain the direction and investigate case-mix explanations for the initial counts. If uncertainty is too large, improve evidence rather than choose a convenient narrative.

## Decision

Propose making durable resolution the goal-facing evaluation and using closure time as a secondary service measure, subject to the user's priorities. Do not claim the new policy caused harm from these synthetic observational counts alone. No distant analogy is needed: the next useful action is a controlled goal-facing measurement. The example shows a real logical mismatch between the proxy and the goal while preserving uncertainty about which policy actually performs better.
