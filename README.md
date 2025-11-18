# FastAPI + React Starter Kit

Kick-start fullstack projects with a FastAPI backend, room for a React frontend (drop code into `frontend/`), PostgreSQL via Docker Compose, opinionated tooling, and ready-to-run developer workflows.

- Docker-first workflow: `docker compose` spins up the API, Postgres, and leaves room for a React frontend container.
- Database layer: PostgreSQL plus Alembic migrations (see `backend/alembic`) and async SQLAlchemy sessions out of the box.
- Quality gates: pytest suite (selective pre-commit hook) and formatting via Black/isort/Ruff to keep diffs tidy.

## Setup

### Create & activate virtual environment
```powershell
cd PythonProject\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### Run Docker services
If you start for the first time:
```powershell
docker compose up -d --build
```
Else:
```powershell
docker compose up -d
```

### Apply database migrations (inside backend container)
```powershell
cd PythonProject
docker compose exec backend /bin/bash
alembic revision --autogenerate -m "init schema"
alembic upgrade head
exit
```

### Run the app locally (optional)
```powershell
cd PythonProject\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/api/v1/health/` to verify the service is responding.

### Environment configuration
Copy `backend/.env.example` to `backend/.env` (and adjust secrets), then ensure Docker uses it by keeping the file in place. For container-specific overrides, duplicate it as `.env.docker` and update `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/backend_db`.

### Run tests (inside backend container)
```powershell
cd PythonProject
docker compose exec backend /bin/bash
pytest
exit
```

### Run tests (local virtual environment)
```powershell
cd PythonProject\backend
.\.venv\Scripts\Activate.ps1
pytest
```

### Git hooks: format + lint + tests
The repo ships with a `.pre-commit-config.yaml` that runs formatting (Black/isort/Ruff) on every commit and executes `pytest backend/tests` before a push.

```powershell
pre-commit install
pre-commit run --all-files  # optional warm-up
```
Pre-commit executes a custom helper (`scripts/run_changed_pytest.py`) so only touched test modules run under pytest alongside the formatting hooks.


## Environments & Docker targets
Set `APP_ENV` to `development`, `staging`, or `production` to pick the matching Docker multi-stage target and application mode. The value is also loaded from `backend/.env` inside containers.

```powershell
# development (default)
docker compose up -d

# staging build/run
docker compose up -d --build --pull always

# production build/run
docker compose up -d --build --pull always
```

## API quick reference
- `GET /api/v1/health/` – service heartbeat (returns status/timestamp)
- `POST /api/v1/users/` – create user (requires JSON payload matching `UserCreate`)
- `GET /api/v1/users/` – list users
- `POST /api/v1/auth/register` – register user & receive JWT
- `POST /api/v1/auth/token` – obtain JWT via credentials form
