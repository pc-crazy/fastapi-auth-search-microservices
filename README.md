# FastAPI Microservices: Auth + Search

This project implements a containerized Python FastAPI microservices system for a scalable HR solution that supports secure and configurable employee search functionality.

---

## 🧩 Architecture

- **Auth Service**

  - Issues JWT tokens upon user login.
  - Stores and verifies users using a shared SQLite database.

- **Search Service**

  - Provides a secure, paginated `/search` API.
  - Supports dynamic column output per organization.
  - Built-in rate limiting (custom, no third-party libraries).
  - Token-based access control using the Auth service.

---

## 📁 Project Structure

```
services/
├── auth_service/
│   ├── main.py
│   ├── models.py
│   ├── db.py
│   ├── init_db.py
│   ├── ...
├── search_service/
│   ├── main.py
│   ├── models.py
│   ├── db.py
│   ├── init_db.py
│   ├── seed_faker_employees.py
│   ├── tests/
│   ├── ...
```

---

## 🧪 Setup & Run Commands

Make sure you have Python 3.11+, Docker, and Docker Compose installed.

### 🔧 Local Development

```
# Setup auth DB
python -m services.auth_service.init_db

# Setup search DB
python -m services.search_service.init_db

# Seed fake employee data (5K records)
python -m services.search_service.seed_faker_employees

# Run the search service
uvicorn services.search_service.main:app --reload --port 8000

# Run the auth service
uvicorn services.auth_service.main:app --reload --port 8001
```

---

## 🐳 Docker Setup

### 🔨 Build & Run with Docker Compose

```
docker-compose up --build
```

### 🧪 Run Tests

```
docker-compose exec search bash
pytest services/search_service/tests --cov=services/search_service --cov-report=term-missing
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here
AUTH_SERVICE_DATABASE_URL=sqlite:///./service/auth/auth.db
SEARCH_SERVICE_DATABASE_URL=sqlite:///./service/search/search.db
```

---

## ✅ Features

- JWT-based authentication
- Rate limiting using Python's standard library
- Secure and isolated access by organization
- Full-text search across multiple fields
- Pagination, filtering and dynamic column output
- 100% test coverage with `pytest`
- OpenAPI compliant documentation

---

## 🧪 Testing

```
pytest services/search_service/tests --cov=services/search_service --cov-report=term-missing
```

---
