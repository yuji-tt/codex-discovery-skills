# Objective diagnostics

Use this record when metric improvement and user benefit may diverge.

| Layer | Record | Distinguishing question |
|---|---|---|
| True goal | Stakeholder outcome and population | Who benefits, over what horizon? |
| Stated objective | User's formulation | Is this a requirement or a working hypothesis? |
| Proxy | Observable substitute | What outcome can move independently of it? |
| Optimization target | Loss, reward, or selection rule | What behavior receives pressure? |
| Evaluation | Held-out success measure | Is it independent of the optimized signal? |
| Constraints | Resources, safety, fairness, deadlines | Which tradeoffs are disallowed? |

Ask what behavior the objective incentivizes, which important variable is absent, and whether a loophole satisfies it unintentionally. Check whether evaluation matches deployment, whether censoring excludes failures, whether aggregation hides subgroup harm, and which competing objectives disappeared.

For a suspected loophole, construct a paired comparison with similar proxy values but different goal outcomes, or an intervention that improves the proxy while measuring the goal independently. For method weakness, use a known feasible solution or controlled synthetic task as a positive control. Prefer these to changing the objective and algorithm simultaneously.

Predeclare the smallest practically meaningful goal change, population, observation horizon, and uncertainty requirement. If proxy gain accompanies goal loss under a valid comparison, consider a revised proxy or constraint. If both improve but the current method misses a known achievable result, deepen the method. If measurement is unreliable or the comparison is confounded, repair evaluation before either conclusion.

An audit ends with retain, revise-proposal, or unresolved plus one discriminating diagnostic. Do not treat absence of evidence as proof of alignment, and do not make repeated speculative reframing a prerequisite to useful work.
