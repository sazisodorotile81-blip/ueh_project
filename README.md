# Ubuntu Enterprise Hub (UEH) Platform

A full-stack starter implementation for the PAICTA 2026 Level 5 simulation.

## Features
- Registration/login with JWT authentication and three roles: MSME Client, UEH Support Agent, UEH Admin.
- Role-aware permissions and dashboards.
- Service requests with category, description, urgency, agent assignment and status workflow.
- Opportunities for funding, tenders and training.
- Client applications and admin review.
- REST API documented with drf-spectacular (Swagger/OpenAPI).
- Relational database (SQLite for quick local setup; PostgreSQL supported).
- Security defaults, input validation, CSRF-ready Django configuration, environment-based secrets.
- React frontend with login/register, dashboards, service requests, opportunities and applications.

## Requirements
- Python 3.11+
- Node.js 20+
- Git

## 1. Backend setup
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Backend: http://127.0.0.1:8000  
Swagger API docs: http://127.0.0.1:8000/api/docs/  
Django admin: http://127.0.0.1:8000/admin/

The first registered user is not automatically an admin. Create a superuser, then use Django admin to assign the `UEH_ADMIN` role to that account. You can also create agent/admin accounts through Django admin.

## 2. Frontend setup
Open a second terminal:
```bash
cd frontend
npm install
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
npm run dev
```
Frontend: http://localhost:5173

## 3. PostgreSQL
Create a database and set these variables in `backend/.env`:
```env
DB_ENGINE=postgres
DB_NAME=ueh_db
DB_USER=ueh_user
DB_PASSWORD=change-this
DB_HOST=localhost
DB_PORT=5432
```
Install `psycopg[binary]` (already included in requirements).

## 4. API overview
| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register MSME client |
| POST | `/api/auth/token/` | Public | Obtain JWT access/refresh tokens |
| POST | `/api/auth/token/refresh/` | Public | Refresh access token |
| GET/PATCH | `/api/auth/me/` | Authenticated | Current profile |
| GET/POST | `/api/requests/` | Client/Agent/Admin | List/create requests |
| GET/PATCH | `/api/requests/{id}/` | Owner/assigned agent/Admin | View/update request |
| GET/POST | `/api/opportunities/` | Authenticated/Admin | Browse or create opportunities |
| GET | `/api/applications/` | Client/Admin | List applications |
| POST | `/api/opportunities/{id}/apply/` | Client | Apply |
| PATCH | `/api/applications/{id}/` | Admin | Review application |
| GET | `/api/dashboard/` | Authenticated | Role-specific dashboard statistics |

## 5. Security notes
- Passwords are hashed by Django's password hasher; passwords are never returned by serializers.
- JWT endpoints require valid credentials.
- Role and object-level permission checks are applied to API endpoints.
- Django ORM parameterizes database queries; do not build SQL using string concatenation.
- DRF serializers validate incoming data.
- React renders user content as text; do not use `dangerouslySetInnerHTML`.
- Django CSRF middleware remains enabled. JWT is stored in session storage in this demo; production deployments should prefer secure, HttpOnly cookies and configure CSRF accordingly.
- Set `DEBUG=False`, a strong `SECRET_KEY`, HTTPS, allowed hosts and secure cookie settings in production.
- Never commit `.env`, credentials, access tokens or production data.

## 6. Git workflow
```bash
git init
git add .
git commit -m "chore: create UEH project structure"
git checkout -b feature/authentication
# make a small change, test it, commit it
git add .
git commit -m "feat: add client registration and JWT login"
```
Each learner must make their own meaningful commits and be able to explain their work.

## 7. Evidence portfolio
Keep these up to date:
- Individual Git commit history and role log.
- Daily stand-up entries.
- Test cases/results and defect register.
- Security checklist.
- Reflection answers.
- Screenshots of running pages and API docs.

## Important
This is a complete educational baseline, not a production-certified financial/payment system. Opportunity applications are recorded in the database; no real payments are processed. Review the security checklist and run the tests before deployment.
