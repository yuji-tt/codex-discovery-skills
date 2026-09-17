# Keep the objective; deepen the algorithm

This is a synthetic worked decision record. Numerical results below are analytically derived from the specified toy problem, not measured model performance.

## Request and framing

An iterative solver reduces loss quickly and then appears to stall. The user requires minimization of the actual quadratic loss, not an indirect business proxy. Let f(x) = (x1² + 1000 x2²)/2, starting at (1, 1). The true goal, optimization target, and evaluation loss coincide on this controlled problem; compute and accuracy are constraints. A plateau is not itself evidence that the objective is wrong.

## Hypothesis and alternatives

The strongest hypothesis is poor conditioning: one global learning rate must accommodate the steep coordinate, slowing the shallow coordinate. Alternatives include an incorrect gradient, stopping too early, and measurement rounding. There is no current goal-facing counterexample that would justify changing the objective.

The mechanism predicts coordinate-specific progress. With step size 0.001, exact gradient descent gives x1(t+1) = 0.999 x1(t) and x2(t+1) = 0. Thus one coordinate disappears immediately while the other decays slowly. The apparent stall can arise from this rate disparity.

## Minimal test and ablation

Compare the fixed-step baseline with diagonal preconditioning P = diag(1, 0.001) and unit step size. Both use the same f, initial state, and exact gradients. The preconditioned update is x(t+1) = x(t) - P grad f(x(t)), which reaches (0, 0) in one step in exact arithmetic. Ablate P back to a scalar step to test whether rescaling supplies the improvement. Record coordinate residuals, objective evaluations, and any cost of constructing P; iteration count alone is not a fair production cost measure.

The manipulation check is that each coordinate receives the specified scaling. Kill this explanation for this toy case if a verified exact implementation fails its derived recurrence; investigate implementation or arithmetic first if the manipulation check fails. For a real solver, predeclare a minimum useful wall-clock improvement and account for preconditioner setup cost before testing.

## Decision

Retain the objective and deepen the conditioning diagnosis. The equations establish the toy mechanism, not its benefit on an unknown production workload. Next test representative Hessian structure and total runtime. Structural transfer would add distraction until this concrete explanation has been checked. If costly preconditioning erases the gain, that limits this implementation rather than proving every conditioning remedy invalid.
