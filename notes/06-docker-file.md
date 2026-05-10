# 🐳 06 — Dockerfile Anatomy, Best Practices & Common Mistakes

> My notes on how to write a proper Dockerfile — instructions, best practices and common mistakes to avoid.
> Completed as part of my DevOps bootcamp journey.

---

## 📌 Table of Contents

- [What is a Dockerfile?](#what-is-a-dockerfile)
- [All Dockerfile Instructions](#all-dockerfile-instructions)
- [A Real World Dockerfile](#a-real-world-dockerfile)
- [The Three Phases of a Dockerfile](#the-three-phases-of-a-dockerfile)
- [Layer Caching — The Performance Secret](#layer-caching--the-performance-secret)
- [Multi-Stage Builds](#multi-stage-builds)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [Quick Reference Cheatsheet](#quick-reference-cheatsheet)

---

## What is a Dockerfile?

A Dockerfile is a plain text file containing step by step instructions for building a Docker image. Docker reads it top to bottom and executes each instruction in order.

```
Dockerfile  →  docker build  →  Image  →  docker run  →  Container
(Recipe)        (Cooking)       (Meal)      (Serving)     (Eating!)
```

> 📋 **Analogy:** A Dockerfile is like a **recipe card** — it tells Docker exactly how to prepare your app so it runs the same way everywhere!

---

## All Dockerfile Instructions

### FROM
**Specifies the base image to start from — always the first instruction!**

```dockerfile
FROM python:3.8-slim          # start from Python 3.8 slim image
FROM python:3.8-slim AS builder  # name this stage for multi-stage builds
FROM ubuntu:22.04             # start from Ubuntu
FROM scratch                  # empty image — start from nothing!
```

> 🏗️ Think of this as choosing what type of building to start with before you renovate it!

---

### WORKDIR
**Creates a directory and sets it as the working directory for all instructions that follow.**

```dockerfile
WORKDIR /app    # create /app folder and cd into it
```

> 🏠 Think of it as your home base — everything after happens here. It combines `mkdir` + `cd` into one instruction!

---

### COPY
**Copies files from your laptop into the image.**

```dockerfile
COPY . .                    # copy everything into WORKDIR
COPY requirements.txt .     # copy just one file
COPY ./src /app/src         # copy a folder
```

> 📦 Left = source on your laptop. Right = destination inside image.

---

### RUN
**Executes commands during image BUILD time — not when container starts!**

```dockerfile
RUN apt-get update && apt-get install -y gcc    # install system packages
RUN pip install flask                           # install Python packages
RUN mkdir /data                                 # create a directory
```

> 🔨 Used for setting things up during build — installing software, creating folders, compiling code!

---

### CMD
**Specifies the default command to run when the container STARTS.**

```dockerfile
CMD ["python", "app.py"]          # run Python app
CMD ["nginx", "-g", "daemon off;"] # run NGINX
CMD ["flask", "run"]              # run Flask
```

> 🚀 Only ONE CMD per Dockerfile — the last one wins. Can be overridden at docker run!

---

### EXPOSE
**Documents which port the container will use — it is just a label!**

```dockerfile
EXPOSE 5002    # document that the app uses port 5002
EXPOSE 80      # document that the app uses port 80
```

> ⚠️ EXPOSE does NOT actually open the port! The real port opening happens with `-p` in docker run!

---

### ENV
**Sets environment variables inside the container.**

```dockerfile
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV DB_HOST=db
```

> ⚙️ These are available to your app at runtime — like settings baked into the image!

---

### ARG
**Build time variables — only available during docker build, not at runtime!**

```dockerfile
ARG VERSION=1.0
ARG BUILD_DATE
```

> 🔑 Difference from ENV: ARG is only available during BUILD. ENV is available at RUNTIME too!

---

### LABEL
**Adds metadata/documentation to the image.**

```dockerfile
LABEL maintainer="youknowans@example.com"
LABEL version="1.0"
LABEL description="Flask MySQL App"
```

> 📝 Labels are purely informational — they don't affect how the image works!

---

### ENTRYPOINT
**Sets the main command for the container — harder to override than CMD.**

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]              # acts as default argument to ENTRYPOINT
```

> 🔒 ENTRYPOINT + CMD work together — ENTRYPOINT sets the executable, CMD provides default arguments!

---

### VOLUME
**Creates a mount point for persistent data.**

```dockerfile
VOLUME /var/lib/mysql    # mark this path as a volume mount point
```

> 💾 Tells Docker this path should be persisted outside the container!

---

### USER
**Sets which user runs subsequent instructions and the container.**

```dockerfile
RUN useradd -m appuser
USER appuser              # don't run as root!
```

> 🔒 Security best practice — never run containers as root in production!

---

## A Real World Dockerfile

Here's a complete production ready Dockerfile with everything explained:

```dockerfile
# ============================================
# STAGE 1 — BUILDER
# ============================================
FROM python:3.8-slim AS builder

# Set working directory
WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*    # clean up after install!

# Copy requirements first (layer caching!)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user -r requirements.txt

# ============================================
# STAGE 2 — FINAL PRODUCTION IMAGE
# ============================================
FROM python:3.8-slim

# Add metadata
LABEL maintainer="youknowans@example.com"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Document the port
EXPOSE 5002

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Start the app
CMD ["python", "app.py"]
```

---

## The Three Phases of a Dockerfile

Every Dockerfile follows three natural phases:

```
┌─────────────────────────────────────────────┐
│ PHASE 1 — SETUP                             │
│ FROM     — choose base image                │
│ WORKDIR  — set working directory            │
│ RUN      — install dependencies             │
├─────────────────────────────────────────────┤
│ PHASE 2 — APPLICATION                       │
│ COPY     — bring your code in               │
│ ENV      — set configuration                │
│ EXPOSE   — document ports                   │
├─────────────────────────────────────────────┤
│ PHASE 3 — STARTUP                           │
│ USER     — set who runs the app             │
│ CMD      — command to start the app         │
└─────────────────────────────────────────────┘
```

---

## Layer Caching — The Performance Secret

Every instruction in a Dockerfile creates a **layer**. Docker caches these layers and only rebuilds from the first changed layer onwards!

```dockerfile
FROM python:3.8-slim        # layer 1 — cached forever ✅
WORKDIR /app                # layer 2 — cached forever ✅
RUN apt-get install ...     # layer 3 — cached forever ✅
COPY requirements.txt .     # layer 4 — cached until requirements change ✅
RUN pip install ...         # layer 5 — cached until requirements change ✅
COPY . .                    # layer 6 — changes every code edit ❌
CMD ["python", "app.py"]    # layer 7 — cached forever ✅
```

When you change `app.py` Docker only rebuilds from layer 6 onwards!

**The Golden Rule:**
```
Things that change RARELY  →  TOP of Dockerfile
Things that change OFTEN   →  BOTTOM of Dockerfile
```

---

## Multi-Stage Builds

Multi-stage builds use multiple FROM statements to produce a smaller, cleaner final image:

```dockerfile
# Stage 1 — Build (has all the heavy tools)
FROM python:3.8 AS builder
RUN apt-get install build-essential gcc
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2 — Final (clean and lightweight!)
FROM python:3.8-slim
COPY --from=builder /root/.local /root/.local  # only copy what's needed
COPY . .
CMD ["python", "app.py"]
```

**Why this matters:**

| | Single Stage | Multi Stage |
|--|-------------|------------|
| Image size | 800MB+ | 50-100MB |
| Security | More attack surface | Less attack surface |
| Deploy speed | Slower | Much faster |
| Production ready | ❌ | ✅ |

> 🪑 **Analogy:** Like flat pack furniture — you use all the tools and packaging to build it, then throw them away. You only keep the finished furniture!

---

## Best Practices

### 1. Use specific image tags — never `latest` in production ✅
```dockerfile
# ❌ Bad — unpredictable, can break anytime
FROM python:latest

# ✅ Good — predictable and stable
FROM python:3.8-slim
```

### 2. Use slim or alpine images ✅
```dockerfile
# ❌ Bloated — 900MB+
FROM python:3.8

# ✅ Lightweight — 120MB
FROM python:3.8-slim

# ✅ Smallest — 50MB (but harder to debug)
FROM python:3.8-alpine
```

### 3. Copy requirements before code (layer caching) ✅
```dockerfile
# ❌ Bad — reinstalls packages every code change!
COPY . .
RUN pip install -r requirements.txt

# ✅ Good — packages cached until requirements change!
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 4. Chain RUN commands to reduce layers ✅
```dockerfile
# ❌ Bad — creates 3 separate layers
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y python3-dev

# ✅ Good — one layer, and cleans up after itself!
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

### 5. Clean up after apt-get installs ✅
```dockerfile
# Always add this after apt-get installs!
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*    # removes cached package lists
```

### 6. Never run as root ✅
```dockerfile
# ❌ Bad — runs as root (security risk!)
CMD ["python", "app.py"]

# ✅ Good — create and use a non-root user
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```

### 7. Use a .dockerignore file ✅
Just like `.gitignore` — tells Docker what NOT to copy into the image:

```
# .dockerignore
.git
.env
__pycache__
*.pyc
node_modules
.DS_Store
*.log
```

> 🔒 Never let `.env` files with secrets get baked into your image!

### 8. Use WORKDIR instead of RUN cd ✅
```dockerfile
# ❌ Bad
RUN mkdir /app
RUN cd /app

# ✅ Good
WORKDIR /app
```

---

## Common Mistakes

### ❌ Mistake 1 — Using latest tag
```dockerfile
FROM python:latest    # unpredictable — could break builds!
FROM python:3.8-slim  # ✅ always use specific versions
```

### ❌ Mistake 2 — Wrong COPY order (kills layer caching)
```dockerfile
# ❌ Every code change triggers full pip reinstall — slow!
COPY . .
RUN pip install -r requirements.txt

# ✅ Packages cached — only code layer rebuilds
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### ❌ Mistake 3 — Putting secrets in Dockerfile
```dockerfile
# ❌ NEVER do this — secret baked into image forever!
ENV DB_PASSWORD=mysecretpassword

# ✅ Pass secrets at runtime
docker run -e DB_PASSWORD=mysecretpassword my-app
# or use an env_file in docker-compose.yml
```

### ❌ Mistake 4 — Not cleaning up after apt-get
```dockerfile
# ❌ Leaves cached package lists — wastes space!
RUN apt-get update && apt-get install -y gcc

# ✅ Clean up after yourself!
RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*
```

### ❌ Mistake 5 — Confusing RUN and CMD
```dockerfile
# ❌ Wrong — CMD runs at build time here? No — RUN does!
CMD pip install flask      # this runs at container start — wrong!

# ✅ Correct
RUN pip install flask      # install at BUILD time
CMD ["python", "app.py"]   # start app at RUN time
```

### ❌ Mistake 6 — Copying everything including secrets
```dockerfile
# ❌ Copies .env, .git, node_modules — bad!
COPY . .

# ✅ Create a .dockerignore file first!
# Then COPY . . is safe
```

### ❌ Mistake 7 — Running as root
```dockerfile
# ❌ Runs as root — security risk in production!
CMD ["python", "app.py"]

# ✅ Create a user first
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```

---

## Quick Reference Cheatsheet

| Instruction | When it runs | What it does |
|-------------|-------------|--------------|
| `FROM` | Build | Specifies base image |
| `WORKDIR` | Build | Sets working directory |
| `COPY` | Build | Copies files from laptop into image |
| `RUN` | Build | Executes commands |
| `ENV` | Build + Runtime | Sets environment variables |
| `ARG` | Build only | Build time variables |
| `EXPOSE` | Documentation | Documents port — does NOT open it! |
| `LABEL` | Documentation | Adds metadata |
| `USER` | Build + Runtime | Sets which user runs the app |
| `VOLUME` | Runtime | Marks path for persistent storage |
| `CMD` | Runtime | Default command when container starts |
| `ENTRYPOINT` | Runtime | Main executable — harder to override |

---

## RUN vs CMD vs ENTRYPOINT

The three most confused instructions:

```dockerfile
RUN pip install flask       # runs at BUILD time — sets up the image
ENTRYPOINT ["python"]       # always runs at START — can't be overridden easily
CMD ["app.py"]              # runs at START — can be overridden at docker run
```

```bash
# CMD can be overridden:
docker run my-app python other.py    # overrides CMD

# ENTRYPOINT stays fixed:
docker run my-app other.py           # other.py becomes argument to python
```

---

*Next up → [07 - CI/CD Pipelines](./07-cicd-pipelines.md)* 🚀
