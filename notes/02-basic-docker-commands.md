# ⌨️ 02 — Basic Docker Commands

> My notes on essential Docker commands. Written in plain English as part of my DevOps bootcamp journey.

---

## 📌 Table of Contents

- [docker build vs docker pull](#docker-build-vs-docker-pull)
- [Checking Docker](#1-checking-docker)
- [Working with Images](#2-working-with-images)
- [Working with Containers](#3-working-with-containers)
- [Managing Containers](#4-managing-containers)
- [Inspecting Containers](#5-inspecting-containers)
- [Port Mapping](#6-port-mapping)
- [Docker Layers & Caching](#7-docker-layers--caching)
- [Cleaning Up](#8-cleaning-up)
- [Full Cheatsheet](#full-cheatsheet)

---

## docker build vs docker pull

This is an important distinction to understand before diving into commands:

| | `docker build` | `docker pull` / auto pull |
|--|---------------|--------------------------|
| **Used when** | You have written your **own** Dockerfile | You want a **pre-built** image from Docker Hub |
| **Example** | Your own Flask app | NGINX, MySQL, Python |
| **Requires a Dockerfile?** | ✅ Yes | ❌ No |
| **Who wrote the image?** | You | Someone else already did |

> **Simple rule:** Did YOU write a Dockerfile for it? → `docker build`. Is it a ready made image on Docker Hub? → just `docker run` and Docker handles the rest!

---

## 1. Checking Docker

Verify Docker is installed and running correctly:

```bash
# Check Docker version
docker --version

# See detailed info about your Docker setup
docker info
```

---

## 2. Working with Images

### Pulling an Image from Docker Hub
```bash
docker pull nginx
```
> Downloads the official NGINX image from Docker Hub onto your machine. Think of it like downloading an app.

### Building Your Own Image
```bash
docker build -t hello-flask .
```

| Part | What it means |
|------|--------------|
| `docker build` | Build an image from a Dockerfile |
| `-t hello-flask` | Tag/name the image `hello-flask` |
| `.` | Look for the Dockerfile in the current folder |

> Used when YOU have written a Dockerfile. The `.` at the end is important — it tells Docker where to find the Dockerfile!

### List All Images on Your Machine
```bash
docker images
```
> Shows all images you have downloaded or built locally.

### Delete an Image
```bash
docker rmi nginx
```
> `rmi` stands for **remove image**

---

## 3. Working with Containers

### Run a Container
```bash
docker run nginx
```
> Starts a container in the **foreground** — your terminal will be locked.

### Run in the Background (Detached Mode)
```bash
docker run -d nginx
```
> `-d` stands for **detached** — runs in the background and gives your terminal back. You'll use this most of the time!

### Run with a Name
```bash
docker run -d --name my-nginx nginx
```
> Giving containers names makes them much easier to manage than random IDs.

### Full Run Command Breakdown
```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

| Part | What it means |
|------|--------------|
| `docker run` | Create and start a container |
| `-d` | Run in the background |
| `-p 8080:80` | Port mapping — left is your laptop, right is the container |
| `--name my-nginx` | Name YOUR container `my-nginx` |
| `nginx` | The **image** to build the container from |

> ⚠️ Note: `--name my-nginx` is the name of your container. `nginx` at the end is the image it's built from. These are two different things!

---

## 4. Managing Containers

```bash
# See all RUNNING containers
docker ps

# See ALL containers including stopped ones
docker ps -a

# Stop a running container
docker stop my-nginx

# Start a stopped container
docker start my-nginx

# Restart a container
docker restart my-nginx

# Delete a stopped container
docker rm my-nginx

# Force delete a running container
docker rm -f my-nginx
```

> ⚠️ You need to stop a container before deleting it, unless you use `-f` to force it!

---

## 5. Inspecting Containers

```bash
# View logs of a container
docker logs my-nginx

# Follow logs in real time (live stream)
docker logs -f my-nginx

# Get inside a running container (like SSH-ing in!)
docker exec -it my-nginx bash
```

> `-f` in `docker logs -f` stands for **follow** — press `Ctrl + C` to stop.
> `-it` in `docker exec -it` stands for **interactive terminal** — type `exit` to get out of the container.

---

## 6. Port Mapping

Port mapping connects a port on your laptop to a port inside the container.

```bash
docker run -p LEFT:RIGHT hello-flask
```

| Side | Represents | What changes |
|------|-----------|-------------|
| **Left** | Port on your laptop | What you type in the browser |
| **Right** | Port inside the container | Where your app listens — must match your app! |

### Examples

```bash
# Same port on both sides
docker run -p 5002:5002 hello-flask
# Visit → http://localhost:5002

# Different ports
docker run -p 8080:5002 hello-flask
# Visit → http://localhost:8080

# Port 80 — no port number needed in browser!
docker run -p 80:5002 hello-flask
# Visit → http://localhost

# Run two copies of the same app on different ports
docker run -p 8081:5002 hello-flask
docker run -p 8082:5002 hello-flask
```

> 💡 **Key insight:** The left side can be anything you like. The right side must match whatever port your app is listening on inside the container — in Flask this is set in `app.py`!

---

## 7. Docker Layers & Caching

Every instruction in a Dockerfile creates a **layer**. Docker **caches** each layer — if nothing has changed, Docker reuses it instead of rebuilding, making builds much faster!

```
Layer 6 → CMD      ["python", "app.py"]
Layer 5 → EXPOSE   5002
Layer 4 → RUN      pip install flask
Layer 3 → COPY     . .
Layer 2 → WORKDIR  /app
Layer 1 → FROM     python:3.8-slim
```

### Layer Order Matters! ⚠️

Docker rebuilds a layer and **every layer after it** when something changes.

**❌ Less efficient — reinstalls Flask every time you change your code:**
```dockerfile
COPY . .              # Your code changes often
RUN pip install flask # Rebuilds every time because COPY changed!
```

**✅ More efficient — uses cached Flask install:**
```dockerfile
RUN pip install flask # Rarely changes — Docker caches this
COPY . .              # Only this layer rebuilds when you edit code
```

> 💡 **Rule of thumb:** Put things that change **rarely** at the top. Put things that change **often** at the bottom.

---

## 8. Cleaning Up

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove everything unused in one go
docker system prune
```

---

## Full Cheatsheet 📋

| Command | What it does |
|---------|-------------|
| `docker --version` | Check Docker version |
| `docker pull nginx` | Download an image from Docker Hub |
| `docker build -t my-app .` | Build an image from a Dockerfile |
| `docker images` | List all local images |
| `docker rmi nginx` | Delete an image |
| `docker run -d -p 8080:80 --name my-nginx nginx` | Run a container |
| `docker ps` | See running containers |
| `docker ps -a` | See all containers including stopped |
| `docker stop my-nginx` | Stop a container |
| `docker start my-nginx` | Start a stopped container |
| `docker restart my-nginx` | Restart a container |
| `docker rm my-nginx` | Delete a stopped container |
| `docker rm -f my-nginx` | Force delete a running container |
| `docker logs my-nginx` | View container logs |
| `docker logs -f my-nginx` | Follow logs in real time |
| `docker exec -it my-nginx bash` | Get inside a running container |
| `docker container prune` | Remove all stopped containers |
| `docker image prune` | Remove all unused images |
| `docker system prune` | Clean up everything unused |

---

*Next up → [03 - Dockerfile](./03-dockerfile.md)* 🚀