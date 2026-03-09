# Quiz 3 Practice

This repository contains a Django backend and a React frontend for the Quiz 3 Practice project.

## Structure
- `backend/` — Django project (with `base` app)
- `frontend/` — React app

## Prerequisites
- Python 3.10+ (tested on 3.13)
- Node.js + npm
- Git

## Backend setup
1. Create and activate a virtual environment (Windows example):

```powershell
cd backend
python -m venv myenv
myenv\Scripts\activate
```

2. Install Python dependencies:

```powershell
pip install -r ..\requirements.txt
```

3. Run migrations and start server:

```powershell
python manage.py migrate
python manage.py runserver
```

4. API endpoints (examples):
- `GET /api/products/`
- `POST /api/users/login/` — returns JWT `refresh` and `access` tokens plus user fields

## Frontend setup

```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000 to view the React app.

## Environment variables
Create a `.env` file (not committed) or set environment variables for:
- `SECRET_KEY`
- `DEBUG` (True/False)
- `DATABASE_URL` (optional if using a different DB)

## Git
Add and commit changes:

```bash
git init
git add .
git commit -m "Initial commit"
# add remote and push
# git remote add origin <url>
# git push -u origin main
```

## Notes
- `requirements.txt` pins core backend packages. You may want to run `pip freeze > requirements.txt` in your activated venv to produce an exact list before sharing.
- The project uses `djangorestframework-simplejwt` for JWT authentication and `django-cors-headers` to allow the frontend to connect.
