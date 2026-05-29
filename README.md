# Trabby-Pose-Generator

## Initial Setup Documentation

## Tech Stack

- Backend: Django
- Frontend: Astro JS
- Database: PostgreSQL

## Prerequisites

Install these on your Windows machine before starting:

- Python 3.10+
- Node.js 18+
- PostgreSQL
- Git

## Tools & installers

IThese are the tools used. Visit the link to download.

- **PuTTY (SSH client):** https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- **WinSCP:** https://winscp.net/eng/download.php#google_vignette
- **PostgreSQL:** https://www.postgresql.org/download/
- **Node.js:** https://nodejs.org/
- **Python:** https://www.python.org/downloads/
- **Git:** https://git-scm.com/downloads


## Step 1 - Create the Project Folder

```bash
mkdir TrabbyPose
cd TrabbyPose
```

## Step 2 - Set Up Django Backend

### Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate.bat
```

### Install dependencies

```bash
pip install django djangorestframework psycopg2-binary python-dotenv django-cors-headers
```

### Create the Django project and app

```bash
python -m django startproject backend
cd backend
python -m django startapp api
```
## Step 3 - Set Up Astro JS Frontend

From the `TrabbyPose` root folder, open a new terminal:

```bash
cd ..
npm create astro@latest frontend
cd frontend
```

## Notes

- This document is a first setup guide for the project structure.
- The backend and frontend are set up separately so they can be developed and deployed independently.

- pip install -r backend/requirements.txt //this installs project dependencies
- in TrabbyPose\backend and TrabbyPose\frontend create a .env file. An env.example is given.
- To generate the secret key, `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Then you paste this to backend\env
- create .gitignore under TrabbyPose and store sensitive files such as the .env

## How to run in terminal

Run the backend and frontend simultaneously in different terminals

- to run the backend:

```bash
cd backend
python manage.py runserver 127.0.0.1:8000
```

- to run the frontend:
```bash
cd frontend
npm run dev
```

- then you visit: http://localhost:8312


