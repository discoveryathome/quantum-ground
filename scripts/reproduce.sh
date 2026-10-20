#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/cpu.sh -m pytest -q -p no:cacheprovider
./scripts/cpu.sh -m scripts.check_ed
./scripts/cpu.sh -m qground.check --case dev12 --witness examples/known-dimer.npz --claim -4.5
./scripts/cpu.sh -m qground.check
./scripts/cpu.sh -m scripts.check_trial
./scripts/cpu.sh -m scripts.check_supplement
./scripts/cpu.sh -m scripts.analyze > .tmp/recomputed-initial.json
./scripts/cpu.sh -m scripts.analyze_trial > .tmp/recomputed-trial.json
./scripts/cpu.sh -m scripts.validate_discovery
