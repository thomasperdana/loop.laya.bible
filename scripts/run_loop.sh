#!/usr/bin/env bash
# run_loop.sh: Autonomous KJV Bible Study Loop Runner
# Implements Loop Engineering standards from docs/loop-engineering
#
# Usage:
#   ./scripts/run_loop.sh --chapter "Genesis 1"
#   ./scripts/run_loop.sh --book "Romans"
#   ./scripts/run_loop.sh --testament "NT"
#   ./scripts/run_loop.sh --all
#   DRY_RUN=1 ./scripts/run_loop.sh --chapter "Genesis 1"
#
# Exit codes:
#   0: DONE (All verifications passed)
#   1: General script error
#   2: CAP (Maximum iterations reached)
#   3: STUCK (Identical failure repeatedly)
#   4: HUMAN (Stopped by .loop-stop sentinel file)
#   5: DANGER (Protected system file modified)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Activate virtualenv if present
if [ -d "$ROOT_DIR/.venv" ]; then
    PYTHON="$ROOT_DIR/.venv/bin/python"
elif command -v uv >/dev/null 2>&1; then
    PYTHON="uv run python"
else
    PYTHON="python3"
fi

cd "$ROOT_DIR"

# Ensure data is initialized
if [ ! -f "data/books.json" ] || [ ! -f "progress/progress.json" ]; then
    echo "==> Initializing canonical KJV indexing..."
    $PYTHON scripts/init_data.py
fi

# Run the Loop Engine
exec $PYTHON engine/loop.py "$@"
