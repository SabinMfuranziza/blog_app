# Blog App API

A REST API built with FastAPI and PostgreSQL (Supabase).

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)
- JWT Authentication

## Setup

1. Clone the repo
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn app.main:app --reload`

## Endpoints

### Auth
- `POST /auth/register` — Register a new account
- `POST /auth/login` — Login and get JWT token

### Users
- `GET /users/me` — Get your own profile (requires auth)

### Articles
- `GET /articles` — List all published articles
- `GET /articles/{id}` — Get a single article
- `GET /articles/my_articles` — List your own articles (requires auth)
- `POST /articles` — Create an article (requires auth)
- `PATCH /articles/{id}` — Edit your article (requires auth)
- `DELETE /articles/{id}` — Delete your article (requires auth)

### Admin
- `GET /admin/users` — List all users
- `GET /admin/users/{id}` — Get a single user
- `PATCH /admin/users/{id}` — Update a user
- `DELETE /admin/users/{id}` — Delete a user
- `GET /admin/articles` — List all articles
- `PATCH /admin/articles/{id}` — Edit any article
- `DELETE /admin/articles/{id}` — Delete any article