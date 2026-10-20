# Frozen problem: open-j1j2-real-mps-v1

For L spin-1/2 sites in basis |down>, |up>, set hbar=1, J1=1,
S^z=diag(-1/2,+1/2), S^+=|up><down|. The Hamiltonian is

H = sum_{r=1,2} J_r sum_{i=0}^{L-r-1}
    (S_i^x S_{i+r}^x + S_i^y S_{i+r}^y + delta S_i^z S_{i+r}^z).

There are no fields, offsets, wrapping bonds, or imposed magnetization sectors.
The physical dimension is 2. Site zero is the most significant bit in ED.
All coefficients are the exact rational values of the decimal strings in
`benchmarks/suite.json`. This formulation includes the XXZ anisotropy listed
there. Changing any Hamiltonian, boundary, bond cap, or objective creates a
new formulation and result series.

| Split | Instance | L | J2 | delta | Maximum bond |
|---|---|---:|---:|---:|---:|
| Development | dev10 | 10 | 0.25 | 1 | 8 |
| Development | dev12 | 12 | 0.5 | 1 | 8 |
| Development | dev24 | 24 | 0.75 | 1.25 | 8 |
| Held out | hold12 | 12 | 0.375 | 1.25 | 8 |
| Held out | hold14 | 14 | 0.625 | 1 | 8 |
| Held out | hold28 | 28 | 0.875 | 1.25 | 8 |

The objective is the total energy, not energy per site. Development aggregates
energy differences per site so the long chain does not dominate selection.
The same bond cap applies to every method on each instance. Small validation
uses L=2,4,6 and no optimization information is drawn from ED.

## Witness and exact checker

A witness is a non-pickled NPZ containing A0,...,A(L-1) and hamiltonian_id.
Each real binary64 tensor has shape (left,2,right), with external bonds 1,
matching internal bonds, and bond size <= the frozen cap. Entries must be finite
and at most 2 in magnitude. This is an interchange format, not a TeNPy pickle.
Real states suffice for this real symmetric Hamiltonian. Complex witness
support is deliberately outside v1. The Hamiltonian hash covers physical
parameters; the benchmark enforces its separate bond cap.

Let v_s=A0[s0]...A(L-1)[s(L-1)]. The represented state is **exactly**
psi=v/sqrt(v^T v). The checker verifies the raw norm is within 1e-8 of one,
then uses the exact quotient v^T H v/(v^T v). It does not assume canonical
form or trust the optimizer's normalization. Floating tensor entries are
interpreted as exact binary rationals, not as uncertain real measurements.

At each site the checker scales its entries by a common power of two to
integers. It propagates integer environments for the norm, internal energy,
and X,Y,Z insertions one and two sites back. Here X=sigma_x,
Y=i*sigma_y is real, Z=2*S_z, and the interaction is
J/4 * (X X - Y Y + delta Z Z). Integer matrix products have no rounding error.
All environments acquire the same squared tensor scale, so those factors
cancel in the Rayleigh quotient. The small common coefficient denominator
is retained. Python arbitrary-precision integers and Fraction produce the
exact rational numerator and denominator. Decimal endpoints are obtained
by integer floor/ceiling at 14 decimal places, giving width <=1e-14 J1.

This establishes a rigorous numerical enclosure **conditional on the checker
implementation and ordinary integer arithmetic correctness**, not a formally
verified theorem. Tests compare it with a separately expanded rational state
and a separate bit-basis Hamiltonian. A forged energy, zero state, nonfinite
entry, wrong Hamiltonian, complex/object payload, or excess bond is rejected.
Candidate claims must agree within the fixed 1e-10 J1 print tolerance.

## What is and is not proved

The variational principle gives E0 <= <psi|H|psi>. Thus the upper decimal
endpoint is a certified variational upper bound. Lower energy is a better
upper bound for this Hamiltonian; it is not proof of optimality, wavefunction
fidelity, correct correlations, or a new physical phase.

A crude rigorous global lower bound is
-(2+delta)/4 * [J1*(L-1)+J2*(L-2)]. Each two-spin interaction has eigenvalues
J*delta/4 (twice) and J*(-delta/4 +/- 1/2). With the positive J values and
delta >=1 here, its minimum is -J*(delta+2)/4. Sum the corresponding operator
inequalities. Frustration means this lower bound need not be attainable.

ED is performed over the full 2^L-dimensional Hilbert space, using dense eigh
for L<=8 and sparse eigsh otherwise. Its residual is reported. A small
residual bounds proximity to some eigenvalue, and is not by itself a proof
that it is the least eigenvalue. The ED number is a numerical reference, never
a certified lower bound. No thermodynamic-limit result is claimed.

## Frozen computational budget

Optimization is binary64, TeNPy 1.1.0. Every run gets exactly six complete
sweeps, with Lanczos N_max=40, N_min=2, P_tol=E_tol=1e-12, svd_min=1e-14,
trunc_cut=None. No early convergence shortcut. The mixer starts at 1e-5,
decays by 10, and disables after three sweeps. Ramp uses chi 2,4,8 starting
at sweeps 0,1,2; TeNPy's default mixer reactivation applies on ramp changes.
All methods use the full physical Hilbert space (conserve=None).

Baseline: two-site DMRG, Neel product initialization, fixed chi=8.
Alternatives: same with bond ramp; same with nearest-neighbor singlet-dimer
initialization; same with seeded real product-state angles; single-site DMRG
with subspace expansion, Neel start. These are literature-supported variants,
not claims of algorithmic novelty. The driver calls TeNPy's initialization,
sweep and mixer cleanup routines explicitly to enforce exactly six sweeps;
cleanup updates its cached environments consistently. No manual environment
reset occurs between sweeps.

BLAS is limited to one thread. CPU and wall time include model construction,
initial state, updates, mixer cleanup and canonicalizing checkpoint copies; exclude scoring and checkpoint I/O.
Every sweep is saved and independently checked. The best saved state is the
run's candidate (truncation can make successive energies nonmonotonic).
Counts of local updates and Lanczos iterations are recorded. Equal sweeps
alone do not mean equal work across variants. The secondary comparison uses
best completed checkpoints under the smaller total CPU budget of each pair.
No extrapolated unfinished sweep is credited.

Methods and Hamiltonians are committed before development. Only development
energy selects the alternative; source and suite hashes are frozen in
selection.json before held-out execution. Held-out cases are public but were
not used for tuning. This is a small fixed test, not a sealed benchmark or a
claim of generalization to all frustrated systems. A/A repeats, interleaved
orders, seeds 1729 and 2718, and one-thread execution are controls. Deterministic
method repeats do not create additional independent Hamiltonian samples.

## Solved positive control at the Majumdar–Ghosh point

For even L, J2=1/2, delta=1, the adjacent-singlet product is a ground state
of this open chain with E0=-3L/8. This is a known special case, not a pilot
advance. It is useful precisely because an exact answer is available.
Write T_i=S_i+S_(i+1)+S_(i+2). Then

H = (1/4) sum_(i=0)^(L-3) [T_i^2-9/4]
    + (1/2) S_0.S_1 + (1/2) S_(L-2).S_(L-1).

Each three-spin T_i has total spin 1/2 or 3/2, so each bracketed term is
at least -3/8. The two end terms are each at least -3/8. Consequently
H >= -3L/8. The adjacent-singlet state attains every bound, as each triple
contains a singlet and each end pair is a singlet. This is a mathematical
lower-bound argument specific to the isotropic J2=1/2 control. It does not
apply to the other suite instances. The rational verifier test reproduces
its energy exactly and independently checks its full-vector residual.
The general dimer prior art includes https://arxiv.org/abs/cond-mat/0205072 .
