#!/usr/bin/env bash
# Run the swing trading scanner
# Usage: ./scripts/run_scanner.sh [options]
# Example: ./scripts/run_scanner.sh --list lq45

set -euo pipefail

# Navigate to repo root
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Find Python - prefer venv, fallback to system
PYTHON="./venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="./venv_314/bin/python"
fi
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="$(command -v python3 || command -v python)"
fi

# Run the scanner
"$PYTHON" -m src.main "$@"
