# Ajali-App
# 🚨 Ajali Reporter - Complete Flask Backend (Single Component)

Ajali Reporter is a road accident and emergency reporting platform built for Kenyan users. This is the **backend API**, built with Flask and designed to integrate with a React frontend. It handles user authentication, image-based incident reporting, and admin-ready user control.

---

## 🧰 Tech Stack

- Python + Flask
- Flask SQLAlchemy (ORM)
- Flask-JWT-Extended (JWT Auth)
- Flask-Migrate (DB migrations)
- Flask-CORS (CORS headers)
- Werkzeug (Password hashing)
- python-dotenv (Environment config)
- SQLite (Default) or PostgreSQL (optional)
- Pillow (optional image validation)

---

## 📦 Project Structure

Ajali-Backend/
├── app/
│ ├── init.py # App setup
│ ├── config.py # Environment config
│ ├── models.py # User & Incident models
│ └── routes/
│ ├── auth_routes.py # Signup/Login APIs
│ └── incident_routes.py # Incident APIs
├── uploads/ # Uploaded images
├── migrations/ # DB migrations
├── run.py # Entry point
├── requirements.txt # All dependencies
└── .env # Secrets & DB config


---

## 🔐 Authentication API

| Endpoint            | Method | Description          |
|---------------------|--------|----------------------|
| `/api/auth/signup`  | POST   | Register new user    |
| `/api/auth/login`   | POST   | Login, get JWT token |

- Stores secure password hashes
- JWT token required for protected endpoints
- Admin-ready (`is_admin` flag)

---

## 🚨 Incident Reporting API

| Endpoint               | Method | Auth? | Description                    |
|------------------------|--------|-------|--------------------------------|
| `/api/incidents/`      | POST   | ✅     | Create new incident with image |
| `/api/incidents/`      | GET    | ❌     | List all incidents             |
| `/api/incidents/:id`   | GET    | ❌     | View specific incident         |

- Accepts `multipart/form-data`
- Stores image locally in `/uploads/`
- Returns image URLs for frontend use

---

## 🧪 Database Models

### User

```python
id, username, email, password_hash, is_admin
