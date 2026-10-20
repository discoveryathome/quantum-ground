# Featured-pilot assessment

**Recommendation: keep this as a promising secondary or incubation pilot; do
not lead the launch with the current benchmark as a scientific flagship.**
There is a real initial improvement path, excellent verifiability and a strong
quantum-computing-adjacent story. This test does not establish a durable supply
of meaningful improvements once standard DMRG refinements are in the baseline.

The experiment portion lasted **38.4 minutes**. This was a prepared-environment
trial by the same agent that built the harness, not an independent onboarding
study. Packaging and clean-checkout checks followed separately. The full
receipt is [research/contributor-001/README.md](../research/contributor-001/README.md).

## What the trial actually demonstrated

Three hypotheses were tested on development cases, with every attempt retained.
The successful choice used three two-site sweeps to grow the tensor space,
then three fixed-bond single-site sweeps to polish it. The first three states
match the baseline exactly; the gains begin when the update strategy changes.
This directly targets the loss introduced by two-site truncation.

On the 24-spin development case:

- Original six-sweep baseline: -10.541881027392.
- Previous best ramp result: -10.541909758937.
- Six-sweep hybrid result: -10.541985281872.
- Best state from 24 ordinary baseline sweeps: -10.541881027392.

All use the same Hamiltonian and maximum bond dimension 8. Thus a targeted
change improved the local incumbent by about 7.55e-5 J1, while four times as
many ordinary sweeps did not close the gap. This is a useful example of agent
reasoning contributing something beyond launching a longer solver run. The
technique itself is established DMRG practice; this is not a new algorithm.

The first fresh random draw landed on a known exactly dimerized line at all
three sizes. It was independently reproduced from its recorded seed, preserved,
and gave **three final-energy ties**. The selected method was not retuned.
A separate, explicitly **post-hoc stratified coverage test** then gave:

| New case | Energy reduction vs baseline | Equal-sweep result | Common-CPU result |
|---|---:|---|---|
| 16 spins, J2=0.3125, delta=1.25 | 5.24e-6 J1 | Win | Win |
| 20 spins, J2=0.5625, delta=1 | 9.45e-7 J1 | Win | Win |
| 32 spins, J2=0.8125, delta=1.25 | 9.58e-5 J1 | Win | Win |

The hybrid also beat the earlier ramp method on all three supplemental cases.
Its recorded process CPU was 0.95, 0.87 and 0.96 times the baseline, respectively.
Those ratios are not established speedups: other workloads were active, and
initial A/A CPU ratios ranged from 0.92 to 1.13. The common-CPU comparison uses
only states completed under the same per-pair ceiling.

For the 16-spin supplemental case, the gap above the numerical ED reference
fell by about **2.86%**. We do not know the ground-energy error for the larger
cases. Small energy gains can matter, but this experiment does not connect
them to a new physical prediction or phase.

## Assessment against the launch criteria

| Criterion | Judgment | Evidence and limit |
|---|---|---|
| Early tangible progress | Promising, with limited demonstrated depth | A verified incumbent improvement appeared after 24.9 minutes; a standard polishing step gave transferable gains in the supplement. Sustained gains after incorporating that step remain untested. |
| Agent reasoning matters | Some direct evidence | The agent diagnosed a truncation plateau and tested a different update schedule. A 24-sweep reference helps distinguish it from simply adding iterations. There is no matched-budget agent-versus-random-search study. |
| High-end home PC feasibility | Strong | CPU-only; one numerical thread; 24 GiB arm64 Mac used. Six-sweep runs generally took about 1–7 process CPU seconds. The exact verifier works on compressed states, without expanding the 32-spin Hilbert space. Linux/Windows have upstream wheels but were not tested here. |
| Public explanation and demo | Strong topic, moderate visible payoff | “Improve a quantum magnet and submit a checkable state” is clear. A 32-spin state has billions of amplitudes; these restricted MPS approximations store thousands of numbers. The actual improvements need an honestly scaled energy chart, not a claim of a quantum breakthrough. |
| Meaningful scientific results | Not yet demonstrated | These are well-studied uniform one-dimensional models and known algorithms. We verified tighter variational bounds for this constrained benchmark, not a literature record, a new phase, or a general ground-state proof. |
| Scalable review | Good technical basis, not operationally ready | Exact witness scoring is cheap and reproducible. No independent person has audited the checker, no maintainer has consented, and review capacity is unassigned. |

## Why I would not make this the headline pilot yet

The easy improvement was available because the initial method menu did not
include a standard polishing step. A strong launch baseline should include
that step. Beating the earlier menu then stops being a recurring contribution.
Two small development cases already showed little or no algorithmic headroom;
one is solved exactly. The primary fresh draw also demonstrated the need for
benchmark coverage controls. Adding more easy rows would create activity
without demonstrating a research frontier.

The promising part is the verification infrastructure: each binary64 tensor
entry is treated as an exact rational, and an independent integer contraction
certifies its normalized state's energy to an outward decimal interval. This
makes a submitted improvement inspectable and replayable. The certification
is conditional on the checker implementation, which needs independent review;
it is not a formal proof assistant result.

## Conditions for featuring it

1. Establish a stronger baseline portfolio including hybrid polishing, ramps,
   structured starts and convergence references. Freeze its costs and outputs.
2. Build a stratified suite with informative difficulty, explicit solved controls,
   development cases, and new held-out cases. Do not reuse this session's exposed
   tests for future adaptive selection.
3. Run at least three independent 30-minute contributor sessions against that
   upgraded baseline. Look for repeatable, held-out improvements or substantive
   verifier findings, and report failed sessions as well as successes.
4. Recruit a quantum many-body maintainer to audit the physical model, checker,
   materiality of the gains and review workload. Before scaling to larger bond
   dimensions, measure exact-verifier cost: its integer arithmetic becomes more
   expensive with tensor size and chain length.

A suitable public framing now is **“Can agents improve a checkable approximation
to a quantum magnet?”** Keep it as a secondary demo or research incubation
project until the stronger-baseline test establishes continuing contribution
yield. Do not promise new materials or newly solved quantum ground states.

The [primary-test figure](contributor-demo.png) retains the ties. The
[coverage-supplement figure](contributor-supplement.png) shows the positive
results and is explicitly labeled post-hoc. [DEMO_CONCEPT.md](DEMO_CONCEPT.md)
explains how to present solver progress, contributor progress and scientific
novelty separately.
