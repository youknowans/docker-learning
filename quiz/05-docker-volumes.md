# 🌶️ Docker Volumes — Quiz

> A self-test quiz covering Docker Volumes concepts including named volumes, bind mounts and persistent data.
> Completed as part of my DevOps bootcamp journey.

---

## 📌 How to Use This Quiz

1. Read each question and scenario carefully
2. Write down or think about your answer
3. Once you've answered all questions scroll down to the **Answers & Explanations** section at the bottom

---

## ❓ Questions

---

### Question 1 — Data Loss Scenario 💥

You run this command:

```bash
docker run -d \
  --name my-db \
  -e MYSQL_ROOT_PASSWORD=password \
  mysql:5.7
```

No volume is specified. You add 1000 records to the database then run `docker rm -f my-db`.

**What happens to the 1000 records?**

- A) They are saved automatically by Docker
- B) They are completely gone — no volume means data lives inside the container
- C) They are backed up to Docker Hub
- D) They are saved in the current folder on your laptop

---

### Question 2 — Volume vs Bind Mount 🌶️

What is the difference between these two commands?

```bash
# Command A
docker run -d \
  -v my-data:/var/lib/mysql \
  mysql:5.7

# Command B
docker run -d \
  -v /home/ansaff/mydata:/var/lib/mysql \
  mysql:5.7
```

- A) No difference — they both do the same thing
- B) Command A uses a Docker managed volume. Command B uses a bind mount — a specific folder on your laptop
- C) Command A uses a bind mount. Command B uses a Docker managed volume
- D) Command A only works on Linux. Command B works on any OS

---

### Question 3 — Development Setup 🔥

You are setting up a development environment for your Flask app. You want to edit code on your laptop and see changes instantly without rebuilding the image.

**Which approach do you use?**

- A) Docker Volume — mount a named volume into the container
- B) Bind Mount — mount your laptop code folder directly into the container
- C) No mount needed — just rebuild the image every time you change code
- D) tmpfs mount — store the code in memory

---

### Question 4 — Trick Question 🌀

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
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

You run `docker compose up -d` and add 500 records to the database.
Then you run `docker compose down` and `docker compose up -d` again.

**Are the 500 records still there?**

- A) No — docker compose down always deletes everything including volumes
- B) Yes — the volume persists data even after docker compose down
- C) No — you need to run docker compose restart to keep data
- D) Yes — but only the first 100 records are saved

---

### Question 5 — Missing Piece 🌶️🌶️

A colleague shows you this docker-compose.yml:

```yaml
version: '3'

services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
    volumes:
      - db-data:/var/lib/mysql
```

They say *"Something is wrong — the volume isn't working and data keeps disappearing!"*

**What is the problem?**

- A) The volume path /var/lib/mysql is wrong
- B) The volume db-data is mounted in the service but never defined at the bottom of the file under volumes:
- C) The MySQL image doesn't support volumes
- D) The environment variable name is wrong

---

### Question 6 — Dev vs Production 🌶️🌶️🌶️

A colleague shows you this docker-compose.yml:

```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5002:5002"
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

Your team lead looks at this and says:
*"This is great for development but you need to make two changes before this goes to production!"*

**What are the two changes?**

- A) Change the MySQL password and remove depends_on
- B) Remove the bind mount on web and add ports to the db service
- C) Remove the bind mount on web since you don't want live code editing in production, and make the password stronger using an env file
- D) Change the image version and remove the volumes section

---

### Question 7 — The Big One 🌶️🌶️🌶️🔥

Your manager gives you these requirements:

> *"Set up a complete development environment for a Flask MySQL app. Developers need to edit code and see changes instantly. Database data must persist between restarts. Password must be stored securely. Database must be hidden from internet!"*

**Which docker-compose.yml meets ALL requirements?**

**Option A:**
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
    env_file:
      - .env
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
      - "5002:5002"
    volumes:
      - .:/app
    depends_on:
      - db
  db:
    image: mysql:5.7
    env_file:
      - .env
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
      - "5002:5002"
    volumes:
      - .:/app
    depends_on:
      - db
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
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
      - "5002:5002"
    volumes:
      - .:/app
    depends_on:
      - db
  db:
    image: mysql:5.7
    env_file:
      - .env
volumes:
  db-data:
```

---
---

## ✅ Answers & Explanations

> ⚠️ **Spoiler Warning** — make sure you've attempted all questions before reading on!

---

### Question 1 — Answer: B) They are completely gone

**Explanation:**
No volume = data lives and dies with the container. Those 1000 records are gone forever the moment the container is deleted!

```
No volume → container deleted → data deleted 💥
With volume → container deleted → data safe in volume ✅
```

> 🧠 This is why every production database always uses a volume — you never want your data living inside a container!

---

### Question 2 — Answer: B) Command A = Docker volume. Command B = Bind mount

**Explanation:**
The key is what's on the **left side** of the colon:

```bash
-v my-data:/var/lib/mysql              # left = name → Docker Volume ✅
-v /home/ansaff/mydata:/var/lib/mysql  # left = path → Bind Mount ✅
```

> 🧠 Easy way to remember — starts with `/` → bind mount. Just a name → Docker volume!

---

### Question 3 — Answer: B) Bind Mount

**Explanation:**
A bind mount mounts your laptop folder directly into the container:

```yaml
volumes:
  - .:/app    # your laptop folder → mounted into /app in container
              # edit on laptop → container sees it instantly!
```

> 🔥 **Rule of thumb:**
> - Bind mount → development (live code editing)
> - Volume → production (persistent database data)

---

### Question 4 — Answer: B) Yes — volume persists data after docker compose down

**Explanation:**
This is a trick question! The key difference is:

```bash
docker compose down      # containers deleted — volumes SAFE ✅
docker compose down -v   # containers deleted — volumes GONE ❌
```

The `-v` flag is what deletes volumes. Without it volumes are always safe!

> ⚠️ Never run `docker compose down -v` in production — it's the nuclear option!

---

### Question 5 — Answer: B) Volume defined in service but not declared at bottom

**Explanation:**
Two parts are always required for volumes in Docker Compose:

```yaml
# ❌ Incomplete — missing bottom section!
services:
  db:
    volumes:
      - db-data:/var/lib/mysql  # referenced but never defined!

# ✅ Complete — both parts present!
services:
  db:
    volumes:
      - db-data:/var/lib/mysql  # PART 1 — mount into service

volumes:
  db-data:                      # PART 2 — define it here!
```

> 🧠 Think of it like declaring a variable in code — you can't use something you haven't defined!

---

### Question 6 — Answer: C) Remove bind mount and use env file for password

**Explanation:**
Two critical production changes:

**1. Remove the bind mount:**
```yaml
# Remove this for production!
volumes:
  - .:/app    # live code editing not needed in production
              # code should be baked into the image via Dockerfile!
```

**2. Never hardcode passwords:**
```yaml
# ❌ Development
environment:
  MYSQL_ROOT_PASSWORD: password

# ✅ Production
env_file:
  - .env      # store secrets here — never commit to GitHub!
```

> 🔒 **Golden rule:** Never commit passwords, API keys or secrets to GitHub — ever!

---

### Question 7 — Answer: B

**Explanation:**

Checking each requirement against Option B:

```yaml
web:
  volumes:
    - .:/app              # ✅ bind mount — live code editing!

db:
  env_file:
    - .env                # ✅ password stored securely!
  volumes:
    - db-data:/var/lib/mysql  # ✅ data persists!
                              # ✅ no ports on db — hidden!
volumes:
  db-data:                # ✅ volume properly defined!
```

Why the others fail:
- **Option A ❌** — No bind mount on web + db has `-p 3306:3306` exposing it publicly!
- **Option C ❌** — Password hardcoded in environment — not secure!
- **Option D ❌** — Volume `db-data` defined at bottom but never mounted in db service — data won't persist!

---

## 💡 Key Takeaways

- 💥 **No volume = data lost** when container is deleted — always use volumes for databases!
- 🔑 **Volume vs Bind Mount** — name = Docker volume, path starting with `/` = bind mount
- 🔥 **Bind mounts for dev** — edit code on laptop, changes appear instantly in container
- 💾 **Volumes for production** — persistent, Docker managed, survives container deletion
- ⚠️ **Two parts needed** — mount in service AND declare under `volumes:` at the bottom
- 🛡️ **docker compose down** — volumes safe. `docker compose down -v` — volumes gone!
- 🔒 **Never hardcode passwords** — always use `env_file` and `.env` files
- 🚫 **Remove bind mounts in production** — code should be baked into the Docker image

---

*Next up → [06 - Dockerfile](./06-dockerfile.md)* 🚀
