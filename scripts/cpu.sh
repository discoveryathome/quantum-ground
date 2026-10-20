#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
mkdir -p .tmp
export TMPDIR="$PWD/.tmp"
if [[ "$(uname)" == Darwin ]] && command -v sandbox-exec >/dev/null; then
  sandbox-exec -p "(version 1)(allow default)(deny network*)(deny file-write*)(allow file-write* (subpath \"$PWD\") (literal \"/dev/null\"))" .venv/bin/python "$@"
else
  exec .venv/bin/python "$@"
fi
