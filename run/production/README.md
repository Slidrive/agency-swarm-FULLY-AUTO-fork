# Production Agency Stack (Default)

This folder contains a production-oriented agency scaffold (no demos). It wires a CEO entry point, specialist agents,
and a task router that caps each agent at three active tasks with overflow queueing.

## Components
- In-memory task router (`TaskRouter`) with claim/complete/stats tools
- Default roster: CEO, Product, TechLead, Builder-1, QA, Ops
- Directional communication flows from CEO to specialists and back (minimal cross-talk)

## Configure
Set environment variables (or `.env`) using the `AGENCY_` prefix:
- `AGENCY_MODEL` (default `gpt-5`)
- `AGENCY_MAX_ACTIVE_TASKS_PER_AGENT` (default `3`)
- `AGENCY_AGENCY_NAME` (display name)
- Optional: `AGENCY_GENESIS_API_BASE`, `AGENCY_GENESIS_API_KEY`, `AGENCY_VOICE_API_BASE`, `AGENCY_VOICE_API_KEY` (placeholders only)

## Run
```bash
uv run python -c "from run.production.agency import build_agency; agency = build_agency(); print('Agency ready:', agency.name)"
```

## Next steps (recommended for public launch)
- Persist threads/tasks: implement `load_threads_callback`/`save_threads_callback` with Postgres.
- Externalize the task router to Redis for multi-worker safety.
- Add FastAPI ingress (API key/JWT) and expose CEO as the only public entry point.
- Wrap Genesis Swarm / Agency Voice as typed tools once endpoints/keys are provided.
- Containerize and deploy behind HTTPS (ALB/ACM on AWS EKS), wire Prometheus/OTel for metrics/tracing.
