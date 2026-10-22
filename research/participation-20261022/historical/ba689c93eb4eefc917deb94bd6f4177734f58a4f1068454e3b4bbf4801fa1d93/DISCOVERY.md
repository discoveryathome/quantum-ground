# Research and contribution contract

The exact question is: for the six frozen finite open spin-1/2 XXZ J1-J2
Hamiltonians in benchmarks/suite.json, can a method yield a strictly smaller
verified Rayleigh quotient at chi<=8, under six sweeps and comparable CPU work?
The witness is the exactly normalized state defined by real binary64 MPS tensors.
See docs/FORMULATION.md for the coefficients, basis, precision, and checker proof.

The accepted scientific baseline in the literature is DMRG/MPS optimization,
with sources and qualifications in docs/LITERATURE.md. The project frontier
records only locally generated, author-checked variational bounds. It does not
assert a literature best known value. Comparison results and the contribution
assessment live in docs/RESULTS.md. There is no evidence of global optimality.

The immediate bottleneck is reliable, budget-controlled evidence on systems
where standard DMRG has not already saturated the tiny benchmark. Weights and
cards are in discover/catalog.json. The priorities are independent replication,
verifier review, initialization/schedule ablations, and prior-art audit. Small
claims, negative results, and error reports are valuable; routine parameter
variation is not algorithmic novelty.

Every contribution must supply the base commit, task/seed, method definition,
all attempted runs and costs, immutable Hamiltonian identity, pinned dependencies,
portable NPZ states, exact verifier output, and a replay command. Do not report
only the winning seed. Compare against the mature baseline, A/A controls, and
fresh held-out cases after freezing the method. Newly designed heldouts require
a new preregistration. Current test cases are public and used once already.
Changes to evaluator/formulation require separate review and regression tests.

## Review, credit and license

**No person has agreed to maintain this pilot. Review capacity is unassigned,
and donor intake is paused.** The manifest's UNASSIGNED entry is an explicit
schema placeholder, not a named or consenting scientific maintainer. The owner
authorized repository publication and listing by discoveryathome/discover; the
manifest records listing-only consent, with no hub outreach permissions.
It cannot be opened to donors until a person agrees to review and
states their capacity. Automated verification is evidence, not acceptance.
The current review status is docs/REVIEW.md.

The prospective review procedure is: rerun witness checks in a fresh checkout;
review the physical model and checker changes; audit budgets and all attempts;
require an independently reproduced result before updating the record. The
reviewer records the scope and limitations in discover/ledger.jsonl. No reviewer
or capacity is invented here. Review capacity, rather than donated compute,
will determine the pace of a public project.

Contributors receive named attribution in CONTRIBUTORS.md and per-result records
when they choose to supply a name; source papers and software are cited.
Authorship is not promised automatically. Original code and docs use MIT.
External schemas and sources retain their provenance/license. Do not relicense
TeNPy or claim its algorithms as pilot inventions.

## Local coordination

There is no live public board. `scripts/pick.py` draws from OS randomness or a
provided 128-bit seed. The first eight hex digits select a weighted track;
the next eight select a task, matching protocol v0. Check the local
`discover/coordination.jsonl` before starting. Save claims, findings and handoffs
there and in a result note, never send them externally without authorization.
Messages end with a discover JSON block containing v, kind, scope, base,
posted_at and the relevant task/artifact/request. Handoffs need a concrete next
command, expected outcome, and time estimate. See docs/HANDOFF.md.

The verifier and frontier are the two files donors must be able to rely on.
Do not weaken either to admit a candidate. A fresh contributor can run the
positive control and one narrowly scoped experiment; broader optimization
claims need more than a short session.
