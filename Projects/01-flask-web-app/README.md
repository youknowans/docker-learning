# 🐳 Flask + Redis Multi-Container App

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A multi-container application built as part of my DevOps bootcamp journey. This project demonstrates Docker, Docker Compose, Docker Networking and Docker Volumes working together in a real world setup.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Testing the Application](#testing-the-application)
- [Environment Variables](#environment-variables)
- [Persistent Storage](#persistent-storage)
- [What I Learned](#what-i-learned)

---

## Overview

This project consists of two containerised services:

- **Flask Web App** — A Python web application with two routes
- **Redis Database** — A key-value store that tracks visit counts

The two containers communicate over a custom Docker network and Redis data persists across container restarts via a Docker Volume.

---

## Architecture

```
                    Internet
                        │
                   -p 5000:5000
                        │
              ┌─────────────────────┐
              │    flask-redis      │
              │      network        │
              │                     │
              │  ┌──────────────┐   │
              │  │   web        │   │
              │  │  (Flask)     │   │
              │  │  port 5000   │   │
              │  └──────┬───────┘   │
              │         │           │
              │  ┌──────▼───────┐   │
              │  │   redis      │   │
              │  │  (Redis)     │   │
              │  │  port 6379   │   │
              │  │  no -p flag! │   │
              │  └──────────────┘   │
              └─────────────────────┘
                        │
                   r_data volume
                  (persistent data)
```

**Key design decisions:**
- Redis has no `ports:` mapping — hidden from the internet 🔒
- Both containers on the same custom network — talk by service name
- Redis data stored in a named volume — survives container restarts
- Redis connection details passed via environment variables

---

## Project Structure

```
flask-redis-app/
├── app.py                 # Flask application
├── Dockerfile             # Flask container build instructions
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Multi-container orchestration
└── README.md              # This file!
```

---

## Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Verify your installation:

```bash
docker --version
docker compose version
```

---

## Getting Started

**1. Clone the repository:**

```bash
git clone https://github.com/youknowans/flask-redis-app.git
cd flask-redis-app
```

**2. Build and start the containers:**

```bash
docker compose up -d --build
```

**3. Verify both containers are running:**

```bash
docker compose ps
```

You should see both `web` and `redis` services with status `Up`.

**4. Check the logs:**

```bash
# All services
docker compose logs

# Flask only
docker compose logs -f web

# Redis only
docker compose logs -f redis
```

**5. Stop the application:**

```bash
docker compose down
```

---

## Testing the Application

### Welcome Page
Visit the home route in your browser:

```
http://localhost:5000
```

Expected response:
```
Welcome to the Flask App!
```

### Visit Counter
Navigate to the count route:

```
http://localhost:5000/count
```

Expected response on first visit:
```
Visit count: 1
```

Refresh the page — the count increments each time:
```
Visit count: 2
Visit count: 3
...
```

---

## Environment Variables

Redis connection details are passed via environment variables — never hardcoded!

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `redis` | Redis service hostname |
| `REDIS_PORT` | `6379` | Redis service port |

These are set in `docker-compose.yml`:

```yaml
environment:
  - REDIS_HOST=redis
  - REDIS_PORT=6379
```

And read in `app.py`:

```python
r = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=0
)
```

---

## Persistent Storage

Redis data is stored in a named Docker Volume called `r_data`. This means your visit count **persists even after containers are stopped and restarted!**

**Test persistence yourself:**

```bash
# Note your current visit count at /count

# Stop and remove containers
docker compose down

# Start again
docker compose up -d

# Visit /count — count continues from where it left off! 🎉
```

To completely reset the data:

```bash
# WARNING — this deletes all Redis data!
docker compose down -v
```

---

## Useful Commands

```bash
# Start everything
docker compose up -d --build

# Stop everything (keeps volume data)
docker compose down

# Stop everything and delete data
docker compose down -v

# See running services
docker compose ps

# Follow Flask logs
docker compose logs -f web

# Get inside Flask container
docker compose exec web bash

# Get inside Redis container
docker compose exec redis redis-cli

# Check visit count directly in Redis
docker compose exec redis redis-cli get counter
```

---

## What I Learned

Building this project taught me how all the Docker concepts fit together in a real application:

| Concept | How it's used in this project |
|---------|------------------------------|
| **Dockerfile** | Builds the Flask image with layer caching and cleanup |
| **Docker Compose** | Orchestrates Flask and Redis together |
| **Docker Networking** | Custom `flask-redis` network — containers find each other by name |
| **Docker Volumes** | `r_data` volume persists Redis data across restarts |
| **Security** | Redis has no port mapping — hidden from internet |
| **Environment Variables** | Redis connection details passed at runtime — not hardcoded |
| **Layer Caching** | `requirements.txt` copied before code for faster builds |

---

## Part of My DevOps Learning Journey 🚀

This project is part of my DevOps bootcamp. Check out my other notes and projects:

- 📝 [Docker Core Concepts](./notes/01-core-concepts.md)
- 📝 [Docker Commands](./notes/02-basic-commands.md)
- 📝 [Docker Networking](./notes/03-docker-networking.md)
- 📝 [Docker Compose](./notes/04-docker-compose.md)
- 📝 [Docker Volumes](./notes/05-docker-volumes.md)
- 📝 [Dockerfile Anatomy](./notes/06-docker-file.md)

---

*Built with 💪 and a lot of debugging!*