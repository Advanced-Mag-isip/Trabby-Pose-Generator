# Docker Setup and Deployment Guide

## Tech Stack and Architecture
- Frontend: Astro JS (Port 8312)
- Backend: Django / REST Framework (Port 8313)
- Database: PostgreSQL (Internal Port 5432, Host Port 5434)

### 1. Tools and Prerequisites

Before starting, ensure you have the following tools installed:
- SSH/File Client: **PuTTY** (or native terminal SSH) https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html, **WinSCP** (for easy file transfers) https://winscp.net/eng/download.php#google_vignette
- Runtimes: **Python** 3.10+ https://www.python.org/downloads/, **Git** https://git-scm.com/downloads
- Container Engine: **Docker** & Docker Compose https://www.docker.com/

### 2. Environment Configuration

**A. Root Configuration** (TrabbyPose/.env)

generate secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

```env
SECRET_KEY=yoursecretkey
DEBUG=False
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,sandbox1.advancedthinkers.app,backend,api-san>
CORS_ORIGIN_SANDBOX=https://sandbox1.advancedthinkers.app:8312
CORS_ORIGIN_IP=http://165.22.107.245
PUBLIC_API_URL=https://api-sandbox1.advancedthinkers.app
INTERNAL_API_URL=http://backend:8313
```

**B. Backend Configuration** (TrabbyPose/backend/.env)

```env
SECRET_KEY=yoursecretkey
DEBUG=False
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,sandbox1.advancedthinkers.app,165.22.107.245:>
CORS_ORIGIN_LOCAL=http://localhost:8312
CORS_ORIGIN_SANDBOX=http://sandbox1.advancedthinkers.app:8312
```

**Frontend Configuration**

```env
PUBLIC_API_URL=http//:api-sandbox1.advancedthinkers.app:8313
INTERNAL_API_URL=http://backend:8313
```


### 3. Remote Sandbox Server Deployment Workflow

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

**Step 4: Database Engine Container**

```bash
docker compose up -d db
```

**Initialize Database Schema (Migrations)**

```bash
docker compose run --rm backend python manage.py migrate
```

**Step 6: Seed Data**

```bash
docker compose run --rm backend python manage.py seed_assets
docker compose run --rm backend python manage.py seed
```

**Step 7: Launch Containers**

```bash
docker compose up -d backend frontend
```

**Step 8: Verify Operations & Logs**

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