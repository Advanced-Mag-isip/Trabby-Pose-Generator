# Sandbox Deployment Guide

This guide shows how to deploy the project on the sandbox server using Docker Compose.

## What You Should Change

Before deploying, make sure these files are correct for the sandbox server:

- [TrabbyPose/docker-compose.yml](TrabbyPose/docker-compose.yml)
- [TrabbyPose/.env](TrabbyPose/.env)
- [TrabbyPose/backend/.env](TrabbyPose/backend/.env)
- [TrabbyPose/frontend/.env](TrabbyPose/frontend/.env)
- [TrabbyPose/backend/project/settings.py](TrabbyPose/backend/project/settings.py)
- [TrabbyPose/frontend/astro.config.mjs](TrabbyPose/frontend/astro.config.mjs)
- [TrabbyPose/frontend/src/lib/api.ts](TrabbyPose/frontend/src/lib/api.ts)

## Recommended Values

### Root `.env`

Use this for Docker Compose variable substitution in [TrabbyPose/.env](TrabbyPose/.env):

```env
SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=trabbydb
DB_USER=trabbypose_user
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=sandbox1.advancedthinkers.app,127.0.0.1,localhost
```

### Backend `.env`

Use this for Django runtime config in [TrabbyPose/backend/.env](TrabbyPose/backend/.env):

```env
SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=trabbydb
DB_USER=trabbypose_user
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,sandbox1.advancedthinkers.app,backend
CORS_ORIGIN_LOCAL=http://localhost:8312
CORS_ORIGIN_SANDBOX=http://sandbox1.advancedthinkers.app:8312
```

### Frontend `.env`

Use this in [TrabbyPose/frontend/.env](TrabbyPose/frontend/.env):

```env
PUBLIC_API_URL=http://backend:8313
```

## Step-By-Step Deployment

### 1. Log in to the sandbox server

Connect with SSH or PuTTY.

### 2. Install Docker if needed

Make sure Docker and Docker Compose are available on the server.

### 3. Clone or update the repository

```bash
cd ~/htdocs/sandbox.xxxxxxxxxxxx/
git clone https://your-github-repo-link .
# or, if the repo already exists:
# git pull origin main
```

### 4. Create or update the env files

Make sure the three env files above exist and contain the correct sandbox values.

### 5. Start the database container

```bash
docker compose up -d db
```

### 6. Run migrations

```bash
docker compose run --rm backend python manage.py migrate
```

If this is the first time the database is being created, this applies the committed migration files to the new database.

### 7. Seed the data

Run the seed commands if you want the sandbox to include sample records:

```bash
docker compose run --rm backend python manage.py seed_assets
docker compose run --rm backend python manage.py seed
```

### 8. Start the app containers

```bash
docker compose up -d backend frontend
```

### 9. Check the running containers

```bash
docker compose ps
```

### 10. Check the logs

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

## If You Change Code Later

After you push new code to GitHub and pull it on the server:

1. Pull the latest changes.
2. Run `docker compose run --rm backend python manage.py migrate` again if there are new migrations.
3. Restart the services:

```bash
docker compose restart backend frontend
```

If you changed model fields, commit the migration files from [TrabbyPose/backend/api/migrations/](TrabbyPose/backend/api/migrations/) before deploying.

## Common Files To Update

These are the files you usually need to touch for sandbox Docker deployment:

- [TrabbyPose/docker-compose.yml](TrabbyPose/docker-compose.yml) if you need different ports or env wiring
- [TrabbyPose/.env](TrabbyPose/.env) for Compose-level variables
- [TrabbyPose/backend/.env](TrabbyPose/backend/.env) for Django settings and CORS values
- [TrabbyPose/frontend/.env](TrabbyPose/frontend/.env) for the backend URL
- [TrabbyPose/backend/project/settings.py](TrabbyPose/backend/project/settings.py) for host and CORS behavior
- [TrabbyPose/frontend/astro.config.mjs](TrabbyPose/frontend/astro.config.mjs) if the host allowlist changes
- [TrabbyPose/frontend/src/lib/api.ts](TrabbyPose/frontend/src/lib/api.ts) if it still has a hardcoded fallback URL
- [TrabbyPose/backend/api/migrations/](TrabbyPose/backend/api/migrations/) when the models change

## Notes

- Keep `DEBUG=False` on the sandbox server.
- `PUBLIC_API_URL=http://backend:8313` works inside Docker Compose because the frontend container can reach the backend by service name.
- If you get `DisallowedHost`, fix `ALLOWED_HOSTS` first.
- If the frontend cannot reach the API, check `PUBLIC_API_URL` and the Astro allowlist.
- If the database is empty, rerun the seed commands after migrations.
