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
ALLOWED_HOSTS=localhost,127.0.0.1,sandbox1.advancedthinkers.app,backend,api-sandbox1.advancedthinkers.app
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

**Build and start containers**
```bash
docker compose up -d --build
```

**Run migrations**
```bash
docker compose run --rm backend python manage.py migrate
```

**Create app user**
```bash
docker compose run --rm backend python manage.py shell

from api.models import User
from django.utils import timezone
import hashlib

User.objects.create(
    user_name='admin',
    password=hashlib.sha256('yourpassword'.encode()).hexdigest(),
    email_address='admin@example.com',
    first_name='Admin',
    last_name='User',
    is_permitted=1,
    created_at=timezone.now(),
    updated_at=timezone.now()
)
exit()
```

**Run localhost**