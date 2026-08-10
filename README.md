# TeamSync

A **Trello/Asana clone** built with Django REST Framework, WebSockets, and a vanilla JavaScript frontend. A production-grade team collaboration SaaS featuring real-time Kanban boards, role-based permissions, and activity tracking.

---

## 🚀 Features

- **Multi-tenant Workspaces** — Teams with role-based access (Admin, Editor, Viewer)
- **Kanban Boards** — Drag-and-drop cards across lists
- **Real-time Updates** — WebSockets sync changes across all connected clients
- **JWT Authentication** — Secure email-based login with refresh tokens
- **REST API** — Full CRUD with search, filter, pagination, and nested resources
- **Auto-generated Docs** — Swagger/OpenAPI at `/api/docs/`
- **Dockerized** — One-command setup with Docker Compose
- **CI/CD** — GitHub Actions runs tests on every push

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x + Django REST Framework |
| Real-time | Django Channels + WebSockets |
| Database | PostgreSQL |
| Cache/Queue | Redis (upcoming) |
| Frontend | Vanilla JavaScript (HTML/CSS) |
| Auth | JWT (SimpleJWT) |
| Docs | drf-spectacular (OpenAPI 3.0) |
| DevOps | Docker + Docker Compose + GitHub Actions |

---

## 📁 Project Structure

teamsync/
├── backend/
│   ├── apps/
│   │   ├── accounts/          # Custom User (email-based auth)
│   │   ├── workspaces/        # Teams, members, roles
│   │   └── boards/            # Boards, Lists, Cards, Comments
│   ├── config/                # Settings, URLs, WSGI, ASGI
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/                  # HTML/CSS/JS Kanban UI
└── .github/workflows/         # CI/CD


---

## 🛠️ Local Setup

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional)

### Without Docker
```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/teamsync.git
cd teamsync/backend

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Environment
cp .env.example .env

# 5. Database
python manage.py migrate
python manage.py createsuperuser

# 6. Run
python manage.py runserver