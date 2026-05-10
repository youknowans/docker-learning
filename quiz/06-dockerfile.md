# 🌶️ Dockerfile Anatomy — Quiz

> A self-test quiz covering Dockerfile instructions, best practices, layer caching, security and multi-stage builds.
> Completed as part of my DevOps bootcamp journey.

---

## 📌 How to Use This Quiz

1. Read each question and scenario carefully
2. Write down or think about your answer
3. Once you've answered all questions scroll down to the **Answers & Explanations** section at the bottom

---

## ❓ Questions

---

### Question 1 — The Foundation 🏗️

You are writing a Dockerfile for a Python Flask app. What is the FIRST instruction you must always write?

```dockerfile
???

WORKDIR /app
RUN pip install flask
COPY . .
CMD ["python", "app.py"]
```

- A) CMD ["python", "app.py"]
- B) WORKDIR /app
- C) FROM python:3.8-slim
- D) RUN pip install flask

---

### Question 2 — RUN vs CMD 🌶️

What is the difference between these two instructions?

```dockerfile
RUN pip install flask

CMD ["python", "app.py"]
```

- A) No difference — they both run commands
- B) RUN executes during image BUILD. CMD executes when the container STARTS
- C) CMD executes during image BUILD. RUN executes when the container STARTS
- D) RUN is for Python commands. CMD is for shell commands

---

### Question 3 — Layer Caching 🌶️

Your colleague writes this Dockerfile and complains that every time they change one line in `app.py` the build takes ages because pip reinstalls everything:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5002
CMD ["python", "app.py"]
```

**What is wrong and how do you fix it?**

- A) Use a faster base image
- B) COPY . . comes before RUN pip install — every code change invalidates the pip cache. Copy requirements.txt first, pip install, then COPY . .
- C) Move CMD to the top of the Dockerfile
- D) Add --no-cache to the pip install command

---

### Question 4 — EXPOSE Trap 🌀

What does `EXPOSE 5002` actually do in a Dockerfile?

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5002
CMD ["python", "app.py"]
```

- A) Opens port 5002 on your laptop so you can visit the app in the browser
- B) Automatically maps port 5002 to the container
- C) Documents that the app uses port 5002 — it does NOT actually open the port!
- D) Blocks all other ports except 5002

---

### Question 5 — Security 🔒

Your colleague shows you this Dockerfile and asks why it's a security risk:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install flask
ENV DB_PASSWORD=supersecret123
EXPOSE 5002
CMD ["python", "app.py"]
```

**What is the security issue?**

- A) The base image is wrong
- B) The password is hardcoded in ENV — it gets baked into the image and anyone who has the image can see it!
- C) EXPOSE is a security risk
- D) The CMD instruction exposes the app publicly

---

### Question 6 — Multi-Stage Builds 🌶️🌶️

Look at these two Dockerfiles. Which one produces a smaller and more secure final image?

```dockerfile
# Dockerfile A
FROM python:3.8
WORKDIR /app
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```dockerfile
# Dockerfile B
FROM python:3.8 AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "app.py"]
```

- A) Dockerfile A — simpler is always better
- B) Dockerfile B — multi-stage build produces a smaller image with only what's needed
- C) Both produce the same size image
- D) Dockerfile A — it installs fewer packages

---

### Question 7 — Production Improvements 🌶️🌶️🌶️

Your team lead says there are **three things** to improve in this Dockerfile before it goes to production:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev
RUN pip install flask mysqlclient
COPY . .
EXPOSE 5002
CMD ["python", "app.py"]
```

**What are the three improvements?**

- A) Change the base image, add a .dockerignore, and move CMD to the top
- B) Clean up after apt-get install, copy requirements.txt before COPY . . for caching, and add a non-root USER
- C) Remove EXPOSE, add ENV variables, and use a different base image
- D) Add LABEL, remove WORKDIR, and use RUN instead of CMD

---

### Question 8 — The Big One 🌶️🌶️🌶️🔥

Your manager asks you to write a production ready Dockerfile for a Flask MySQL app. **Which one is correct?**

**Option A:**
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y \
    gcc python3-dev libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install flask mysqlclient
EXPOSE 5002
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```

**Option B:**
```dockerfile
FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc python3-dev libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5002
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```

**Option C:**
```dockerfile
FROM python:latest
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc python3-dev libmariadb-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DB_PASSWORD=supersecret123
EXPOSE 5002
CMD ["python", "app.py"]
```

**Option D:**
```dockerfile
FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc python3-dev libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5002
ENV DB_PASSWORD=supersecret123
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```

---
---

## ✅ Answers & Explanations

> ⚠️ **Spoiler Warning** — make sure you've attempted all questions before reading on!

---

### Question 1 — Answer: C) FROM python:3.8-slim

**Explanation:**
`FROM` is always the first instruction — every Dockerfile must start with it. It specifies the base image to build on top of.

```dockerfile
FROM python:3.8-slim    # ← always first!
WORKDIR /app
RUN pip install flask
COPY . .
CMD ["python", "app.py"]
```

> 🧠 `FROM` is the **foundation** — you can't build anything without telling Docker what to build on top of!

---

### Question 2 — Answer: B) RUN = BUILD time. CMD = container START time

**Explanation:**
The most important distinction in any Dockerfile:

```dockerfile
RUN pip install flask      # 🔨 BUILD time — sets up the image once
CMD ["python", "app.py"]   # 🚀 RUN time — starts the app every time container starts
```

> 🏠 **Analogy:**
> - `RUN` = building and furnishing the house
> - `CMD` = the moment you move in and start living!

---

### Question 3 — Answer: B) COPY . . before pip install kills layer caching

**Explanation:**
Docker caches layers — when a layer changes everything after it rebuilds. `COPY . .` changes every time you edit any file, so putting it before `pip install` means packages reinstall every single build!

```dockerfile
# ❌ Before — slow!
COPY . .                             # changes every time!
RUN pip install -r requirements.txt  # reinstalls every time!

# ✅ After — fast!
COPY requirements.txt .              # only changes when dependencies change
RUN pip install -r requirements.txt  # cached until requirements change!
COPY . .                             # only this rebuilds on code changes
```

> 🧠 **Golden rule:** Things that change **rarely** go at the TOP — things that change **often** go at the BOTTOM!

---

### Question 4 — Answer: C) Documents the port — does NOT open it!

**Explanation:**
`EXPOSE` is just a label — nothing more! It does not open, map or publish any ports.

```dockerfile
EXPOSE 5002    # 📝 just documentation
               # does NOT open anything!
```

The actual port opening happens with `-p` in docker run:
```bash
docker run -p 5002:5002 my-app    # THIS actually opens the port!
```

> 🚪 **Think of it like this:**
> - `EXPOSE 5002` = putting a sign on a door saying "this door exists"
> - `-p 5002:5002` = actually unlocking and opening the door!

---

### Question 5 — Answer: B) Password hardcoded in ENV — baked into image!

**Explanation:**
Anything set with `ENV` in a Dockerfile gets permanently baked into the image. Anyone with access to the image can run `docker inspect` and see all environment variables in plain text!

```dockerfile
# ❌ NEVER do this!
ENV DB_PASSWORD=supersecret123    # visible to anyone with the image!
```

The correct approach:
```bash
# ✅ Pass at runtime
docker run -e DB_PASSWORD=supersecret123 my-app

# ✅ Use env_file in docker-compose.yml
env_file:
  - .env    # never commit this to GitHub!
```

> 🔒 **Golden rule:** Never hardcode secrets in a Dockerfile — never commit `.env` files to GitHub!

---

### Question 6 — Answer: B) Dockerfile B — multi-stage build

**Explanation:**
Multi-stage builds use multiple FROM statements to produce a smaller, cleaner final image:

```
Dockerfile A — single stage:
python:3.8 + gcc + build tools + packages + code = 900MB+ 😱

Dockerfile B — multi stage:
python:3.8-slim + packages + code only = ~100MB ✅
```

The key line:
```dockerfile
COPY --from=builder /root/.local /root/.local  # only grab installed packages
                                                # leave gcc and build tools behind!
```

> 🪑 **Analogy:** Like flat pack furniture — use all the tools to build it, then throw them away. Only keep the finished furniture!

---

### Question 7 — Answer: B) Clean up apt-get, fix COPY order, add non-root USER

**Explanation:**
Three production improvements:

**Fix 1 — Clean up after apt-get:**
```dockerfile
RUN apt-get update && apt-get install -y \
    gcc python3-dev libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*    # ✅ reduces image size!
```

**Fix 2 — Requirements before code:**
```dockerfile
COPY requirements.txt .               # ✅ cached until dependencies change!
RUN pip install flask mysqlclient
COPY . .                              # ✅ only code layer rebuilds!
```

**Fix 3 — Non-root user:**
```dockerfile
RUN useradd -m appuser
USER appuser                          # ✅ security best practice!
CMD ["python", "app.py"]
```

| Fix | Why it matters |
|-----|---------------|
| Clean up apt-get | Removes cached package lists — reduces image size |
| Requirements first | Pip install cached — saves minutes on every build |
| Non-root user | If hacked attacker gets limited access not full root! |

---

### Question 8 — Answer: B

**Explanation:**

**Option A ❌** — `COPY . .` comes before `RUN pip install` — kills layer caching! Every code change triggers a full reinstall!

**Option B ✅ — Perfect:**
```dockerfile
FROM python:3.8-slim              # ✅ specific slim image
RUN apt-get install ... \
    && rm -rf /var/lib/apt/lists/* # ✅ cleans up after apt-get!
COPY requirements.txt .           # ✅ requirements before code!
RUN pip install -r requirements.txt # ✅ cached until requirements change!
COPY . .                          # ✅ code copied last!
RUN useradd -m appuser            # ✅ non-root user created!
USER appuser                      # ✅ runs securely!
CMD ["python", "app.py"]          # ✅ correct startup command!
```

**Option C ❌** — Three problems:
- `FROM python:latest` — unpredictable in production!
- No `rm -rf /var/lib/apt/lists/*` — bloated image!
- `ENV DB_PASSWORD=supersecret123` — hardcoded secret!

**Option D ❌** — Fatal mistake:
- `ENV DB_PASSWORD=supersecret123` — secret baked into image forever!

---

## 💡 Key Takeaways

- 🏗️ **FROM is always first** — the foundation of every Dockerfile
- 🔨 **RUN = build time** — use for installing software and setting things up
- 🚀 **CMD = run time** — use for starting your app
- 📝 **EXPOSE is just documentation** — does NOT open ports! Use `-p` for that!
- 🔒 **Never hardcode secrets** — use env files passed at runtime
- 🥞 **Layer caching** — copy requirements.txt before COPY . . for fast builds
- 🧹 **Clean up apt-get** — always add `&& rm -rf /var/lib/apt/lists/*`
- 👤 **Non-root user** — always add USER instruction for production security
- 🏭 **Multi-stage builds** — smaller, faster, more secure production images
- 🏷️ **Use specific tags** — never use `latest` in production!

---

*Next up → [07 - CI/CD Pipelines](./07-cicd-pipelines.md)* 🚀
