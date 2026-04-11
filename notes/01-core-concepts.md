# 🐳 01 — Docker Core Concepts

> These are my personal notes on Docker core concepts written in plain English as part of my DevOps bootcamp journey.

---

## 📌 Table of Contents

- [What is a Container?](#what-is-a-container)
- [What is Docker?](#what-is-docker)
- [Docker vs Virtual Machines](#docker-vs-virtual-machines)
- [Core Concepts](#core-concepts)
  - [Dockerfile](#1-dockerfile)
  - [Docker Image](#2-docker-image)
  - [Docker Container](#3-docker-container)
  - [Docker Hub](#4-docker-hub)
  - [Docker Compose](#5-docker-compose)
- [How It All Fits Together](#how-it-all-fits-together)
- [Key Takeaways](#key-takeaways)

---

## What is a Container?

Imagine you've built an app on your laptop and it works perfectly. But when you send it to a colleague or deploy it to a server — it breaks. They say *"it doesn't work on my machine!"*

This happens because different computers have:
- Different operating systems
- Different software versions
- Different settings and configurations

A **container** solves this by packaging your app **together with everything it needs to run** — the code, settings, libraries and dependencies — all in one neat box. It then runs the same way on **any** machine.

> 🚢 **Analogy:** Think of it like a **shipping container**. Before shipping containers existed, goods were loaded onto ships in all different shapes and sizes causing chaos. The shipping container standardised everything — same box, works on any ship, any port, anywhere in the world.

---

## What is Docker?

Docker is the most popular **tool for creating and running containers**. It's the software that:

- **Builds** containers
- **Runs** containers
- **Manages** containers

> 🚢 **Analogy:** If containers are shipping containers, Docker is the **shipping company** that manages all of them.

---

## Docker vs Virtual Machines

You might hear about Virtual Machines (VMs) — here's the key difference:

| | Virtual Machine | Docker Container |
|--|----------------|-----------------|
| Size | Gigabytes | Megabytes |
| Startup time | Minutes | Seconds |
| Has its own OS | ✅ Yes | ❌ No (shares host OS) |
| Isolation | Full | Process level |
| Performance | Slower | Much faster |

> 🏠 **Analogy:** A VM is like building a **whole new house** for each app. A container is like giving each app its **own room** in the same house — much more efficient!

---

## Core Concepts

### 1. Dockerfile

A **Dockerfile** is a plain text file with step by step instructions that tells Docker how to build your app.

> 📋 **Analogy:** Think of it as a **recipe card** — step by step instructions for making your app.

**Example Dockerfile:**
```dockerfile
FROM ubuntu                           # Start with Ubuntu as the base
RUN apt update                        # Update the software list
RUN apt install -y nginx              # Install NGINX
COPY index.html /var/www/html         # Copy our webpage in
CMD ["nginx", "-g", "daemon off;"]    # Start NGINX
```

Each line is an instruction Docker follows **top to bottom** when building your image.

---

### 2. Docker Image

A **Docker Image** is what you get when Docker reads and executes your Dockerfile — a ready to use, packaged version of your app.

> 🍪 **Analogy:** The Dockerfile is the **cookie cutter**, the image is the **shape/mould** — use it to stamp out as many identical containers as you want.

**Key things to know:**
- Images are **read only** — you cannot change them once built
- Images are made up of **layers** — each line in your Dockerfile creates a layer
- Think of layers like a **stack of pancakes** — each one adds something on top

```
Layer 4 → CMD   (start NGINX)
Layer 3 → COPY  (our webpage)
Layer 2 → RUN   (install NGINX)
Layer 1 → FROM  (Ubuntu base)
```

---

### 3. Docker Container

A **container** is a running instance of an image — your app actually executing.

> 🍪 **Analogy:** If the image is the cookie cutter/mould, the container is the **actual cookie** — the real running thing!

**Key things to know:**
- You can run **multiple containers** from the same image
- Containers are **isolated** — they can't interfere with each other or your computer
- They are **lightweight** — they share your computer's OS instead of needing their own like a VM
- When a container stops, any changes inside it are **lost** unless saved using volumes

---

### 4. Docker Hub

**Docker Hub** is the official online library of pre-built images at [hub.docker.com](https://hub.docker.com)

> 📱 **Analogy:** Think of it like an **app store for containers** — instead of building everything from scratch, download a ready made image.

**Popular images available:**

| Image | What it is |
|-------|-----------|
| `nginx` | Web server |
| `mysql` | Database |
| `python` | Python environment |
| `ubuntu` | Base Ubuntu system |
| `node` | Node.js environment |

---

### 5. Docker Compose

Real world apps rarely run as just one container. A typical web app might need:

- A **web server** container (NGINX)
- A **backend** container (Python/Node.js)
- A **database** container (MySQL)

**Docker Compose** lets you define and run all of these together using a single file called `docker-compose.yml`

> 🎻 **Analogy:** Think of Docker Compose as a **conductor leading an orchestra** — each instrument (container) plays its part, and the conductor keeps them all in sync.

**Example docker-compose.yml:**
```yaml
version: '3'
services:
  web:
    image: nginx
  database:
    image: mysql
```

---

## How It All Fits Together

Here's the full Docker workflow from start to finish:

```
Write           Build             Push              Pull & Run
Dockerfile  →   Docker Image  →   Docker Hub   →   Container
(Recipe)        (Packaged app)    (App Store)       (Running app)
```

**Restaurant analogy to tie it all together:**

| Restaurant World | Docker World |
|-----------------|--------------|
| Recipe card | Dockerfile |
| Prepared meal ready to serve | Docker Image |
| Actual meal served to a customer | Container |
| Head office with all recipes | Docker Hub |
| Running multiple restaurants | Docker Compose |

---

## Key Takeaways

- 🐳 **Docker** is a tool for building and running containers
- 📄 **Dockerfile** — the recipe/instructions for building your app
- 📦 **Image** — the packaged, ready to use version of your app (read only)
- 🏃 **Container** — a running instance of an image
- 🌐 **Docker Hub** — online library of pre-built images
- 🎻 **Docker Compose** — tool for running multiple containers together
- ⚡ **Containers are faster and lighter than Virtual Machines** because they share the host OS

---

*Next up → [02 - Basic Docker Commands](./02-basic-docker-commands.md)* 🚀

