#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/cpu.sh -m pytest -q -p no:cacheprovider
./scripts/cpu.sh -m scripts.validate_discovery
./scripts/cpu.sh -m qground.check
