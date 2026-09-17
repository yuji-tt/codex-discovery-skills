# Decision loop

Keep a compact state record: goal and constraints; objective/proxy; strongest hypothesis and rival; evidence quality; remaining experiment budget; next decision. Resume from this record rather than restarting the audit.

| Suspected limit | Small discriminating diagnostic |
|---|---|
| Objective mismatch | Measure goal independently during a proxy-improving intervention |
| Missing information | Add a controlled oracle signal; compare to current observations |
| Representation limitation | Test whether distinguishable required states collapse to one representation |
| Algorithmic limitation | Compare an exact small-instance solver under the same objective |
| Optimization limitation | Check convergence, conditioning, restarts, and a known reachable solution |
| Incorrect causal hypothesis | Verify manipulation then remove the claimed mediator |
| Evaluation artifact | Recompute with uncensored denominators, held-out populations, or leakage removed |
| Fundamental constraint | Establish a bound under explicit assumptions; check whether they hold |
| Insufficient evidence | Estimate uncertainty or improve the measurement before choosing a story |

These are competing diagnoses, not mandatory steps or mutually exclusive labels. Prefer a test that separates several plausible diagnoses at once without changing many factors.

Deepening gate: a coherent mechanism remains compatible with valid observations and an affordable test could resolve uncertainty. Declare predictions and kill criteria, verify the implementation, and run that test.

Transfer gate: the mechanism has been understood enough to identify its limiting structure, measurement and implementation explanations have been checked where material, and further local changes lack an informative rationale within the budget. Document this evidence; a handful of arbitrary failed hyperparameters is not enough. If the user explicitly asks for transfer earlier, label the search exploratory.

For transfer without companion skills, record entities, information, hidden state, actions, feedback, objective, constraints, timescale, failure mode, invariants, and bottleneck. Search distant mechanisms with matching relations. Require source → principle → mapping → intervention → prediction → falsification → break conditions. Reject metaphor-only candidates.

Compare the smallest resulting mechanism with the existing baseline using the same population, resource accounting, and goal-facing outcomes. Update one of objective, hypothesis, or method according to what the evidence actually identifies. Re-audit only when new evidence changes goal alignment. Stop on resolved decision, exhausted budget, or unavailable evidence; report unresolved alternatives without pretending to have run tests.
