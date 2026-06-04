# Trabby Pose Backend - Setup Guide

### Quick Start (5 minutes)

### 1. Environment Setup

Create `.env` file in `TrabbyPose/backend/`:

```bash
cd TrabbyPose/backend
cp .env.example .env  # Copy example
# Edit .env with your settings

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Database Setup

```bash
# Edit project/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Run migrations
python manage.py migrate

```

### 4. Start Development Server

```bash
python manage.py runserver

```

Visit `http://localhost:8000/api/poses/` to test!

---

## Full Setup Instructions

### Prerequisites

* **Python**: 3.11 or higher
```bash
python --version

```


* **PostgreSQL** (recommended for production):
* Download: https://www.postgresql.org/download/
* Or use: `brew install postgresql` (macOS)


* **pip** (Python package manager):
```bash
pip --version

```



### Step 1: Clone & Navigate

```bash
git clone <repository>
cd Trabby-Pose-Generator/TrabbyPose/backend

```

### Step 2: Create Virtual Environment

**macOS/Linux**:

```bash
python -m venv venv
source venv/bin/activate

```

**Windows**:

```bash
python -m venv venv
venv\Scripts\activate

```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

**Current Dependencies**:

* Django 6.0.5
* djangorestframework 3.17.1
* django-cors-headers 4.9.0
* psycopg2-binary 2.9.12 (PostgreSQL adapter)
* python-dotenv 1.2.2 (environment variables)

### Step 4: Configure Environment

Create `.env` file with:

```env
# Security
SECRET_KEY=your-django-secret-key-here

# Debug Mode (NEVER use True in production!)
DEBUG=True

# Database
DATABASE_URL=sqlite:///db.sqlite3
# OR for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/trabby_pose

# CORS (for frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:4321

```

**Generate SECRET_KEY**:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

```

### Step 5: Database Migrations

```bash
# Show pending migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

```

**Expected Output**:

```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...

```

### Step 6: Create Admin and User Accounts

**1. Create a Superuser (For Admin Access)**

```bash
python manage.py createsuperuser

```

Follow the prompts to set your admin username, email, and password. You can then visit `http://localhost:8000/admin/` to manage your data.

**2. Create a Regular User (For Login Testing)**
After creating your admin account, you can quickly create a standard user to test standard login functionality. You can do this via the Django shell:

```bash
python manage.py shell

```

Inside the shell, run the following commands (replace the credentials with your preferences):

```python
from django.contrib.auth.models import User
User.objects.create_user('testuser', 'test@example.com', 'testpassword123')
exit()

```

*(Alternatively, you can log into the Admin panel with your superuser account and add a new user manually under the "Users" section).*

### Step 7: Run Development Server

```bash
python manage.py runserver

```

**Expected Output**:

```
Watching for file changes with StatReloader
Quit the server with CONTROL-C.

Starting development server at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

```
---

## Troubleshooting

### ImportError: No module named 'rest_framework'

**Solution**: Install dependencies

```bash
pip install -r requirements.txt

```

### psycopg2 Build Error

**macOS**:

```bash
brew install libpq
pip install psycopg2-binary

```

**Ubuntu/Debian**:

```bash
sudo apt-get install libpq-dev
pip install psycopg2-binary

```

**Windows**: Use `psycopg2-binary` (pre-compiled, already in requirements.txt)

### CORS Errors in Frontend

Update `CORS_ALLOWED_ORIGINS` in `.env`:

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:4321,http://your-astro-port:port

```

### Database Already Exists

To fresh-start:

```bash
# Remove database file (SQLite)
rm db.sqlite3

# Or for PostgreSQL, drop and recreate:
dropdb trabby_pose
createdb trabby_pose

# Then re-run migrations
python manage.py migrate

```

### 404 Not Found on `/api/poses/`

**Check**: Ensure Django server is running and endpoint is correct

```bash
curl http://localhost:8000/api/poses/

```

If not found, verify:

1. URLs are correct in `api/urls.py`
2. Django is picking up the URL configuration in `project/urls.py`

---

## Development Workflow

### Making Changes

1. **Update Models**: Edit `api/models.py`
2. **Create Migration**: `python manage.py makemigrations`
3. **Apply Migration**: `python manage.py migrate`
4. **Update Serializers**: Edit `api/serializers.py` (no migration needed)
5. **Update Views**: Edit `api/views.py` (no migration needed)
6. **Test**: `curl http://localhost:8000/api/poses/`

### Running Tests

```bash
python manage.py test api

```

### Linting & Code Quality

```bash
pip install flake8 black

# Format code
black api/

# Check code style
flake8 api/

```

---

## Project Structure

```
backend/
├── manage.py                    # Django management commands
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment file
├── README.md                    # Project overview
├── API_DOCUMENTATION.md         # Full API docs
├── SETUP_GUIDE.md               # This file
├── db.sqlite3                   # Database (created after first migration)
│
├── project/                     # Django project settings
│   ├── settings.py              # Configuration
│   ├── urls.py                  # URL routing
│   ├── asgi.py                  # ASGI config
│   └── wsgi.py                  # WSGI config
│
└── api/                         # Main app
    ├── models.py                # Database models
    ├── serializers.py           # DRF serializers
    ├── views.py                 # API views & endpoints
    ├── urls.py                  # API URL routes
    ├── admin.py                 # Django admin config
    ├── tests.py                 # Unit tests
    │
    └── migrations/              # Database migrations
        └── 0001_initial.py

```

---

## Next Steps

1. ✅ **Run the backend**: `python manage.py runserver`
2. ✅ **Test endpoints**: `curl http://localhost:8000/api/poses/`
3. 🔄 **Connect frontend**: Update Astro to fetch from these APIs
4. 📖 **Read API docs**: See `API_DOCUMENTATION.md` for full endpoint specs

---

## Support

For issues:

1. Check troubleshooting section above
2. Review `API_DOCUMENTATION.md` for endpoint specs
3. Check Django logs: `tail -f logs/django.log`
4. Try Django shell for debugging: `python manage.py shell`

---

**Backend Version**: 1.0.0 (MVP)

**Created**: May 29, 2026

**Last Updated**: June 3, 2026