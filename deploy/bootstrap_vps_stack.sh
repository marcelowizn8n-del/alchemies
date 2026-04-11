#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STACK_DIR="${STACK_DIR:-/opt/alchemies}"

mkdir -p "${STACK_DIR}/site" "${STACK_DIR}/nginx" "${STACK_DIR}/backend/runtime/artifacts"

"${ROOT_DIR}/deploy/prepare_release.sh"

rsync -av --delete "${ROOT_DIR}/dist/" "${STACK_DIR}/site/"
rsync -av --delete --exclude '.venv' --exclude '__pycache__' --exclude 'runtime' "${ROOT_DIR}/backend/" "${STACK_DIR}/backend/"
cp "${ROOT_DIR}/deploy/docker-compose.vps.yml" "${STACK_DIR}/docker-compose.yml"
cp "${ROOT_DIR}/deploy/nginx/default.conf" "${STACK_DIR}/nginx/default.conf"

if [[ ! -f "${STACK_DIR}/.env" ]]; then
  cat > "${STACK_DIR}/.env" <<'EOF'
ALCHEMIES_HOST_PORT=8090
NPM_NETWORK=npm_default
EOF
fi

echo "Stack files refreshed in ${STACK_DIR}"
echo "Next steps:"
echo "  cd ${STACK_DIR}"
echo "  docker compose --env-file .env up -d --build"
