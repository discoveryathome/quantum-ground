# Evidence brief, checked 2026-10-20

The question is whether short, CPU-scale contributions can improve an exact
variational energy at fixed representation and comparable work. It is meaningful
as a local benchmark. There is no sourced universal best energy or universally
best optimizer across this custom finite suite; no world-record claim is made.
The established frontier is mature DMRG/MPS optimization, not a new discovery
by this project. Local records must not be mistaken for literature records.

Primary sources:

1. U. Schollwoeck, *The density-matrix renormalization group in the age of matrix
   product states*, Annals of Physics 326 (2011),
   https://arxiv.org/abs/1008.3477 . Foundational MPS/DMRG review. It motivates
   alternating tensor optimization and explains why this is already a mature
   one-dimensional method.
2. S. R. White, *Density matrix renormalization group algorithms with a single
   center site*, PRB 72, 180403 (2005),
   https://arxiv.org/abs/cond-mat/0508709 . Density-matrix correction addresses
   incomplete environments and sticking; improvements there do not establish
   improvements on this suite.
3. C. Hubig et al., *A Strictly Single-Site DMRG Algorithm with Subspace
   Expansion*, PRB 91, 155115 (2015), https://arxiv.org/abs/1501.05504 . Basis
   enrichment motivates the single-site comparison. Its reported speedups
   have model-specific conditions and are not imported as pilot results.
4. J. Hauschild et al., *Tensor network Python (TeNPy) version 1*, SciPost
   Physics Codebases 41 (2024), https://doi.org/10.21468/SciPostPhysCodeb.41 .
   Mature implementation used for the baseline, not for independent scoring.
5. TeNPy model reference:
   https://tenpy.readthedocs.io/en/latest/reference/tenpy.models.spins_nnn.SpinChainNNN2.html .
   Confirms nearest and next-nearest XXZ couplings. The actual audited source
   is release v1.1.0, commit 3c3304e2a7a1b90a9cd983c095da6678b9e7d2b1:
   https://github.com/tenpy/tenpy/tree/3c3304e2a7a1b90a9cd983c095da6678b9e7d2b1 .
6. TeNPy DMRG protocol:
   https://tenpy.readthedocs.io/en/latest/intro/dmrg-protocol.html . Supports
   model checks, staged chi schedules and convergence checks; exhausting a
   sweep cap alone is not evidence of convergence.
7. S. Kumar et al., *Numerical study of incommensurate and decoupled phases
   of spin-1/2 chains with isotropic exchange J1,J2 between first and second
   neighbors*, https://arxiv.org/abs/1603.02108 . Confirms ED/DMRG use in the
   frustrated chain. Its thermodynamic/phase conclusions are not benchmark
   scores for these finite open XXZ instances.

Claim audit of the supplied problem:

- Small spin chains are practical ED validation cases: confirmed by the
  explicit 2^L matrix sizes and local ED tests, with the literature above as
  context. This does not extend to arbitrary L.
- MPS can represent larger candidates: confirmed by saved 24/28-site
  representations of bounded bond size; representability does not imply
  arbitrary accuracy at chi=8.
- TeNPy is suitable for this baseline: confirmed by its model/DMRG APIs and
  independent Hamiltonian checks. Its presence alone does not validate a run.
- A new method will beat DMRG at equal cost: a research hypothesis, not an
  established premise. Selection and held-out results decide only this pilot.
- Better variational energy proves the true ground energy: false in general;
  the exact checker certifies only a normalized state's Rayleigh quotient.

Settled constraints and common dead ends:

- A one-site update without basis expansion cannot grow a product state's
  bond space. The tested single-site method includes the mixer.
- Changing J2, boundary conditions, chi, or field changes the problem; lower
  energy then is not progress on the same record.
- More seeds and more sweeps cost compute; best-of-many cannot be compared
  to one baseline run without charging the whole search budget.
- ED residuals, discarded weight, and apparent energy convergence are useful
  diagnostics but are not stand-alone global optimality certificates.
- Small instances can saturate available accuracy, leaving no meaningful
  improvement. A negative result here does not rule out benefits on harder
  chains. Broader tensor ansatze remain speculative follow-up work.

The literature search is a targeted baseline audit, not an exhaustive survey
of all 2026 optimizers. It establishes prior art for every tested direction;
any future novelty claim needs a fresh, broader audit.
