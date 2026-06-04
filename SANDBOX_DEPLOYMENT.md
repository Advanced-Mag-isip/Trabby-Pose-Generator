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

**Step 1: Connect to the Sandbox Server via PuTTY**

- SSH: sandbox.advancedthinkers.app
- UN: advancedthinkers-sandbox1
- PW: EFGoeF1zfHgzjTqDMgDY

```bash
cd ~/htdocs/sandbox1.advancedthinkers.app/
```

**Step 2: Clone Codebase** (Only if first time deploying to server)

To check if there is an existing codebase already:

```bash
cd ~/htdocs/sandbox1.advancedthinkers.app/Trabby-Pose-Generator/TrabbyPose
```
If there is an existing folder, no need to clone the repository, if there's no existing folder, then clone the repository.

```bash
git clone https://yourgithubrepo
git pull origin main
```

**Step 3: Seed the Environment Configuration Files**

Create the setup based on what you did on the Environment COnfiguration part

```bash
nano .env
nano backend/.env
nano frontend/.env
```

**Step 4: Build Container**

```bash
docker compose up -d --build
```

**Initialize Database Schema (Migrations)**

```bash
docker compose run --rm backend python manage.py migrate
```

**Step 6: Create Superuser**

```bash
docker compose run --rm backend python manage.py createsuperuser
```

**Step 7: Create admin user**
```bash
docker compose run --rm backend python manage.py shell

from api.models import User
from django.utils import timezone
import hashlib

User.objects.create(
    user_name='your username',
    password=hashlib.sha256('yourpassword'.encode()).hexdigest(),
    email_address='your@example.com',
    first_name='yourfn',
    last_name='yourln',
    is_permitted=1,
    created_at=timezone.now(),
    updated_at=timezone.now()
)
exit()
```


**Step 8: Launch Containers**

```bash
docker compose up -d backend frontend
```

**Step 9: Verify Operations & Logs**

```bash
# Check orchestration status
docker compose ps

# View live application standard outputs
docker compose logs -f backend
docker compose logs -f frontend
```


### F4. Applying Ongoing Code Updates

When you want to apply changes that are committed to remote repository:

```bash
cd ~/htdocs/sandbox1.advancedthinkers.app/Trabby-Pose-Generator

# 2. Pull production-ready changes
git pull 

# 3. Apply schema updates if backend models shifted
docker compose run --rm backend python manage.py migrate

# 4. Trigger container software rebuilding and recycle execution layers
docker compose up --build -d backend frontend
```