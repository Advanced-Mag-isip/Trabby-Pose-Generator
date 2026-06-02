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

These are the tools used. Visit the link to download.

- **PuTTY (SSH client):** https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- **WinSCP:** https://winscp.net/eng/download.php#google_vignette
- **PostgreSQL:** https://www.postgresql.org/download/
- **Docker:** https://www.docker.com/
- **Node.js:** https://nodejs.org/
- **Python:** https://www.python.org/downloads/
- **Git:** https://git-scm.com/downloads

## Local Setup

## Step 1 - Clone the repository

```bash
git clone https://github.com/Advanced-Mag-isip/Trabby-Pose-Generator.git
cd TrabbyPose
```

## Step 2 - Set Up the Backend

### Create and activate virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
```

### Install dependencies

```bash
pip install django djangorestframework psycopg2-binary python-dotenv django-cors-headers
```

Generate a secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```
Create a `.env` file:

Example contents:
```bash
SECRET_KEY=generate-a-new-key-for-server
DEBUG=False
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,sandbox.xxxxxxxxxxxx
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


## Deployment to the sandbox server

This section explains how to deploy the app to the sandbox server using PuTTY.

### 1. Connect with PuTTY

- Host Name (SSH): `sandbox.xxx.app`
- Port: `22`
- Connection type: `SSH`
- You can save your session to skip this part the next time you login
- click open
- UN:
- PW:


### 2. Clone the repository

```bash
ls //to show the all the files in the directory
cd ~/htdocs/sandbox.xxxxxxxxxxxx/
git clone https://Your github repo link .
ls
```

### 3. Set up the backend

```bash
cd ~/htdocs/sandbox.xxxxxxxxxxxx/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Generate a secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Create a `.env` file:

```bash
nano .env
```

Example contents:

```env
SECRET_KEY=generate-a-new-key-for-server
DEBUG=False
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,sandbox.xxxxxxxxxxxx
```

Run migrations:

```bash
python manage.py migrate
```

### 4. Set up the frontend

```bash
cd ~/htdocs/sandbox.xxxxxxxxxxxx/frontend
npm install
nano .env
```

Example contents:

```env
PUBLIC_API_URL=http://sandbox.xxxxxxxxxxxx:8313
```

### 5. Run Django on port 8313

```bash
screen -S django
cd ~/htdocs/sandbox.xxxxxxxxxxxx/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8313
```

Detach with `Ctrl+A` then `D`.

### 6. Run Astro on port 8312

```bash
screen -S astro
cd ~/htdocs/sandbox.xxxxxxxxxxxx/frontend
npm run dev -- --host 0.0.0.0 --port 8312
```

Detach with `Ctrl+A` then `D`.

### 7. Verify

```bash
screen -ls
```
- You can now open the URLs for your frontend or backend

- To stop the server to prevent multiple ports running simmultaneously:

```bash
screen -r django
# stop the server with Ctrl+C
```

```bash
screen -r astro
# stop the server with Ctrl+C
```

### 8. Future updates

When you push new code to GitHub, update the server with:

```bash
cd ~/htdocs/sandbox.xxxxxxxxxxxx/
git pull origin main
```

Restart Django:

```bash
screen -r django
# stop the server with Ctrl+C
python manage.py runserver 0.0.0.0:8313
# detach again with Ctrl+A then D
```

Restart Astro:

```bash
screen -r astro
# stop the server with Ctrl+C
npm run dev -- --host 0.0.0.0 --port 8312
# detach again with Ctrl+A then D
```

### Useful screen commands

| Command | What it does |
| --- | --- |
| `screen -S name` | Create a new session |
| `screen -ls` | List all sessions |
| `screen -r name` | Reattach to a session |
| `Ctrl+A` then `D` | Detach from a session |
| `Ctrl+C` | Stop the running process |
| `screen -X -S name quit` | Kill a session |

### Important notes

- Never commit `.env` files to GitHub.
- Use `screen` sessions to keep servers running after closing PuTTY.
- Always activate the virtual environment before running Django commands.
- Run `git pull` before restarting servers after pushing new code.
- Use `Ctrl+A` then `D` to detach instead of closing PuTTY inside a screen session.


