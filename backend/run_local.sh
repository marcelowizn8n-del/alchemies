#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${SCRIPT_DIR}"

python3 -m uvicorn app.main:app --app-dir "${SCRIPT_DIR}" --reload --host 127.0.0.1 --port 8010
