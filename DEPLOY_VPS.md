# Deploy Guide for `alchemies.pro`

This project is now packaged as a static site that can be served directly by Nginx on your VPS at `72.62.12.98`.

## Recommended workflow

Use the included scripts:

1. Prepare the public bundle:

```bash
./deploy/prepare_release.sh
```

2. Publish the generated `dist/` folder:

```bash
./deploy/publish.sh
```

3. On the VPS, install and configure Nginx:

```bash
./deploy/setup_vps.sh
```

If you prefer running setup remotely without uploading the whole project first:

```bash
scp -r ./deploy root@72.62.12.98:/root/alchemies-deploy
ssh root@72.62.12.98 'bash /root/alchemies-deploy/setup_vps.sh'
```

## Files to publish

If you are publishing manually, upload the contents of `dist/`, especially:

- `index.html`
- `studio.html`
- `blueprint.html`
- `robots.txt`
- `sitemap.xml`
- `assets/`
- `Multimodal_AI_Blueprint.pdf`
- `Gerador_de_IA_Multimodal.mp4`

## DNS

Create these DNS records:

- `A` record for `@` -> `72.62.12.98`
- `A` record for `www` -> `72.62.12.98`

## Suggested server path

Use a dedicated document root such as:

```bash
/var/www/alchemies.pro/current
```

## Upload example

From your local machine:

```bash
REMOTE_USER=root REMOTE_HOST=72.62.12.98 ./deploy/publish.sh
```

## Nginx setup

1. Run [setup_vps.sh](/Users/marcelo/Documents/alchemies.pro/deploy/setup_vps.sh) as `root`, or copy [alchemies.pro.conf](/Users/marcelo/Documents/alchemies.pro/deploy/nginx/alchemies.pro.conf) to `/etc/nginx/sites-available/alchemies.pro`
2. If doing it manually, create the symlink:

```bash
ln -s /etc/nginx/sites-available/alchemies.pro /etc/nginx/sites-enabled/alchemies.pro
```

3. Test and reload:

```bash
nginx -t
systemctl reload nginx
```

## TLS with Certbot

After DNS resolves to the VPS:

```bash
certbot --nginx -d alchemies.pro -d www.alchemies.pro
```

## Recommended VPS packages

```bash
apt update
apt install -y nginx certbot python3-certbot-nginx
```

## Notes

- This is a static frontend build with no backend dependency.
- File uploads in the studio are demo-level browser interactions only.
- The public deployment bundle is generated in `/Users/marcelo/Documents/alchemies.pro/dist`.
- If you later add an API, keep Nginx serving the static files and reverse proxy `/api` to the application service.
