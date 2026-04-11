# Own API Architecture for Alchemies.PRO

This document defines the direction for Alchemies.PRO to become its own generation platform and eventually offer the service to third parties.

## Product rule

The public product should talk to **our API**, not directly to model runtimes.

That API becomes the stable contract for:

- web app
- future desktop clients
- partner integrations
- billing and subscriptions
- rate limiting
- model routing
- queue management
- observability

## Why this matters

Even if the underlying models are open or self-hosted, a product business needs its own API layer so it can:

- switch models without breaking clients
- keep prompts, outputs, and usage records in one system
- enforce quotas
- add private fine-tunes
- expose a future commercial platform safely

## Recommended architecture

### 1. Public API

Responsibilities:

- auth
- API keys
- tenant isolation
- request validation
- moderation and guardrails
- billing hooks
- job creation
- polling and webhooks

Suggested stack:

- FastAPI
- PostgreSQL
- Redis

### 2. Orchestration

Responsibilities:

- route image jobs to image workers
- route video jobs to video workers
- pick model family and preset
- retry failed jobs
- track cost and latency

### 3. GPU workers

Responsibilities:

- download models
- run inference
- upload results
- report progress

Important:

- workers should remain private
- do not expose worker ports publicly
- run them on dedicated GPU machines, not on the current shared VPS

### 4. Storage

Responsibilities:

- store reference uploads
- store generated images and videos
- produce signed URLs
- preserve metadata for audits and billing

Suggested options:

- S3-compatible object storage
- Cloudflare R2
- MinIO for self-managed environments

## Rollout plan

### Phase 1

- image generation only
- internal API
- one GPU worker
- manual admin usage

### Phase 2

- user accounts
- API keys
- quotas
- generation history
- object storage

### Phase 3

- video generation worker
- webhook callbacks
- usage metering
- service plans

### Phase 4

- custom LoRAs
- customer workspaces
- fine-tuned styles
- commercial API offering

## Model direction

For a future commercial service, do not assume every open model is allowed for commercial API resale.

The API should be designed so models can be swapped per license and per workload.

## Current code status

The repository now includes:

- `backend/` for the public API foundation
- generation endpoints for image and video jobs
- a private image worker scaffold with an internal HTTP contract
- development placeholder artifact flow for both image and video

The next step is to replace the placeholder image backend inside the private worker with a real `diffusers` runtime on a dedicated GPU machine.
