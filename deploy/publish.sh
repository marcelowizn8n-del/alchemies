#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"
REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_HOST="${REMOTE_HOST:-72.62.12.98}"
REMOTE_PORT="${REMOTE_PORT:-22}"
REMOTE_PATH="${REMOTE_PATH:-/var/www/alchemies.pro/current}"

"${ROOT_DIR}/deploy/prepare_release.sh"

rsync \
  -avz \
  --delete \
  -e "ssh -p ${REMOTE_PORT}" \
  "${DIST_DIR}/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"

echo "Published ${DIST_DIR} to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
