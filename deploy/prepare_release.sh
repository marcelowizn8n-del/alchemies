#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"

rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"

cp "${ROOT_DIR}/index.html" "${DIST_DIR}/"
cp "${ROOT_DIR}/studio.html" "${DIST_DIR}/"
cp "${ROOT_DIR}/blueprint.html" "${DIST_DIR}/"
cp "${ROOT_DIR}/robots.txt" "${DIST_DIR}/"
cp "${ROOT_DIR}/sitemap.xml" "${DIST_DIR}/"
cp "${ROOT_DIR}/Multimodal_AI_Blueprint.pdf" "${DIST_DIR}/"
cp "${ROOT_DIR}/Gerador_de_IA_Multimodal.mp4" "${DIST_DIR}/"
cp -R "${ROOT_DIR}/assets" "${DIST_DIR}/assets"

echo "Release prepared at: ${DIST_DIR}"
