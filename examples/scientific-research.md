# Transfer an information structure into assay design

This synthetic design exercise uses an explicitly defined mathematical model. It is not evidence that pooling works for a particular laboratory assay.

## Target signature

There are 16 candidate samples and exactly one active sample. A test on a pool returns a noiseless binary result indicating whether the active sample is present. Every pool has equal cost. The hidden state is the active index; the decisions are pool membership; the observations are binary outcomes; feedback arrives after each assay. The objective is exact identification under a small assay budget. The timescale is one assay batch. The dominant bottleneck is information per costly observation. An invariant is that candidates with identical outcome signatures cannot be distinguished.

These assumptions exclude dilution, interactions, and multiple active samples. Validate them before applying the design to physical experiments.

## Source and mapping

The donor is binary coding rather than another local assay recipe. The elementary mechanism assigns distinct bit strings to messages; observing the string identifies the message. This exercise derives that property directly and makes no historical or novelty claim.

Source mechanism → unique four-bit codewords for 16 messages.

Abstract principle → distinguish hidden states by assigning unique observation signatures; four noiseless binary outcomes can represent 16 states.

Target mapping → message is active sample index, bit position is assay pool, and bit value is inclusion in that pool. Assay outputs are the active sample's codeword.

Intervention → assign indices 0 through 15 their four-bit representations. Construct four pools, each containing the eight indices with a 1 in that bit position. Run all four assays and decode the result.

## Predictions, controls, and fastest falsification

Enumerating each possible active index should yield a distinct observed four-bit vector. For example, index 10 maps to 1010, so only its first and third pools respond under this convention. A simulation can exhaustively check all 16 states before any wet-lab work. A duplicated pool that causes two columns to coincide is a negative control for identifiability.

The information bound is 2^k >= 16, requiring at least four binary outcomes for exact identification in this model. Individual testing provides a baseline with up to 15 tests under the exactly-one assumption. Compare total sample preparation and measurement costs too; equal assay price does not imply equal practical cost.

For the first physical diagnostic, use known positive and negative controls in individual and pooled settings. Kill the noiseless model for this application if calibrated pooling changes the expected sign. Do not interpret that as a refutation of coding theory. Instead, establish an error model and ask whether extra redundant assays remain worthwhile.

## Break conditions and decision

Multiple actives combine codewords and can alias another index; false negatives, contamination, or concentration-dependent responses invalidate direct decoding. In particular, the all-zero codeword is indistinguishable from no active sample, so the exactly-one assumption is essential. This is a structural correspondence with explicit failure conditions, not the metaphor that experiments “speak a language.”

The decision is to test pooling validity and identifiability before investing in a larger assay screen. The transfer produces a minimal target mechanism and a falsifiable prediction; it does not establish a novel method or experimental benefit.
