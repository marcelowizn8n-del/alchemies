# Deploy Guide for `alchemies.pro`

This project is packaged as a static site.

There are two deployment modes in this repo:

- `Safe Docker + Nginx Proxy Manager`: recommended for your current VPS, because ports `80` and `443` are already owned by `nginx-proxy-manager`
- `Host Nginx`: only for clean servers where no other reverse proxy is already managing public traffic

For your current VPS, use the safe Docker flow below and do **not** run `setup_vps.sh`.

## Current VPS recommendation

Your server already has:

- `nginx-proxy-manager` on ports `80`, `81`, and `443`
- `n8n` on `5678`
- other running workloads

So the safe path is:

1. keep `nginx-proxy-manager` as the public reverse proxy
2. run Alchemies web, API, and image worker in dedicated containers
3. bind only the web container to `127.0.0.1:8090`
4. keep the API and image worker private inside Docker only
5. attach the web container to the same Docker network used by `nginx-proxy-manager`
6. create a new Proxy Host in NPM for `alchemies.pro`

## Recommended workflow

Use the included scripts for the site bundle:

1. Prepare the public bundle:

```bash
./deploy/prepare_release.sh
```

2. Publish the generated `dist/` folder:

```bash
./deploy/publish.sh
```

3. Deploy the isolated Docker services on the VPS using:

- `deploy/docker-compose.vps.yml`
- `deploy/nginx/default.conf`
- `deploy/bootstrap_vps_stack.sh`

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
/opt/alchemies/site
```

## Upload example

From your local machine:

```bash
REMOTE_USER=root REMOTE_HOST=72.62.12.98 REMOTE_PATH=/opt/alchemies/site ./deploy/publish.sh
```

## Safe Docker setup for your VPS

Use:

```bash
deploy/docker-compose.vps.yml
```

And:

```bash
deploy/nginx/default.conf
```

This keeps Alchemies isolated from the host Nginx and from the other containers.

The production flow is:

- NPM -> `alchemies-web`
- `alchemies-web` -> `/api/*` proxied internally to `alchemies-api`
- `alchemies-api` -> private `alchemies-image-worker` for image jobs
- `alchemies-api` keeps video placeholder processing inline for now
- `alchemies-image-worker` writes artifacts privately inside the stack

## Nginx Proxy Manager

In NPM, create a new Proxy Host:

- Domain Names: `alchemies.pro`, `www.alchemies.pro`
- Scheme: `http`
- Forward Hostname/IP: `alchemies-web`
- Forward Port: `80`
- Enable:
  - `Block Common Exploits`
  - `Websockets Support`
- Then request an SSL certificate in NPM for both domains

## Recommended VPS packages

```bash
apt update
apt install -y docker.io docker-compose-plugin rsync
```

## Notes

- This is a static frontend build with no backend dependency.
- File uploads in the studio are demo-level browser interactions only.
- The public deployment bundle is generated in `/Users/marcelo/Documents/alchemies.pro/dist`.
- If you later add an API, keep it in a separate service and route it independently.
- The host-Nginx files remain in the repo, but they are not the recommended path for this VPS.
- The VPS stack now supports a private `alchemies-api` service and a private `alchemies-image-worker` behind the existing `alchemies-web` container.
