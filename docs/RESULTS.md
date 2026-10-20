# Initial pilot: measured results

The development-selected method was **ramp**. On three held-out Hamiltonians, each run twice, it recorded **4 wins, 0 ties, 2 losses** against fixed-chi two-site DMRG at six sweeps. At common per-pair CPU ceilings: **4 wins, 0 ties, 2 losses**.

The selected ramp did not improve mean held-out energy per site in this initial test.

A win requires an exact interval separation exceeding 1e-10 J1. Two repeats of a deterministic method are not two independent Hamiltonians. These are local benchmark results, not scientific novelty or a claim of universal superiority.

| Held-out case | Baseline energy | Ramp energy | Energy reduction | Candidate/baseline CPU |
|---|---:|---:|---:|---:|
| hold12 | -4.950164216940 | -4.950164283007 | 6.60673e-08 | 1.010 |
| hold14 | -5.352363954889 | -5.352363999759 | 4.48703e-08 | 0.861 |
| hold28 | -13.307192030235 | -13.307191469222 | -5.61013e-07 | 1.043 |

Mean held-out improvement per site: -3.7751842e-09 J1 at equal sweeps; -3.8355943e-09 J1 at common CPU ceilings.
Largest A/A energy difference: 0 J1. A/A CPU ratios ranged from 0.924 to 1.130. Other machine workloads were active; wall-time speedups are not established.

## Exact diagonalization controls

| Case | Numerical ED energy | ED residual norm | Best initial candidate minus ED |
|---|---:|---:|---:|
| dev10 | -3.925836271515 | 2.59e-15 | 1.06261e-05 |
| dev12 | -4.500000000000 | 6.22e-15 | -5.32907e-15 |
| hold12 | -4.950195339221 | 5.34e-15 | 3.10562e-05 |
| hold14 | -5.352531743995 | 3.92e-15 | 0.000167744 |

ED operates over the full Hilbert space. Its residual is a numerical diagnostic, not a global lower-bound certificate. The isotropic J2=1/2 control additionally has the known exact bound E0=-3L/8, derived in FORMULATION.md. Small negative ED gaps at roundoff scale have no physical significance.

## Search accounting

The initial search contains 30 development runs and 18 held-out/control runs, with six saved checkpoints per run (288 checkpoints). All checkpoints passed independent exact-integer energy and normalization checks.
Total measured optimizer CPU: 134.2 s. Optimizer wall time: 955.8 s. Separate exact verification wall time: 527.3 s. These omit environment setup, imports, ED, failed setup attempts and agent reasoning; all such work still belongs to session cost.

Seeds: 1729 and 2718. Source and suite hashes precede held-out evaluation in selection.json. Parameters, traces, states, A/A comparisons, CPU and wall times, Lanczos iterations and update counts are in results/pilot/. Failed pre-dataset setup attempts are described in OPERATIONS.md.

## Interpretation and follow-up

A tighter variational upper bound is real progress on the frozen benchmark. It does not establish a new physical result, a true ground-state energy, or a generally superior algorithm. This small experiment has no confidence interval for a population of Hamiltonians. Public fixed test cases should be replaced before subsequent adaptive tuning.

The initial method menu was not exhaustive. The timed contributor test adds structured starts, coupling continuation, and two-site-to-one-site polishing. See [the contributor report](../research/contributor-001/README.md) and [featured-pilot assessment](FEATURE_ASSESSMENT.md). The record table may include later checked contributor states on the same development instances; those do not alter this frozen initial benchmark comparison.

Evidence level: author-checked. An independent code path checked states, but no independent contributor or maintainer has accepted them.
