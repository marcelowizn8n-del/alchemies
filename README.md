# Alchemies.PRO

Premium static frontend for a multimodal AI studio focused on image and video generation.

## Included pages

- `index.html`: landing page and portal entry
- `studio.html`: interactive studio demo with generation controls and modal states
- `blueprint.html`: technical blueprint page tied to the PDF and diagram assets

## Backend foundation

- `backend/`: own API scaffold for future self-hosted image and video generation
- `OWN_API_ARCHITECTURE.md`: product and infra direction for evolving into a commercial generation service

## Main assets

- `assets/styles.css`: shared visual system and responsive layout
- `assets/app.js`: UI interactions for tabs, ratios, modal states, and demo flow
- `Multimodal_AI_Blueprint.pdf`: technical blueprint document
- `Gerador_de_IA_Multimodal.mp4`: demo video asset

## Deployment

Prepare a public bundle:

```bash
./deploy/prepare_release.sh
```

Publish to the VPS:

```bash
REMOTE_USER=root REMOTE_HOST=72.62.12.98 ./deploy/publish.sh
```

Server setup and Nginx config details are documented in `DEPLOY_VPS.md`.

## Run the API locally

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
./run_local.sh
```

Then open `studio.html` through a local static server and the studio will dispatch jobs to the API.

Example:

```bash
cd /Users/marcelo/Documents/alchemies.pro
python3 -m http.server 4173
```

Then visit:

```text
http://127.0.0.1:4173/studio.html
```

For the next architectural step, the repo now includes a private image worker scaffold. The public API can delegate image jobs to that worker while video remains inline for development.
