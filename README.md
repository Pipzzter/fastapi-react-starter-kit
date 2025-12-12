# FastAPI + Vue Starter Kit

Kick-start fullstack projects with a FastAPI backend, Vue 3 frontend, PostgreSQL via Docker Compose, opinionated tooling, and ready-to-run developer workflows.

- Docker-first workflow: `docker compose` spins up the API, Vue frontend, and Postgres.
- Frontend: Vue 3 + TypeScript + Vite + Pinia + Vue Router with hot module replacement.
- Database layer: PostgreSQL plus Alembic migrations (see `backend/alembic`) and async SQLAlchemy sessions out of the box.
- Quality gates: pytest suite (selective pre-commit hook) and formatting via Black/isort/Ruff to keep diffs tidy.

## Project Structure

```
├── backend/          # FastAPI application
├── frontend/         # Vue 3 + Vite application
├── docker/           # Docker configuration
│   ├── backend/
│   │   └── Dockerfile
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── docker-compose.yml
│   └── .dockerignore
└── scripts/          # Utility scripts
```

## Setup

### Create & activate virtual environment (backend)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### Install frontend dependencies
```powershell
cd frontend
npm install
```

### Run Docker services
If you start for the first time:
```powershell
docker compose -f docker/docker-compose.yml up -d --build
```
Else:
```powershell
docker compose -f docker/docker-compose.yml up -d
```

### Apply database migrations (inside backend container)
```powershell
cd docker
docker compose exec backend /bin/bash
alembic revision --autogenerate -m "init schema"
alembic upgrade head
exit
```

### Run the app locally (optional)
```powershell
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/api/v1/health/` to verify the service is responding.

### Environment configuration
Copy `backend/.env.example` to `backend/.env` (and adjust secrets), then ensure Docker uses it by keeping the file in place. For container-specific overrides, duplicate it as `.env.docker` and update `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/backend_db`.

## Run tests

### Run tests (inside backend container)
- Run only a single test file:
```powershell
pytest
```



- Run only a single test file:
```powershell
pytest tests/services
```


## Git hooks: format + lint + tests
The repository ships a `.pre-commit-config.yaml` that runs formatting (Black/isort/Ruff) on every commit and executes a selective pytest check for changed tests.

- Pre-commit local hook: the project uses a local hook entry that runs `python scripts/run_changed_pytest.py` with `pass_filenames: true`.
- Behavior: pre-commit passes only the changed/staged file paths to the helper; the helper filters to test files (paths containing `tests` and ending in `.py`), prepends the `backend` directory to `PYTHONPATH`, and invokes `pytest` from the repository root. This means only touched test modules are executed automatically during commits, keeping commits fast while still exercising modified tests.

To install and run hooks locally:
```powershell
# install the pre-commit hooks into .git/hooks
pre-commit install
# optionally run all configured hooks against the whole repo (warm-up)
pre-commit run --all-files
```

If you want the pre-commit hook to run the full pytest suite instead of only changed files, update `.pre-commit-config.yaml` (remove `pass_filenames: true` or configure the hook to always run) or run `pytest` directly as shown above.

## Environments & Docker targets
Set `APP_ENV` to `development`, `staging`, or `production` to pick the matching Docker multi-stage target and application mode. The value is also loaded from `backend/.env` inside containers.

```powershell
# development (default)
docker compose -f docker/docker-compose.yml up -d

# staging build/run
APP_ENV=staging docker compose -f docker/docker-compose.yml up -d --build

# production build/run
APP_ENV=production docker compose -f docker/docker-compose.yml up -d --build
```

## Access the application
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Health: `http://localhost:8000/api/v1/health/`

## API quick reference
- `GET /api/v1/health/` – service heartbeat (returns status/timestamp)
- `POST /api/v1/user/` – create user (requires JSON payload matching `UserCreate`)
- `GET /api/v1/user/` – list users
- `POST /api/v1/auth/register` – register user & receive JWT
- `POST /api/v1/auth/token` – obtain JWT via credentials form
