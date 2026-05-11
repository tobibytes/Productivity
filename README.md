# Productivity

A microservice-based student-productivity platform. Connect your Canvas LMS, pull your courses and announcements, and get AI-generated study aids (notes, flashcards, embeddings for search) — all behind a Next.js front-end.

## Services

| Service | Language | Role |
| --- | --- | --- |
| [`canvas/`](./canvas) | Python (FastAPI) | Canvas LMS integration: courses, modules, assignments, submissions. Stores user Canvas API tokens encrypted at rest. |
| [`controller/`](./controller) | Python (FastAPI) | Front-door API that fans out to the other services. |
| [`ai/`](./ai) | Python | AI study-aid generators — `embeddings/`, `flashcards/`, `notes/`. |
| [`payment/`](./payment) | Python (FastAPI) | Subscription & pricing. |
| [`shared/`](./shared) | Python | Shared DB client. |
| [`canvasfrontend/`](./canvasfrontend) | Next.js | User-facing UI. |

Each service has its own `Dockerfile` and is meant to run behind the controller; see `controller/` for the routing surface.

## Configuration

The Canvas service encrypts user API tokens with AES-256-GCM. **Set the key via env, never via a committed file:**

```sh
# Generate a fresh 32-byte key, base64 encoded
python -c "import base64, os; print(base64.b64encode(os.urandom(32)).decode())"

# Then for every environment:
export CANVAS_ENCRYPTION_KEY="<that-base64-string>"
```

Other env vars (per-service `.env` or Docker secrets):

- `JWT_SECRET` — used by the canvas service for session JWTs
- `FRONTEND_ORIGIN` — CORS allowlist
- `COOKIE_SECURE`, `COOKIE_SAMESITE`, `COOKIE_DOMAIN` — session cookie tuning
- Redis, Postgres connection details per `db.py` / `db_client.py`

## Run it

Each service is independently runnable:

```sh
# Canvas service (port 8000)
cd canvas
pip install -r requirements.txt
uvicorn main:app --reload

# Controller, payment, ai/* — same pattern with their own requirements.txt
```

A compose file isn't checked in (intentionally — see `.gitignore`).

## Stack

**Backend** — Python · FastAPI · `pydantic` · `redis` · Postgres · `cryptography` (AES-GCM) · `pyjwt` · `dotenv`

**Frontend** — Next.js · React · TypeScript

**Infra** — per-service Dockerfiles
