# 🎻 04 — Docker Compose

> My notes on Docker Compose written in plain English as part of my DevOps bootcamp journey.

---

## 📌 Table of Contents

- [What is Docker Compose?](#what-is-docker-compose)
- [The docker-compose.yml File](#the-docker-composeyml-file)
- [Line by Line Breakdown](#line-by-line-breakdown)
- [Key Commands](#key-commands)
- [docker run vs Docker Compose](#docker-run-vs-docker-compose)
- [Volumes — Persisting Data](#volumes--persisting-data)
- [depends_on and Healthchecks](#depends_on-and-healthchecks)
- [Compact vs Explicit Compose Files](#compact-vs-explicit-compose-files)
- [Common Mistakes](#common-mistakes)
- [Quick Summary](#quick-summary)

---

## What is Docker Compose?

So far every time you set up a Flask and MySQL app you had to run multiple commands:

```bash
docker network create app-network
docker run -d --name db --network app-network ...
docker run -d --name myapp --network app-network ...
```

**Docker Compose replaces ALL of that with a single file and a single command!**

> 🎻 **Analogy:** Instead of calling each musician individually and telling them when to start — Docker Compose is the **conductor** that coordinates everyone at once!

---

## The docker-compose.yml File

Everything lives in a file called `docker-compose.yml`. It describes:
- What containers to run
- What images to use
- What ports to map
- What environment variables to set
- What networks to use
- What volumes to mount

Here's a Flask + MySQL setup as a Docker Compose file:

```yaml
version: '3'

services:

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - app-network

  web:
    build: .
    ports:
      - "5002:5002"
    networks:
      - app-network
    depends_on:
      - db

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
```

---

## Line by Line Breakdown

**`version: '3'`**
> Tells Docker Compose which version of the compose format to use. Version 3 is the most common.

**`services:`**
> Where you define all your containers. Each item under services is one container.

**`db:`**
> The name of the service — used as the hostname for container to container communication!

**`image: mysql:5.7`**
> Use this pre-built image from Docker Hub — same as `docker run mysql:5.7`

**`build: .`**
> Instead of a pre-built image, build from the Dockerfile in the current folder — same as `docker build .`

**`ports:`**
> Same as `-p` in docker run. Maps laptop port to container port (LEFT:RIGHT)

**`environment:`**
> Same as `-e` in docker run. Sets environment variables inside the container.

**`networks:`**
> Which network this container joins — same as `--network` in docker run.

**`depends_on:`**
> Tells Docker Compose to start `db` BEFORE `web`. Controls startup order.

**`volumes:` (under a service)**
> Mounts a volume to persist data outside the container.

**`networks:` (at the bottom)**
> Defines the actual networks — same as `docker network create`

**`volumes:` (at the bottom)**
> Defines the actual volumes used by services.

---

## Key Commands

```bash
# Start everything in the background
docker compose up -d

# Start everything and REBUILD images (use after code changes!)
docker compose up -d --build

# Stop and remove everything
docker compose down

# Stop and remove everything including volumes
docker compose down -v

# See running services
docker compose ps

# See logs of all services
docker compose logs

# Follow logs in real time
docker compose logs -f

# See logs of a specific service only
docker compose logs -f web

# Restart a specific service
docker compose restart web

# Get inside a running service
docker compose exec web bash

# Build images without starting
docker compose build
```

> ⚠️ **Always use `--build`** when you've made code changes — `docker compose up -d` alone uses the cached image and won't pick up your changes!

---

## docker run vs Docker Compose

The same Flask + MySQL setup written both ways:

**Without Docker Compose ❌ — many commands:**
```bash
docker network create app-network

docker run -d \
  --name db \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  mysql:5.7

docker run -d \
  --name web \
  --network app-network \
  -p 5002:5002 \
  hello-flask-mysql
```

**With Docker Compose ✅ — one command:**
```bash
docker compose up -d
```

And to tear it all down:
```bash
docker compose down
```

---

## Volumes — Persisting Data

By default containers are **ephemeral** — all data is lost when a container is deleted!

```bash
docker compose down    # stops AND deletes containers
docker compose up -d   # fresh containers — all data GONE! 💥
```

The solution is **Docker Volumes** — stores data outside the container on your machine:

```yaml
services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    volumes:
      - db-data:/var/lib/mysql    # store data outside container!

volumes:
  db-data:                        # define the volume here
```

Now even after `docker compose down` and `docker compose up -d` — data is still there! ✅

> 💾 **Analogy:** Think of a volume like a **USB drive** plugged into the container — even when the container is thrown away the USB drive and all its data remains!

> ⚠️ To delete volumes too: `docker compose down -v` — use with caution!

---

## depends_on and Healthchecks

### What depends_on does

`depends_on` controls **start order** — it starts `db` before `web`:

```yaml
services:
  web:
    build: .
    depends_on:
      - db    # start db first, then web
```

### What depends_on does NOT do ⚠️

`depends_on` does NOT wait for the database to be **fully ready** — it only waits for the container to **start**. MySQL takes several seconds to fully initialise which can cause connection errors!

```
db container starts → web starts immediately →
web tries to connect → MySQL still initialising → ❌ connection error!
```

### The proper fix — Healthchecks

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy    # wait until db is healthy!

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      retries: 5
```

> 🧠 `depends_on` = *"start db first"* not *"wait until db is ready"* — a subtle but very important difference!

---

## Compact vs Explicit Compose Files

Both of these work — the compact version just relies on Docker Compose defaults:

**Compact version:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5002:5002"
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
```

**Explicit version:**
```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5002:5002"
    networks:
      - app-network
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**What Docker Compose handles automatically in the compact version:**
- Creates a default network named `foldername_default`
- Puts all services on that network automatically
- Containers still find each other by service name

> 💡 The compact version is fine for simple projects. Explicit is better for complex multi-network setups!

---

## Service Name as Hostname

In Docker Compose containers find each other using the **service name** — not the container name!

```yaml
services:
  web:    # ← web uses this to find db
    build: .
  db:     # ← this is the hostname web uses!
    image: mysql:5.7
```

```python
# In app.py — must match the service name exactly!
db = MySQLdb.connect(
    host="db",    # ✅ matches service name
    ...
)
```

> ⚠️ This is slightly different from plain `docker run` where you use `--name` as the hostname. In Docker Compose the **service name** IS the hostname!

---

## Common Mistakes ⚠️

- ❌ Using `docker compose up -d` after code changes without `--build` — changes won't be picked up!
- ❌ Exposing database ports with `ports:` — databases should never be publicly accessible
- ❌ Hostname in code not matching service name in docker-compose.yml
- ❌ Defining a volume at the bottom but forgetting to mount it in the service
- ❌ Relying on `depends_on` to wait for database readiness — use healthchecks instead!
- ❌ Running `docker compose down -v` accidentally — this deletes all volume data!

---

## Quick Summary

| Feature | What it does |
|---------|-------------|
| `docker compose up -d` | Start all services in background |
| `docker compose up -d --build` | Rebuild images then start |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Stop, remove containers AND volumes |
| `docker compose logs -f` | Follow all logs |
| `docker compose ps` | See running services |
| `docker compose exec web bash` | Get inside a service |
| `depends_on` | Controls start order only |
| `volumes` | Persists data outside containers |
| Service name | Used as hostname between containers |

---

## Why DevOps Engineers Love Docker Compose 💡

- ✅ One file describes your entire app
- ✅ One command starts everything — `docker compose up -d`
- ✅ One command stops everything — `docker compose down`
- ✅ Networks created automatically
- ✅ `depends_on` controls startup order
- ✅ Volumes persist important data
- ✅ Commit to GitHub — anyone can run your app instantly!

---

*Next up → [05 - Docker Volumes](./05-docker-volumes.md)* 🚀
