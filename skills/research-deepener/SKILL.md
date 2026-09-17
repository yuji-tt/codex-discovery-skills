---
name: research-deepener
description: Develop a promising research or engineering approach mechanistically
  before pivoting. Use when results are ambiguous, implementations fail, or local
  progress stalls; define predictions, ablations, and kill criteria without protecting
  a refuted idea.
---

# Research Deepener

State the candidate hypothesis as a conditional causal claim: under assumptions A, mechanism M changes outcome Y relative to baseline B. Separate essential causal components from incidental implementation choices.

Derive observable predictions, a mechanism-removal ablation, failure signatures, and explicit kill criteria before inspecting new outcomes. Choose the smallest test that separates the hypothesis from its strongest alternative. Use [depth protocol](references/depth-protocol.md) for ambiguous failures or stopping decisions.

Check that an implementation actually instantiates the mechanism before treating failure as refutation. Multiple failures sharing one broken measurement or implementation assumption are not independent evidence. Conversely, retire or narrow the hypothesis when valid tests meet its predefined kill criteria; do not move the threshold after seeing results.

Prefer a simpler explanation until added components predict an observation it cannot explain. Keep objective validity as a live uncertainty without reopening settled framing on every iteration. User instructions take precedence over this protocol.

Run the authorized informative test when feasible; otherwise label it proposed and state the missing input. Update the hypothesis with the outcome, confidence limits, and next decision. Report concise assumptions, predictions, evidence, and conclusions, not private chain-of-thought.
