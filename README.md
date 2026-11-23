# Feedback Management System

FastAPI + SQLite backend (port **8001**), React frontend, Docker, GitHub Actions CI/CD, AWS EC2.

**Live API (EC2):** http://13.203.76.211:8001/docs

## Team 15 · Mini Project 5

| Member | Role |
|---|---|
| Nanda Kishore | Team lead |
| Yashwanth | Developer |
| Abhishek N| Developer |

## Work distribution

| Member | Backend | Frontend | DevOps |
|---|---|---|---|
| **Nanda Kishore** | Database tables (`users`, `feedback`), password hashing, JWT helpers, **A1** `/register`, **A2** `/login` | – | GitHub repo + collaborators, Dockerfile, GitHub Actions CI/CD, EC2 deployment |
| **Yashwanth** | **A3** `/refresh`, **E1** `GET /feedback` | Feedback Dashboard (auto-fetch after login, empty message, logout, refresh-token handling) | – |
| **Abhishek** | **E2** `POST /feedback`, validation rules (422 errors) | Register page, Login page (store tokens, show errors) | Bonus: submit-feedback form |

## What we built

- **Backend:** FastAPI + SQLAlchemy, one SQLite file `feedback.db` with two tables, `users` and `feedback`.
- **Security:** passwords hashed with argon2; JWT access token (30 min) and refresh token (7 days). The JWT secret key comes from the GitHub secret `JWT_SECRET_KEY`.
- **Each user sees only their own feedback.**
- **Frontend:** React (Vite) with Register, Login and Feedback Dashboard pages. Tokens are stored after login, feedback loads automatically, the access token is refreshed when it expires, and API errors are shown on the page.
- **Docker:** `backend/dockerfile` builds the API image.
- **CI/CD:** every push to `main` runs `.github/workflows/deploy.yml`: build image → push to Docker Hub → SSH to EC2 → replace the container.
- **Persistent data:** on EC2, `feedback.db` lives in `/opt/feedback/data`, mounted into the container at `/app/data`, so data stays after every redeploy.

## API: 5 endpoints

| # | What it does | Method | Path | Request | Success code |
|---|---|---|---|---|---|
| A1 | Register a new user | POST | `/register` | body `{username, email, password}` | 200 |
| A2 | Login, get access + refresh tokens | POST | `/login` | body `{email, password}` | 200 |
| A3 | New access token from refresh token | POST | `/refresh` | header `refresh-token: <refresh_token>` | 200 |
| E1 | Get my feedback | GET | `/feedback` | header `token: <access_token>` | 200 |
| E2 | Submit feedback | POST | `/feedback` | body `{subject, message, rating}` + header `token` | 201 |

## Rules

| Rule | Status |
|---|---|
| Email already registered | 409 |
| Wrong email or password | 401 |
| Invalid / expired access token, or no token | 401 |
| Invalid / expired refresh token | 401 |
| Missing or empty fields, invalid email, rating not 1–5 | 422 |

All of these were tested on the EC2 deployment.

## Project structure

```
backend/     main.py (endpoints), functions.py (database, hashing, JWT), requirements.txt, dockerfile
frontend/    React app: src/App.jsx, src/components/Register.jsx, Login.jsx, Dashboard.jsx
.github/workflows/deploy.yml   CI/CD to Docker Hub and EC2
```

## Run locally

Backend (http://127.0.0.1:8001/docs):
```
cd backend
docker build -t feedback-api -f dockerfile .
docker run -d --name feedback-local -p 8001:8001 feedback-api
```

Frontend (http://localhost:5173):
```
cd frontend
npm install
npm run dev
```

## GitHub Actions secrets

`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`, `JWT_SECRET_KEY`
