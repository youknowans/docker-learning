# 🌶️ Docker Compose & Networking — Refresher Quiz

> A self-test quiz covering Docker Compose and Docker Networking concepts.
> Completed as part of my DevOps bootcamp journey.

---

## 📌 How to Use This Quiz

1. Read each question and scenario carefully
2. Write down or think about your answer
3. Once you've answered all questions scroll down to the **Answers & Explanations** section at the bottom

---

## ❓ Questions

---

### Question 1 — Auto Networking 🌐

You have this docker-compose.yml:

```yaml
version: '3'

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

There is no network defined.

**Can the `web` and `db` containers still talk to each other?**

- A) No — you must always define a network in docker-compose.yml
- B) Yes — Docker Compose automatically creates a default network and puts all services on it
- C) No — you need to add --network flag to each service
- D) Yes — but only if they are on the same machine

---

### Question 2 — Service Name Trap 🌀

Your `app.py` connects to the database like this:

```python
db = MySQLdb.connect(
    host="database",
    user="root",
    passwd="my-secret-pw",
    db="mysql"
)
```

But your docker-compose.yml looks like this:

```yaml
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

**You visit `http://localhost:5002` and get a connection error. Why?**

- A) The port mapping is wrong — should be 3306:5002
- B) The host in app.py is 'database' but the service name in docker-compose.yml is 'db' — they don't match!
- C) The depends_on is in the wrong order
- D) MySQL needs an extra environment variable to work

---

### Question 3 — Trick Question 🌀

What does `depends_on` actually do in Docker Compose?

```yaml
services:
  web:
    build: .
    depends_on:
      - db
  db:
    image: mysql:5.7
```

- A) It waits until the database is fully ready before starting the web container
- B) It starts the db container before the web container but doesn't guarantee db is fully ready
- C) It connects the two containers to the same network
- D) It means web and db share the same volume

---

### Question 4 — Commands 🌶️

You run `docker compose up -d` and everything starts fine. You then make changes to your `app.py`.

**Which command do you run to rebuild the image and restart the containers with the changes?**

- A) docker compose up -d
- B) docker compose up -d --build
- C) docker compose restart
- D) docker compose build && docker compose start

---

### Question 5 — Logs 🌶️

You have three containers running via Docker Compose. Your manager asks you to check the live logs of just the `web` service.

**Which command do you use?**

- A) docker logs -f web
- B) docker compose logs -f web
- C) docker compose ps web
- D) docker compose inspect web

---

### Question 6 — Security 🔒

Your team lead reviews this docker-compose.yml and immediately flags a security issue:

```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5002:5002"
    depends_on:
      - db

  db:
    image: mysql:5.7
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
```

**What is the security issue?**

- A) The web service shouldn't have ports defined
- B) The MySQL password is too weak
- C) The db service has ports defined — this exposes the database publicly to the internet!
- D) The version should be '3.8' not '3'

---

### Question 7 — Data Persistence 🌶️🌶️

You run `docker compose down` and then `docker compose up -d` again.

Your colleague says:
*"All our database data will still be there — Docker Compose saves it automatically!"*

**Are they right?**

- A) Yes — Docker Compose automatically persists database data between restarts
- B) No — docker compose down destroys containers and all data inside them is lost
- C) Yes — but only if you used docker compose restart instead of down
- D) No — but the data is backed up to Docker Hub automatically

---

### Question 8 — The Big One 🌶️🌶️🌶️🔥

Your manager gives you these requirements:

> *"Set up a Flask web app with a MySQL database. The app runs on port 80. The database must be hidden from the internet. Data must persist even if containers are restarted. Use Docker Compose!"*

**Which docker-compose.yml meets ALL the requirements?**

**Option A:**
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "80:5002"
    depends_on:
      - db
  db:
    image: mysql:5.7
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    volumes:
      - db-data:/var/lib/mysql
volumes:
  db-data:
```

**Option B:**
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "80:5002"
    depends_on:
      - db
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    volumes:
      - db-data:/var/lib/mysql
volumes:
  db-data:
```

**Option C:**
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5002:80"
    depends_on:
      - db
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    volumes:
      - db-data:/var/lib/mysql
volumes:
  db-data:
```

**Option D:**
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "80:5002"
    depends_on:
      - db
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
volumes:
  db-data:
```

---
---

## ✅ Answers & Explanations

> ⚠️ **Spoiler Warning** — make sure you've attempted all questions before reading on!

---

### Question 1 — Answer: B) Yes — Docker Compose automatically creates a default network

**Explanation:**
When no network is defined Docker Compose quietly creates one named after your project folder and puts all services on it:

```
folder: flask-app
auto network: flask-app_default
```

You only need to define networks explicitly when you want custom names or more complex setups like network segmentation!

---

### Question 2 — Answer: B) host in app.py is 'database' but service name is 'db'

**Explanation:**
In Docker Compose the **service name** is automatically used as the hostname for container to container communication:

```yaml
services:
  db:    # ← this is the hostname!
```

```python
host="db"         # ✅ matches service name
host="database"   # ❌ no service called 'database' exists!
```

> ⚠️ This is slightly different from plain `docker run` where you use `--name` as the hostname. In Docker Compose the **service name IS the hostname!**

---

### Question 3 — Answer: B) Starts db before web but doesn't guarantee readiness

**Explanation:**
`depends_on` only controls **start order** not **readiness**. MySQL takes several seconds to fully initialise inside the container — `depends_on` doesn't wait for that!

```
db container starts → web starts immediately →
web tries to connect → MySQL still initialising → ❌ connection error!
```

The proper fix is a healthcheck:

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:5.7
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      retries: 5
```

> 🧠 `depends_on` = *"start db first"* not *"wait until db is ready"* — a very important distinction!

---

### Question 4 — Answer: B) docker compose up -d --build

**Explanation:**
```bash
docker compose up -d          # uses CACHED image — changes not picked up!
docker compose up -d --build  # rebuilds image THEN starts — picks up changes!
```

Always use `--build` when you've made code changes — one of the most common mistakes!

---

### Question 5 — Answer: B) docker compose logs -f web

**Explanation:**
```bash
docker compose logs -f        # follow ALL services
docker compose logs -f web    # follow ONLY web service ✅
docker compose logs -f db     # follow ONLY db service
```

Using `docker compose` commands is cleaner than hunting for container IDs with plain `docker` commands when working with Compose projects!

---

### Question 6 — Answer: C) db service has ports — exposes database publicly!

**Explanation:**
```yaml
db:
  ports:
    - "3306:3306"    # ❌ database exposed to entire internet!
```

The fix is simply removing `ports` from the db service:
```yaml
db:
  image: mysql:5.7   # ✅ no ports — hidden from internet
  environment:       #    web can still reach it internally!
    MYSQL_ROOT_PASSWORD: my-secret-pw
```

Containers on the same Docker Compose network can always talk internally without port mapping. Ports are only needed to expose something to the outside world!

---

### Question 7 — Answer: B) No — docker compose down destroys containers and all data

**Explanation:**
```bash
docker compose down    # stops AND deletes containers — data GONE! 💥
docker compose restart # stops and restarts — data preserved ✅
```

To properly persist data you need **volumes:**

```yaml
db:
  volumes:
    - db-data:/var/lib/mysql    # data stored outside container!

volumes:
  db-data:
```

> 💾 **Analogy:** A volume is like a **USB drive** plugged into the container — even when the container is thrown away the USB drive and its data remains!

---

### Question 8 — Answer: B

**Explanation:**

Breaking down why each option fails or succeeds:

**Option A ❌** — db has `ports: 3306:3306` which exposes the database publicly. Manager said database must be hidden!

**Option B ✅** — Perfect:
```yaml
ports:
  - "80:5002"              # ✅ app on port 80 as requested
                           # ✅ no ports on db — hidden!
volumes:
  - db-data:/var/lib/mysql # ✅ data persists!
volumes:
  db-data:                 # ✅ volume properly defined!
```

**Option C ❌** — Port mapping is backwards! `5002:80` means laptop port 5002 maps to container port 80 — but Flask runs on 5002 inside the container!

**Option D ❌** — Volume `db-data` is defined at the bottom but never mounted in the db service — data still won't persist!

---

## 💡 Key Takeaways

- 🌐 **Auto networking** — Docker Compose creates a default network automatically if none is defined
- 📛 **Service name = hostname** — containers find each other by service name in Compose, not container name
- ⚠️ **depends_on ≠ ready** — it controls start order only, not readiness. Use healthchecks for readiness!
- 🔨 **--build flag** — always use `docker compose up -d --build` after code changes
- 🔒 **Never expose db ports** — remove `ports:` from database services
- 💾 **Volumes persist data** — `docker compose down` destroys data without volumes
- 🗑️ **docker compose down -v** — deletes volumes too — use with extreme caution!

---

*Next up → [05 - Docker Volumes](./05-docker-volumes.md)* 🚀
