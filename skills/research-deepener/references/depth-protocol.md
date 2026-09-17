# Depth protocol

Use for failure interpretation and bounded persistence.

1. Write H: “Under A, component C changes mediator M, producing outcome Y versus B.” Specify the simplest rival explanation.
2. Separate C's essential action from optimizer, architecture, parameterization, and numerical choices. Name a manipulation check showing C actually operated.
3. Predict both mediator and outcome. A better score without the predicted mediator may indicate another cause.
4. Remove or neutralize C while matching resources and other conditions. Add a positive control where the mechanism should work and a negative control where it should not.
5. Predeclare a resource budget, meaningful effect threshold, repeat/noise handling, and a kill rule conditional on a valid manipulation and measurement. Use problem-appropriate values rather than universal trial counts.
6. Run the smallest informative test. Log the setup, baseline, observed result, uncertainty, and whether the manipulation check passed.

| Observation | Update |
|---|---|
| Manipulation absent | Repair implementation within the budget; no mechanism verdict |
| Mediator changes, outcome does not | Challenge mediator-to-outcome link or scope |
| Outcome improves, mediator absent | Investigate rival explanation |
| Valid tests meet kill rule | Retire or narrow H; do not silently relax the rule |
| Noise overwhelms predicted effect | Improve measurement or stop as unresolved |

Repeated failures from a shared defect count as one failure mode. Do not excuse independent, valid refutations by indefinitely inventing implementation problems. If the budget ends before a valid test, stop as unresolved; preserve the hypothesis record without claiming it remains likely.

Example kill-rule form: after verified manipulation, if the uncertainty interval excludes the minimum useful gain across the prespecified target conditions, stop developing this mechanism for those conditions. Distinguish a mechanism being false from an effect being too small to matter.
