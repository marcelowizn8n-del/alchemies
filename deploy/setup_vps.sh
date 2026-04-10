#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script as root."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_ROOT="${SITE_ROOT:-/var/www/alchemies.pro/current}"
NGINX_CONFIG_SOURCE="${SCRIPT_DIR}/nginx/alchemies.pro.conf"
NGINX_CONFIG_TARGET="/etc/nginx/sites-available/alchemies.pro"

apt update
apt install -y nginx certbot python3-certbot-nginx rsync

mkdir -p "${SITE_ROOT}"
cp "${NGINX_CONFIG_SOURCE}" "${NGINX_CONFIG_TARGET}"
ln -sfn "${NGINX_CONFIG_TARGET}" /etc/nginx/sites-enabled/alchemies.pro

nginx -t
systemctl enable nginx
systemctl reload nginx

echo "VPS base setup completed."
echo "Next step: publish the site files to ${SITE_ROOT}"
echo "Then issue TLS with:"
echo "  certbot --nginx -d alchemies.pro -d www.alchemies.pro"
