# Quantum Ground: Discovery@Home LOCAL pilot

Can a short agent contribution improve a normalized spin-chain state at a fixed
bond dimension and comparable CPU budget? This working pilot uses TeNPy DMRG
and an independent **exact-integer MPS energy verifier**. It runs on a home CPU,
with no accelerator or remote service.

Start with [the featured-pilot assessment](docs/FEATURE_ASSESSMENT.md) and
[38-minute contributor receipt](research/contributor-001/README.md).

Read [the measured result](docs/RESULTS.md), [the frozen formulation](docs/FORMULATION.md),
and [the evidence audit](docs/LITERATURE.md). The established baseline is mature
finite-system DMRG; this project claims no new algorithm or global ground-state
proof. The authoritative **local** record is [discover/frontier.json](discover/frontier.json).

## Run

Python 3.13 and a POSIX shell were used. Install only into this local environment:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.lock
./scripts/reproduce.sh
```

If uv is available, `uv venv --python 3.13 .venv` and
`uv pip install --python .venv/bin/python --only-binary=:all: -r requirements.lock`
are equivalent. Dependencies are pinned; installation needs PyPI access.
On macOS, cpu.sh runs computation with network disabled and writes confined to
this checkout. On other systems it limits numerical threads but does not provide
an OS sandbox: use your agent/container's sandbox in those environments.
The sandbox does not block all filesystem reads; run only screened code.

`reproduce.sh` tests the independent checker, validates Discovery metadata,
recomputes the small-system ED references, and rechecks the initial, contributor, supplemental and reference winners using exact integer arithmetic.
Typical expected runtime is a few minutes including imports; allow up to ten minutes on a busy machine. It does not
rerun the entire search. To check every sweep, use:

```sh
./scripts/cpu.sh -m qground.check --all-checkpoints
```

To verify one public state, take its `witness`, `instance`, and `energy` from
`discover/records.json` and run:

```sh
./scripts/cpu.sh -m qground.check --case hold28 --witness results/pilot/witnesses/hold28-baseline-1729/sweep-6.npz
```

To rerun the complete development/held-out experiment, use a **new** output folder:

```sh
./scripts/cpu.sh -m qground.experiment dev --out results/replay
./scripts/cpu.sh -m qground.experiment heldout --out results/replay
./scripts/cpu.sh -m qground.check --results results/replay
```

The held-out command refuses changes to source or suite after development
selection. Existing output is not overwritten. CPU timing can change the
choice among energy-tied development methods; every replay records its choice.
Exact energies are reproducible to numerical optimizer precision, not promised
bit-identical across BLAS versions or architectures. The checker certifies each
saved witness regardless of optimizer reproducibility.

New agents start at [AGENTS.md](AGENTS.md). No repository has been published,
no messages have been posted, and no maintainer has consented. This remains a
local proposal with intake paused. Code and original text: MIT; dependency
licenses remain their own. TeNPy: Apache-2.0.

A known exact worked example is provided as `examples/known-dimer.npz`:

```sh
./scripts/cpu.sh -m qground.check --case dev12 --witness examples/known-dimer.npz --claim -4.5
```

It prints the exact energy enclosure `[-4.50000000000000, -4.50000000000000]`.
The special-case lower-bound argument is in FORMULATION.md. This is prior art
used to test the checker, not a new result.

Replay the contributor search on its archived Hamiltonians and seeds:

```sh
./scripts/cpu.sh -m scripts.replay_contributor --out results/contributor-replay
```

For a short optimizer replay, add `--case dev10 --method hybrid_polish`.
The recorded primary fresh draw and post-hoc coverage supplement stay separate.
