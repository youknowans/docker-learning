# 💾 05 — Docker Volumes

> My notes on Docker Volumes written in plain English as part of my DevOps bootcamp journey.

---

## 📌 Table of Contents

- [What is a Docker Volume?](#what-is-a-docker-volume)
- [The Three Ways to Mount Data](#the-three-ways-to-mount-data)
- [Volumes vs Bind Mounts](#volumes-vs-bind-mounts)
- [Volume Commands](#volume-commands)
- [Using Volumes with docker run](#using-volumes-with-docker-run)
- [Using Volumes in Docker Compose](#using-volumes-in-docker-compose)
- [Bind Mounts for Development](#bind-mounts-for-development)
- [Development vs Production Setup](#development-vs-production-setup)
- [docker compose down vs down -v](#docker-compose-down-vs-down--v)
- [Common Mistakes](#common-mistakes)
- [Quick Summary](#quick-summary)

---

## What is a Docker Volume?

Containers are **ephemeral** — when a container is deleted everything inside it is gone. But some data needs to survive:

- 🗄️ Database records
- 📁 Uploaded files
- 📝 Log files
- ⚙️ Config files

**Docker Volumes** solve this by storing data OUTSIDE the container!

> 🏨 **Analogy:** Think of a container like a **hotel room** — when you check out the room is wiped clean for the next guest. A volume is like a **storage locker in the hotel lobby** — you can check out of any room but your stuff stays safely in the locker!

---

## The Three Ways to Mount Data

### 1. Volumes (Managed by Docker) ✅
Docker manages everything — storage lives in Docker's own area on your machine:

```bash
# Create a volume
docker volume create my-data

# Use it when running a container
docker run -d \
  --name my-db \
  -v my-data:/var/lib/mysql \
  mysql:5.7
```

### 2. Bind Mounts (You manage the path)
You specify an exact folder on your machine to mount into the container:

```bash
docker run -d \
  -v /home/user/mydata:/var/lib/mysql \
  mysql:5.7
```

> 📁 Like plugging a specific folder on your laptop directly into the container!

### 3. tmpfs Mounts (In memory only)
Stored in memory — not on disk at all. Gone when container stops:

```bash
docker run -d \
  --tmpfs /app/temp \
  my-app
```

> 🧠 Used for sensitive temporary data you don't want written to disk!

---

## Volumes vs Bind Mounts

| | Volumes | Bind Mounts |
|--|---------|------------|
| **Managed by** | Docker | You |
| **Location** | Docker's storage area | Anywhere on your machine |
| **Portability** | ✅ Works anywhere | ❌ Path must exist on host |
| **Best for** | Databases, persistent data | Development — live code editing |
| **Performance** | ✅ Optimised | Good |
| **Recommended** | ✅ Production | Development |

**Easy way to tell them apart in a command:**
```bash
-v my-data:/var/lib/mysql          # left = name → Docker Volume ✅
-v /home/ansaff/mydata:/var/lib/mysql  # left = path starting with / → Bind Mount ✅
```

> 🧠 Starts with `/` → bind mount. Just a name → Docker volume!

---

## Volume Commands

```bash
# Create a volume
docker volume create my-data

# List all volumes
docker volume ls

# Inspect a volume — see where Docker stores the data
docker volume inspect my-data

# Remove a volume
docker volume rm my-data

# Remove ALL unused volumes
docker volume prune
```

> ⚠️ Volumes don't appear in your normal laptop folders — Docker stores them in its own area. Use `docker volume inspect` to find the `Mountpoint` if you need to see where!

---

## Using Volumes with docker run

The `-v` flag maps a volume to a path inside the container:

```bash
docker run -d \
  --name my-db \
  -v my-data:/var/lib/mysql \
  mysql:5.7
```

| Part | Meaning |
|------|---------|
| `my-data` | Volume name — Docker manages this |
| `/var/lib/mysql` | Path inside the container where MySQL stores data |

> ⚠️ The right side path must match where the app actually stores its data inside the container!

---

## Using Volumes in Docker Compose

Two parts are required — both must be present for volumes to work:

```yaml
version: '3'

services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    volumes:
      - db-data:/var/lib/mysql    # PART 1 — mount into the service

volumes:
  db-data:                        # PART 2 — define the volume here!
```

> ⚠️ A very common mistake is defining the volume in the service but forgetting to declare it at the bottom — always need BOTH parts!

---

## Bind Mounts for Development

Bind mounts let you edit code on your laptop and see changes instantly without rebuilding the image:

```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5002:5002"
    volumes:
      - .:/app    # mount current folder into /app in container
```

Now when you edit `app.py` on your laptop the container sees the changes immediately — no `docker compose up -d --build` needed! ✅

> 🔥 This is how most developers work locally — bind mount the code in, use volumes for the database!

---

## Development vs Production Setup

A complete development setup combining everything:

```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5002:5002"
    volumes:
      - .:/app                    # 🔥 bind mount — live code editing (dev only!)
    depends_on:
      - db

  db:
    image: mysql:5.7
    env_file:
      - .env                      # 🔒 secure password storage
    volumes:
      - db-data:/var/lib/mysql    # 💾 persistent database data

volumes:
  db-data:
```

Your `.env` file (never commit to GitHub!):
```bash
MYSQL_ROOT_PASSWORD=Str0ng$ecureP@ssword123!
```

**Changes needed before going to production:**

| Change | Why |
|--------|-----|
| Remove `- .:/app` bind mount | Don't want live code editing in production — bake code into image! |
| Use `env_file` not hardcoded password | Never expose secrets in your compose file |
| Never add `ports:` to db | Database must always be hidden from internet |

---

## docker compose down vs down -v

This is critical to understand:

```bash
# Stops and removes containers — volumes SAFE ✅
docker compose down

# Stops, removes containers AND deletes volumes ❌
docker compose down -v
```

```
docker compose down      → containers gone, data SAFE ✅
docker compose down -v   → containers gone, data GONE ❌
```

> ⚠️ **Never run `docker compose down -v` in production** unless you absolutely want to wipe all data — it's the nuclear option!

---

## What You Proved Hands On 🛠️

### Mission 2 — Named volumes survive container deletion
```bash
# Write data into volume
docker run --rm -v my-test-data:/data ubuntu \
  bash -c "echo 'Hello!' > /data/test.txt"

# Delete container (--rm auto-deletes it)
# Volume still exists!

# Read data from fresh container
docker run --rm -v my-test-data:/data ubuntu cat /data/test.txt
# Output: Hello! ✅
```

### Mission 3 — Database data survives container deletion
```bash
# Start MySQL with volume
docker run -d --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -v mysql-data:/var/lib/mysql \
  mysql:5.7

# Add data, then delete container
docker rm -f my-mysql

# Start brand new container with SAME volume
docker run -d --name my-mysql-new \
  -e MYSQL_ROOT_PASSWORD=password \
  -v mysql-data:/var/lib/mysql \
  mysql:5.7

# Data still there! ✅
```

### Mission 4 — Bind mount for live development
```yaml
# In docker-compose.yml
volumes:
  - .:/app    # edit on laptop → instant changes in container!
```

---

## Common Mistakes ⚠️

- ❌ No volume on database container — all data lost on container deletion!
- ❌ Defining volume in service but forgetting to declare it under `volumes:` at the bottom
- ❌ Using bind mounts in production — code should be baked into the image
- ❌ Hardcoding passwords — always use `env_file` and `.env` files
- ❌ Running `docker compose down -v` accidentally — deletes all volume data!
- ❌ Expecting volumes to appear in your normal laptop folders — Docker manages its own storage area

---

## Quick Summary 📋

| Concept | Key Point |
|---------|-----------|
| Volume | Docker managed — data lives outside container — survives deletion |
| Bind Mount | Your folder mounted into container — great for live dev |
| tmpfs | Memory only — gone when container stops |
| `-v name:/path` | Docker volume |
| `-v /path:/path` | Bind mount |
| `docker compose down` | Volumes safe ✅ |
| `docker compose down -v` | Volumes deleted ❌ |
| Two parts needed | Mount in service AND define under `volumes:` |
| Production rule | Use volumes for db, no bind mounts, secrets in `.env` |

---

*Next up → [06 - CI/CD Pipelines](./06-docker-file.md)* 🚀
