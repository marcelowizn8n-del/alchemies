# Alchemies API

This backend is the foundation for Alchemies.PRO to operate as its own generation service instead of depending on third-party generation APIs.

## Goal

The API should become the product boundary for:

- authentication
- billing and quotas
- generation job creation
- orchestration across image and video workers
- artifact metadata and delivery URLs
- future fine-tuning, LoRA, and private model operations

## Current state

This scaffold provides:

- a FastAPI app
- image and video generation job endpoints
- in-memory job and generation state for development
- development placeholder artifact generation for image and video
- a private image worker service contract, ready to swap from placeholder to `diffusers`
- a clean place to add queues, storage, billing, and GPU workers next

It still does **not** perform real AI generation yet. In local development it now creates real placeholder files so the end-to-end product flow can be tested honestly.

## Suggested architecture

- `api`: public HTTP layer, auth, limits, orchestration
- `postgres`: persistent metadata for users, jobs, generations, billing state
- `redis`: queue, rate limits, ephemeral job state, pub/sub
- `worker-image`: GPU worker for image generation
- `worker-video`: GPU worker for video generation
- `storage`: S3-compatible storage for outputs and references

## Recommended first production path

1. make image generation real first
2. keep video as a second worker
3. keep the public API and the GPU workers separated
4. expose only the API publicly
5. keep workers on private networking only

## Local run

```bash
cd backend
uvicorn app.main:app --app-dir . --reload --host 127.0.0.1 --port 8010
```

If you do not have dependencies installed yet:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --app-dir . --reload --host 127.0.0.1 --port 8010
```

## Studio integration

The frontend studio is now prepared to call this API directly.

- local static studio pages default to `http://127.0.0.1:8010`
- deployed pages expect a future reverse proxy path such as `/api`
- jobs are created through the API and then polled until completion
- image jobs are now delegated to a private image worker when `ALCHEMIES_IMAGE_WORKER_URL` is configured
- image worker and API share `backend/runtime/artifacts/` for development artifact delivery
- video jobs produce a placeholder GIF in `backend/runtime/artifacts/`

## Local worker run

First export the private worker URL so the public API knows where to dispatch image jobs:

```bash
cd backend
export ALCHEMIES_IMAGE_WORKER_URL=http://127.0.0.1:8011
```

Then run the public API:

```bash
cd backend
./run_local.sh
```

In another terminal, run the private image worker:

```bash
cd backend
./run_image_worker.sh
```

## Next implementation steps

1. add PostgreSQL models
2. add Redis-backed queueing
3. add object storage integration
4. add auth tokens
5. add authenticated uploads for reference assets
6. replace mock completion with real GPU workers
