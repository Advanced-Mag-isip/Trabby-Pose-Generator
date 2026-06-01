# Docker Setup Guide

## 1. Files Involved In The Docker Setup

### Root compose file

- [TrabbyPose/docker-compose.yml](TrabbyPose/docker-compose.yml)
- Defines the `db`, `backend`, and `frontend` services.
- Controls ports, environment variables, and service names inside the Docker network.

### Backend image

- [TrabbyPose/backend/Dockerfile](TrabbyPose/backend/Dockerfile)
- Builds the Django image.
- Installs Python dependencies from `requirements.txt`.

### Frontend image

- [TrabbyPose/frontend/Dockerfile](TrabbyPose/frontend/Dockerfile)
- Builds the Astro image.
- Installs Node dependencies from `package.json`.

### Backend environment file

- [TrabbyPose/backend/.env](TrabbyPose/backend/.env)
- Stores Django runtime config, database credentials, and CORS hosts.

### Frontend environment file

- [TrabbyPose/frontend/.env](TrabbyPose/frontend/.env)
- Stores the backend base URL used by Astro SSR and the browser.

### Django settings

- [TrabbyPose/backend/project/settings.py](TrabbyPose/backend/project/settings.py)
- Reads `.env`, sets `ALLOWED_HOSTS`, CORS values, and database settings.

### Django URL routing

- [TrabbyPose/backend/project/urls.py](TrabbyPose/backend/project/urls.py)
- [TrabbyPose/backend/api/urls.py](TrabbyPose/backend/api/urls.py)
- Exposes `/api/` endpoints to the frontend.

### Frontend API helper

- [TrabbyPose/frontend/src/services/insightsAPI.js](TrabbyPose/frontend/src/services/insightsAPI.js)
- Uses `PUBLIC_API_URL` to reach the backend API.

### Astro server config

- [TrabbyPose/frontend/astro.config.mjs](TrabbyPose/frontend/astro.config.mjs)
- Controls the dev server host/port and allowed hosts.

## 2. Current Ports

### Container ports

- Postgres: `5432`
- Backend: `8313`
- Frontend: `8312`

### Host ports used in compose

- Postgres: `5434 -> 5432`
- Backend: `8313 -> 8313`
- Frontend: `8312 -> 8312`

## 3. What Must Be In `.env`

### Files You Need To Create Manually

If you are setting up the project from scratch, these are the files you should create or fill in:

- [TrabbyPose/backend/.env](TrabbyPose/backend/.env)
- [TrabbyPose/frontend/.env](TrabbyPose/frontend/.env)

If you are starting from a fresh clone, the Docker and app files already exist:

- [TrabbyPose/docker-compose.yml](TrabbyPose/docker-compose.yml)
- [TrabbyPose/backend/Dockerfile](TrabbyPose/backend/Dockerfile)
- [TrabbyPose/frontend/Dockerfile](TrabbyPose/frontend/Dockerfile)

Files that are generated later by commands:

- `backend/api/migrations/*.py` from `python manage.py makemigrations`
- database tables from `python manage.py migrate`
- seed data from `python manage.py seed`

### Backend `.env`

Required values for local Docker development:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=trabbydb
DB_USER=trabbypose_user
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ORIGIN_LOCAL=http://localhost:8312
```

Important notes:

- `ALLOWED_HOSTS` should contain hostnames or IPs only, not ports.
- `DB_HOST=db` works inside Docker Compose.

### Frontend `.env`

Required values:

```env
PUBLIC_API_URL=http://backend:8313
```

## 4. Step-By-Step Local Docker Commands

### First-time setup

1. Start the database container:

```bash
docker compose up -d db
```

2. Create migrations if your models changed:

```bash
docker compose run --rm backend python manage.py makemigrations api
```

If Django asks for a temporary default because a new non-nullable field was added, that means there is already existing data in the database.

3. Apply migrations:

```bash
docker compose run --rm backend python manage.py migrate
```

4. Seed the database:

```bash
docker compose run --rm backend python manage.py seed
```

5. Start the backend and frontend containers:

```bash
docker compose up -d backend frontend
```

### Daily start

```bash
docker compose up -d
```

### Rebuild from scratch

```bash
docker compose down -v
docker compose up --build
```

### Useful extra commands

```bash
docker compose restart backend frontend
docker compose down
docker compose logs -f backend
docker compose logs -f frontend
```

## 5. Files You Usually Need To Commit

- `backend/api/migrations/*.py` when model changes require new migrations
- `backend/project/settings.py` when host or CORS behavior changes
- `docker-compose.yml` when service names, ports, or env wiring change
- `frontend/src/services/insightsAPI.js` when API routing changes
- `frontend/astro.config.mjs` when the frontend host allowlist changes

Do not commit actual secret values from `.env` files.

## 6. Quick Checklist Before Running Locally

- Docker Desktop is running
- `db` container is up
- `backend/.env` points to `DB_HOST=db`
- `frontend/.env` points to `PUBLIC_API_URL=http://backend:8313`
- Migrations are applied
- Seed data is loaded if you want test values in Insights
- `docker compose logs -f backend` shows no `DisallowedHost` or database errors
