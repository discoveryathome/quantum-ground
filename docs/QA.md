# Author fresh-checkout verification

On 2026-10-20, cloned the local repository at commit
`8fccd91cb1eae252902d658f18b84bbcaddff5f7` into a separate directory and installed
all 24 pinned packages in a new venv, using cached wheels. Screen: no findings.
This is the author's replication, not an independent contributor's review.

`./scripts/reproduce.sh` passed in **57.64 seconds** on the recorded Mac:

- 17 tests, including independent exact-rational contractions, malformed inputs,
  model-vs-bit-Hamiltonian checks and all six single-site checkpoint exports.
- Six full-Hilbert-space numerical ED references: energy agreement below 1e-10
  J1 and residual norms below 1e-9. These are numerical reference checks, not
  certified global lower bounds.
- 80 saved-state checks: 48 initial winners, 21 contributor winners, nine
  supplemental winners, one longer-run reference and one exact dimer control.
  These are checks, not 80 distinct states; some runs produce identical states.
- Frozen source/artifact hashes, recomputed comparisons, and metadata schemas.

All four catalog first-step commands passed; the reproduction command above
is the replication card's first step. A new optimizer run of dev10 hybrid_polish
also passed, including all six exact checkpoint checks and final energy drift
below 1e-9 J1 relative to the archived run. This smoke replay is not a second
run of the entire search. The original search recorded and checked all 492
checkpoints as it ran; the replay commands retain all attempts and seeds.

TeNPy emitted two harmless test warnings about a future mandatory
`unit_cell_width` argument; its default is correct for these chains.
A preliminary distribution screen found generated pytest temporary symlinks
accidentally tracked from setup. Those generated artifacts were excluded before
this clean-checkout run; no frozen scientific code or results changed.

The tested checkout remained clean after reproduction. Later commits add this
receipt and clarify documentation/catalog text; the scientific source and
saved results remain at the tested hashes. Raw logs and command receipts are
in [results/qa](../results/qa/). Protocol helper validation reports conformant.
No external acceptance, cross-platform validation or publication is implied.
