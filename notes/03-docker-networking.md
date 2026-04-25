# 🌐 03 — Docker Networking

> My notes on Docker Networking written in plain English as part of my DevOps bootcamp journey.

---

## 📌 Table of Contents

- [Why Docker Networking?](#why-docker-networking)
- [Network Types](#network-types)
  - [Bridge Network](#1-bridge-network)
  - [Host Network](#2-host-network)
  - [None Network](#3-none-network)
  - [Custom Bridge Network](#4-custom-bridge-network)
- [Key Commands](#key-commands)
- [Real World Example](#real-world-example)
- [Network Segmentation](#network-segmentation)
- [How It All Fits Together](#how-it-all-fits-together)
- [Quick Summary](#quick-summary)

---

## Why Docker Networking?

Containers are **isolated** by default — they can't interfere with each other. But in the real world containers need to **talk to each other!**

Think about a typical web app:
```
🌐 NGINX container    →   needs to talk to   →   🐍 Flask container
🐍 Flask container    →   needs to talk to   →   🗄️ MySQL container
```

Docker Networking controls this communication in a **controlled and secure way.**

> 🏘️ **Analogy:** Think of Docker networks like **neighbourhoods**. Containers in the same neighbourhood can talk to each other freely. Containers in different neighbourhoods can't — unless you build a road between them!

---

## Network Types

### 1. Bridge Network

- The **default** network — every container joins this automatically
- Containers on the same bridge network can talk to each other
- Containers are isolated from the outside world unless you wuse `-p` to open a port
- Best for containers running on a single machine

```bash
docker run -d --name flask-app hello-flask
docker run -d --name mysql-db mysql
```

> 🌉 **Analogy:** Think of it like a **private office building** — everyone inside can talk to each other, but outsiders need to be buzzed in through a specific door (port)!

---

### 2. Host Network

- The container shares your laptop/server's network directly
- No port mapping needed — the container uses your machine's ports directly
- Less isolation — the container is fully exposed to your network

```bash
docker run -d --network host hello-flask
```

> 🏠 **Analogy:** Think of it like **working from home** — you're directly on your home network, no building security!

---

### 3. None Network

- The container has no network access at all
- Completely isolated — can't talk to anything
- Used for security sensitive workloads

```bash
docker run -d --network none hello-flask
```

> 🏝️ **Analogy:** Like putting a container on a **desert island** — completely cut off from everything!

---

### 4. Custom Bridge Network

The default bridge network has a limitation — containers can only find each other using **IP addresses** which change every time a container restarts!

A custom bridge network lets containers find each other using their **names** instead:

```bash
docker network create my-network
docker run -d --name flask-app --network my-network hello-flask
docker run -d --name mysql-db --network my-network mysql
```

Now `flask-app` can talk to `mysql-db` just by using the name `mysql-db` — no IP address needed! ✅

> 📞 **Analogy:** Instead of memorising everyone's phone number (IP) you just look up their name in a contact book!

---

## Key Commands

```bash
# List all networks
docker network ls

# Create a new network
docker network create my-network

# Run a container on a specific network
docker run -d --network my-network --name my-app hello-flask

# Connect a RUNNING container to a network (no downtime!)
docker network connect my-network my-app

# Disconnect a container from a network
docker network disconnect my-network my-app

# Inspect a network — see which containers are on it
docker network inspect my-network

# Delete a network
docker network rm my-network
```

> ⚠️ Always create the network BEFORE attaching containers to it — you can't attach to a network that doesn't exist!

---

## Real World Example

Setting up a Flask app that connects to a MySQL database:

```bash
# Step 1 — Create a custom network
docker network create app-network

# Step 2 — Build the Flask image
docker build -t hello-flask-mysql .

# Step 3 — Start MySQL on the network (NO port mapping — hidden from internet!)
docker run -d \
  --name db \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  mysql:5.7

# Step 4 — Start Flask on the same network (port mapping — accessible publicly)
docker run -d \
  --name myapp \
  --network app-network \
  -p 5002:5002 \
  hello-flask-mysql
```

Flask connects to MySQL using the container name `db` in `app.py`:

```python
db = MySQLdb.connect(
    host="db",              # must match the container name exactly!
    user="root",
    passwd="my-secret-pw",
    db="mysql"
)
```

> ⚠️ The `host` value in your code must ALWAYS match the container name exactly. If you rename the container you must update the code too!

---

## Network Segmentation

For more complex apps you can use **multiple networks** to control exactly which containers can talk to each other:

```bash
# Create two networks
docker network create frontend-network
docker network create backend-network

# Frontend — exposed publicly
docker run -d --name frontend \
  --network frontend-network \
  -p 80:3000 my-react-app

# Backend — connects to BOTH networks (bridge between frontend and db)
docker run -d --name backend \
  --network frontend-network \
  my-flask-app
docker network connect backend-network backend

# Database — completely hidden, only backend can reach it
docker run -d --name db \
  --network backend-network \
  -e MYSQL_ROOT_PASSWORD=password \
  mysql:5.7
```

This produces a secure layered architecture:

```
Internet
    ↓
frontend (public via -p)
    ↓
[frontend-network]
    ↓
backend (no -p — only reachable from frontend)
    ↓
[backend-network]
    ↓
db (no -p — only reachable from backend)
```

> 🔒 This is called **defence in depth** — even if the frontend was hacked, the attacker still couldn't reach the database!

---

## How It All Fits Together

```
Internet
    ↓
 -p 5002:5002 (port mapping opens this door)
    ↓
┌─────────────────────────────┐
│        app-network          │
│                             │
│  [myapp] ←→ [db]           │
│  172.19.0.3   172.19.0.2   │
└─────────────────────────────┘
```

Only Flask is exposed to the internet via port mapping. MySQL stays hidden inside the network — much more secure!

---

## Quick Summary

| Network Type | Containers talk to each other | Exposed to internet | Best for |
|-------------|------------------------------|---------------------|---------|
| Bridge (default) | ✅ Same network only | Only via `-p` | Single machine apps |
| Host | ✅ | ✅ Fully exposed | Full network access needed |
| None | ❌ | ❌ | Maximum isolation |
| Custom Bridge | ✅ By name! | Only via `-p` | ✅ Best practice for multi-container apps |

---

## Common Mistakes to Avoid ⚠️

- ❌ Forgetting `--network` flag when running a container — it ends up on the default network and can't find other containers
- ❌ Exposing database ports publicly with `-p` — databases should never be accessible from the internet
- ❌ Container name in code not matching actual container name — always double check!
- ❌ Trying to attach to a network before creating it — always `docker network create` first
- ❌ Typos in environment variable names — `MYSQL_ROOT_PASSWPRD` instead of `MYSQL_ROOT_PASSWORD`!

---

*Next up → [04 - Docker Compose](./04-docker-compose.md)* 🚀
