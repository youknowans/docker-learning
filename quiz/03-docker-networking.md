# 🌶️ Docker — Full Refresher Quiz

> A comprehensive self-test quiz covering everything learned so far — core concepts, commands, Dockerfiles and networking.
> Completed as part of my DevOps bootcamp journey.

---

## 📌 How to Use This Quiz

1. Read each question and scenario carefully
2. Write down or think about your answer
3. Once you've answered all questions scroll down to the **Answers & Explanations** section at the bottom

---

## ❓ Questions

---

### Question 1 — Real World Scenario 🌍

You're a junior DevOps engineer and you sit down at a new machine. You have no idea what's running on it.

**What are the FIRST two commands you run to understand the current state of the machine?**

- A) docker build and docker run
- B) docker ps -a and docker network ls
- C) docker images and docker system prune
- D) docker logs and docker inspect

---

### Question 2 — Security Scenario 🔒

You have this network setup:

```
app-network
│
├── db       → 172.19.0.2  (MySQL)
└── myapp    → 172.19.0.3  (Flask)
```

Your colleague says:
*"I can't connect to the database from my laptop browser — I need to add `-p 3306:3306` to the MySQL container!"*

**Should you let them do it?**

- A) Yes — databases always need port mapping to work
- B) No — the database should never be exposed to the internet, Flask handles the connection internally
- C) Yes — but only use -p 3306:3306 in development not production
- D) No — MySQL uses port 5432 not 3306

---

### Question 3 — Debugging Scenario 🕵️

You run:
```bash
docker network create app-network
docker run -d --name db -e MYSQL_ROOT_PASSWORD=password mysql:5.7
docker run -d --name myapp --network app-network -p 5002:5002 hello-flask-mysql
```

You visit `http://localhost:5002` and get a database connection error.

**What is the problem?**

- A) The Flask container is on the wrong port
- B) The MySQL container was started without --network app-network so Flask can't find it
- C) The MYSQL_ROOT_PASSWORD environment variable is wrong
- D) Flask needs to be restarted after MySQL starts

---

### Question 4 — Trick Question 🌀

Look at this `app.py` snippet:

```python
db = MySQLdb.connect(
    host="db",
    user="root",
    passwd="my-secret-pw",
    db="mysql"
)
```

You rename your MySQL container from `db` to `mysql-database` when running it.

**What happens when you visit the app?**

- A) It works fine — Docker automatically updates the hostname
- B) It fails — the app is still looking for host 'db' which no longer exists
- C) It works — Docker uses the IP address not the name to connect
- D) It fails — you need to rebuild the image after renaming

---

### Question 5 — Advanced Scenario 🌶️🌶️

You have three containers running on `app-network`:

```
app-network
│
├── frontend    (React app)
├── backend     (Flask API)
└── db          (MySQL)
```

Your manager asks:
*"I want the frontend accessible to the public, the backend only accessible to the frontend, and the database only accessible to the backend!"*

**How would you achieve this with Docker networking?**

- A) Put all three on the same network and add -p to all of them
- B) Put frontend and backend on one network, backend and db on another network. Only add -p to frontend
- C) Put each container on its own separate network so they're all isolated
- D) Docker networking can't achieve this level of control — use a firewall instead

---

### Question 6 — Error Scenario 🚨

You run this command and get this error:

```bash
docker run -d --name myapp --network app-network hello-flask-mysql

Error: No such network: app-network
```

**What is the most likely cause and fix?**

- A) The image doesn't exist — run docker build first
- B) The network doesn't exist yet — run docker network create app-network first
- C) Docker needs to be restarted — run sudo service docker restart
- D) The container name is already taken — run docker rm myapp first

---

### Question 7 — Commands 🌶️🌶️

You have a running Flask container called `myapp` that is currently on `app-network`. Your manager asks you to also connect it to a second network called `monitoring-network` **without stopping the container.**

**Which command do you use?**

- A) docker network create monitoring-network myapp
- B) docker run --network monitoring-network myapp
- C) docker network connect monitoring-network myapp
- D) docker network attach monitoring-network myapp

---

### Question 8 — Dockerfile Optimisation 🌶️🌶️

A colleague shows you this Dockerfile:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y gcc python3-dev libmariadb-dev pkg-config
RUN pip install flask mysqlclient
EXPOSE 5002
CMD ["python", "app.py"]
```

**They're complaining that every time they change one line of code in app.py the build takes ages. What's wrong and how do you fix it?**

- A) Nothing is wrong — builds always take a long time
- B) COPY is before the RUN commands — every code change triggers a full reinstall of system packages and pip libraries
- C) The FROM image is wrong — use a bigger base image to speed up builds
- D) They need a faster internet connection to speed up apt-get and pip

---

### Question 9 — Debugging 🌶️🌶️🌶️

You run `docker ps -a` and see this:

```bash
CONTAINER ID   IMAGE             STATUS                     NAMES
a1b2c3d4e5f6   hello-flask-mysql Exited (1) 2 minutes ago  myapp
b2c3d4e5f6a1   mysql:5.7         Up 2 minutes               db
```

**What are the TWO things you should do to diagnose why myapp crashed?**

- A) docker rm myapp and docker run it again
- B) docker logs myapp to see the error and docker network inspect to check if it's on the right network
- C) docker start myapp and hope it works this time
- D) docker build the image again and redeploy

---

### Question 10 — The Big One 🌶️🌶️🌶️🔥

Your manager sends you this message:

> *"Set up our Python Flask app that connects to MySQL. The app should be accessible on port 80. The database must be hidden. Name the network `prod-network`. The database password is `securepass123`."*

**Which is the complete correct solution?**

**Option A:**
```bash
docker network create prod-network

docker run -d --name db \
  --network prod-network \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=securepass123 \
  mysql:5.7

docker run -d --name myapp \
  --network prod-network \
  -p 80:5002 \
  hello-flask-mysql
```

**Option B:**
```bash
docker network create prod-network

docker run -d --name db \
  --network prod-network \
  -e MYSQL_ROOT_PASSWORD=securepass123 \
  mysql:5.7

docker run -d --name myapp \
  --network prod-network \
  -p 80:5002 \
  hello-flask-mysql
```

**Option C:**
```bash
docker run -d --name db \
  -e MYSQL_ROOT_PASSWORD=securepass123 \
  mysql:5.7

docker run -d --name myapp \
  --network prod-network \
  -p 80:5002 \
  hello-flask-mysql
```

**Option D:**
```bash
docker network create prod-network

docker run -d --name db \
  --network prod-network \
  -e MYSQL_ROOT_PASSWORD=securepass123 \
  mysql:5.7

docker run -d --name myapp \
  --network prod-network \
  -p 5002:80 \
  hello-flask-mysql
```

---
---

## ✅ Answers & Explanations

> ⚠️ **Spoiler Warning** — make sure you've attempted all questions before reading on!

---

### Question 1 — Answer: B) docker ps -a and docker network ls

**Explanation:**
`docker ps -a` shows every container (running or stopped) and `docker network ls` shows all networks. Together they give a full picture of what's going on before you touch anything.

> 🧠 Always **observe before you act** — a good DevOps engineer never runs commands blindly on an unknown machine!

---

### Question 2 — Answer: B) No — the database should never be exposed to the internet

**Explanation:**
This is a critical security principle. Databases should never be publicly accessible. Flask acts as the gatekeeper:

```
Internet → Flask (public) → MySQL (private, inside network only)
```

Exposing a database port publicly is one of the most common and dangerous security mistakes in real deployments!

---

### Question 3 — Answer: B) MySQL container was started without --network app-network

**Explanation:**
Looking at the commands:
```bash
docker run -d --name db \
  -e MYSQL_ROOT_PASSWORD=password \
  mysql:5.7                          # ❌ no --network app-network!

docker run -d --name myapp \
  --network app-network \            # ✅ Flask is on the network
  -p 5002:5002 \
  hello-flask-mysql
```

They're on completely different networks — Flask is shouting `db`'s name but `db` can't hear it!

---

### Question 4 — Answer: B) It fails — the app is still looking for host 'db'

**Explanation:**
The `host` value in your code must always match the container name exactly:

```python
host="db"         # app.py looks for a container called 'db'
```
```bash
--name db         # ✅ matches — works!
--name mysql-db   # ❌ doesn't match — connection error!
```

In a real team always agree on container names upfront and document them!

---

### Question 5 — Answer: B) Two networks — frontend+backend on one, backend+db on another

**Explanation:**
This is called **network segmentation**:

```bash
docker network create frontend-network
docker network create backend-network

# Frontend — public
docker run -d --name frontend --network frontend-network -p 80:3000 my-react-app

# Backend — on BOTH networks
docker run -d --name backend --network frontend-network my-flask-app
docker network connect backend-network backend

# Database — hidden
docker run -d --name db --network backend-network -e MYSQL_ROOT_PASSWORD=password mysql:5.7
```

> 🔒 **Defence in depth** — even if the frontend was hacked, the attacker still couldn't reach the database!

---

### Question 6 — Answer: B) Network doesn't exist — run docker network create first

**Explanation:**
You must always create the network before attaching containers to it:

```bash
docker network create app-network    # 1️⃣ create network first
docker run --network app-network ... # 2️⃣ then attach containers
```

> 🧠 Like building roads before opening shops — you can't tell a shop to be on a road that doesn't exist yet!

---

### Question 7 — Answer: C) docker network connect monitoring-network myapp

**Explanation:**
`docker network connect` lets you plug a running container into a new network with zero downtime:

```bash
docker network connect monitoring-network myapp    # connect
docker network disconnect monitoring-network myapp # disconnect
```

In real production systems you can't just stop containers whenever you want — users depend on them!

---

### Question 8 — Answer: B) COPY is before RUN commands

**Explanation:**
Every time `app.py` changes, Docker invalidates the `COPY` layer and rebuilds everything after it — including the slow system package install and pip install!

```dockerfile
# ❌ Slow
COPY . .                        # changes every time!
RUN apt-get install ...         # reinstalls every time!
RUN pip install flask mysqlclient

# ✅ Fast — fixed version
RUN apt-get install ...         # cached! rarely changes
RUN pip install flask mysqlclient  # cached!
COPY . .                        # only this rebuilds on code changes
```

Time difference: ❌ 3-5 minutes vs ✅ 10-15 seconds!

---

### Question 9 — Answer: B) docker logs and docker network inspect

**Explanation:**
The golden debugging rule:
1. `docker logs myapp` — what is the app actually saying?
2. `docker network inspect app-network` — is the container on the right network?

Never just restart and hope — always understand WHY it failed first!

---

### Question 10 — Answer: B

**Explanation:**

```bash
docker network create prod-network      # ✅ network created first
docker run -d --name db \
  --network prod-network \              # ✅ db on network
  -e MYSQL_ROOT_PASSWORD=securepass123 \# ✅ correct password
  mysql:5.7                             # ✅ no -p flag — db hidden!
docker run -d --name myapp \
  --network prod-network \              # ✅ myapp on same network
  -p 80:5002 \                          # ✅ accessible on port 80
  hello-flask-mysql
```

Why the others fail:
- Option A ❌ — db has `-p 3306:3306` exposing the database publicly!
- Option C ❌ — no `docker network create` and db has no `--network` flag
- Option D ❌ — port mapping is backwards! `-p 5002:80` maps laptop port 5002 to container port 80 — but Flask runs on 5002 inside!

---

## 💡 Key Takeaways

- 🕵️ **Always observe first** — `docker ps -a` and `docker network ls` before touching anything
- 🔒 **Never expose databases publicly** — no `-p` flag on database containers
- 🌐 **Custom networks enable DNS** — containers find each other by name not IP
- ⚠️ **Create network before attaching** — network must exist first
- 🔗 **docker network connect** — add running containers to networks with zero downtime
- 🥞 **Layer caching** — put RUN commands before COPY for faster builds
- 📝 **Container names matter** — host in your code must match the container name exactly
- 🏗️ **Network segmentation** — use multiple networks to control which containers can talk to each other

---

*Next up → [04 - Docker Compose](./04-docker-compose.md)* 🚀
