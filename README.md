# Feedback Management System

FastAPI + SQLite backend (port **8001**), React frontend, Docker, GitHub Actions CI/CD, AWS EC2.

## Team 15 · Mini Project 5

| Member | Role |
|---|---|
| Nanda Kishore | Team lead |
| Yashwanth | Developer |
| Abhishek | Developer |

## Work distribution

| Member | Backend | Frontend | DevOps |
|---|---|---|---|
| **Nanda Kishore** | Database tables (`users`, `feedback`), password hashing, JWT helpers, **A1** `/register`, **A2** `/login` | – | GitHub repo + collaborators, Dockerfile, GitHub Actions CI/CD, EC2 deployment |
| **Yashwanth** | **A3** `/refresh`, **E1** `GET /feedback` | Feedback Dashboard (auto-fetch after login, empty message, logout, refresh-token handling) | – |
| **Abhishek** | **E2** `POST /feedback`, validation rules (422 errors) | Register page, Login page (store tokens, show errors) | Bonus: submit-feedback form |

## API: 5 endpoints

| # | What it does | Method | Path | Request body | Success code |
|---|---|---|---|---|---|
| A1 | Register a new user | POST | `/register` | `{username, email, password}` | 201 |
| A2 | Login, get access + refresh tokens | POST | `/login` | `{email, password}` | 200 |
| A3 | New access token from refresh token | POST | `/refresh` | `{refresh_token}` | 200 |
| E1 | Get my feedback | GET | `/feedback` | – (header `Authorization: Bearer <access_token>`) | 200 |
| E2 | Submit feedback | POST | `/feedback` | `{subject, message, rating}` + Bearer header | 201 |

## Rules

| Rule | Status |
|---|---|
| Email already registered | 409 |
| Wrong email or password | 401 |
| Invalid / expired access token, or no token | 401 |
| Invalid / expired refresh token | 401 |
| Missing or empty fields, invalid email, rating not 1–5 | 422 |
