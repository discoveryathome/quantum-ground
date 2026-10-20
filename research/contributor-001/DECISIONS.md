# Reasoning log

2026-10-20, before any fresh test draw:

1. Initial development suggests that more sweeps on tiny cases often hit a
   common fixed-bond plateau, while chi ramping helps the 24-site chain.
2. Hypothesis A: next-neighbor singlets may initialize the strongly frustrated
   regime better by respecting the two interleaved chains.
3. Hypothesis B: two sweeps near the dimer point followed by four at the target
   may navigate a more favorable path. Intermediate states are always scored
   on the frozen target, and all work is charged.
4. Hypothesis C: single-site DMRG from a product state underperformed, but this
   does not test single-site polishing after the bond space has grown. Two-site
   minimization followed by SVD truncation can stall above a fixed-bond
   variational optimum. Test three two-site sweeps followed by three one-site
   sweeps, without a mixer in the polishing phase. This is established DMRG
   practice applied to the current resource constraint, not a new algorithm.

No fresh held-out Hamiltonian existed when these hypotheses were chosen. The
code and selection hash are frozen before the random test draw. The initial
pilot's held-out outcomes are not used to choose these hypotheses. Three
hypotheses, not an unreported grid of parameter settings, are tested. Existing
ramp/dimer/random/single-site development results remain eligible fallbacks.
