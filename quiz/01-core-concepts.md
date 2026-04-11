# 🧠 Docker Core Concepts — Quiz & Scenarios

> A self-test quiz with real world scenarios to reinforce understanding of Docker core concepts.
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

**Scenario:**
> Your friend is a developer and says: *"I built an app on my Windows laptop but when I deployed it to the Linux server it completely broke!"*

**What Docker concept would have prevented this problem?**

- A) Docker Hub — they should have uploaded it online first
- B) A Container — it packages the app with everything it needs to run the same on any machine
- C) Docker Compose — they should have used multiple containers
- D) A Dockerfile — they should have written better instructions

---

### Question 2 — Real World Scenario 🌍

**Scenario:**
> You have a Docker Image of your web app. Your boss asks you to run it on the dev server for testing, on the production server for real users, and on your local laptop for debugging.

**How many times do you need to build the image?**

- A) 3 times — once for each environment
- B) 2 times — once for dev and once for production
- C) 1 time — the same image runs everywhere
- D) 0 times — you don't need an image to run containers

---

### Question 3 — Trick Question 🌀

**Scenario:**
> A junior developer on your team says: *"I made some changes directly inside a running container — added some new files and updated some configs. I'm done for the day so I'm going to stop the container and pick it up tomorrow!"*

**What is the problem with what they just did?**

- A) Nothing — containers save changes automatically when stopped
- B) When the container stops all their changes will be lost
- C) They should have used Docker Compose instead
- D) They needed to push to Docker Hub before stopping

---

### Question 4 — Real World Scenario 🌍

**Scenario:**
> You're building a website that needs three things running at the same time — an NGINX web server, a Python backend and a MySQL database.

**What is the best Docker tool to manage all three together?**

- A) Run three separate Dockerfiles one by one
- B) Docker Compose — manage all containers together in one file
- C) Docker Hub — download all three images separately
- D) Just use one big container for everything

---

### Question 5 — Trick Question 🌀

**Scenario:**
> You need an NGINX web server container urgently. A colleague says: *"Don't waste time writing a Dockerfile from scratch — just grab the official NGINX image and run it straight away!"*

**Is your colleague right?**

- A) No — you always need to write a Dockerfile first before running anything
- B) No — Docker Hub images are not trustworthy
- C) Yes — you can pull a pre-built image from Docker Hub and run it instantly
- D) Yes — but only if you have Docker Compose installed

---

### Question 6 — Real World Scenario 🌍

**Scenario:**
> Your company's website suddenly gets a huge spike in traffic — 10x more users than normal. Your manager says: *"We need more capacity immediately — spin up more web servers NOW!"*

**What is the fastest Docker solution?**

- A) Write a new Dockerfile for each extra server needed
- B) Build a new image from scratch for each server
- C) Spin up multiple containers from the same existing image instantly
- D) Upload the image to Docker Hub and wait for it to scale automatically

---

### Question 7 — The Big Twist 🌀

**Complete the analogy:**

> *"A Dockerfile is to a Docker Image what a _______ is to a _______"*

- A) A house is to a blueprint
- B) A recipe is to a meal
- C) A cookie is to a cookie cutter
- D) A ship is to a shipping container

---
---

## ✅ Answers & Explanations

> ⚠️ **Spoiler Warning** — make sure you've attempted all questions before reading on!

---

### Question 1 — Answer: B) A Container

**Explanation:**
This is the core problem Docker was built to solve — the classic *"works on my machine"* nightmare. By packaging the app together with all its dependencies inside a container, it runs identically on Windows, Linux or Mac regardless of the environment.

---

### Question 2 — Answer: C) 1 time — the same image runs everywhere

**Explanation:**
This is one of Docker's biggest superpowers — **build once, run anywhere!** One image can be used to spin up as many containers as you need across any environment — dev, staging, production, local laptop. No rebuilding needed.

---

### Question 3 — Answer: B) When the container stops all their changes will be lost

**Explanation:**
Containers are **ephemeral** — a fancy word for *temporary*. Any changes made directly inside a running container are lost the moment it stops. The correct approaches are:
- Update the **Dockerfile** and rebuild the image with the changes baked in
- Use **Docker Volumes** to persist data outside the container (covered later in the bootcamp!)

---

### Question 4 — Answer: B) Docker Compose

**Explanation:**
Docker Compose is designed exactly for this situation. Instead of manually starting each container one by one, you define them all in a single `docker-compose.yml` file and bring them all up with just one command:

```bash
docker compose up
```

**Example docker-compose.yml:**
```yaml
version: '3'
services:
  web:
    image: nginx
  backend:
    image: python
  database:
    image: mysql
```

---

### Question 5 — Answer: C) Yes — your colleague is right!

**Explanation:**
Docker Hub has thousands of official pre-built images ready to use immediately. For well known tools like NGINX, MySQL, Python, Ubuntu etc — there is no need to build from scratch. You simply pull and run:

```bash
docker pull nginx
docker run nginx
```

> Always check the image is **official** or **verified** on Docker Hub for security!

---

### Question 6 — Answer: C) Spin up multiple containers from the same existing image instantly

**Explanation:**
Because containers start in **seconds** and all use the same image, you can scale from 1 to 10 to 100 containers almost instantly. This is what big companies like Netflix and Amazon do in production every single day — spinning up and tearing down containers automatically based on traffic demand. This is the foundation of what's called **container orchestration** which tools like Kubernetes build on!

---

### Question 7 — Answer: B) A recipe is to a meal

**Explanation:**
A **recipe** (Dockerfile) contains the instructions, and the **meal** (Image) is the finished packaged result.

> ⚠️ The trick option was **C) A cookie is to a cookie cutter** — this is **backwards**! In Docker terms:
> - The **cookie cutter** = the **Image** (the mould/blueprint)
> - The **cookie** = the **Container** (the actual running thing made from the mould)

**Full analogy breakdown:**

| Analogy | Docker Equivalent |
|---------|------------------|
| Recipe card | Dockerfile |
| Finished packaged meal | Docker Image |
| Meal served to a customer | Container |
| Restaurant head office with all recipes | Docker Hub |
| Running multiple restaurants | Docker Compose |

---

## 💡 Key Takeaways

- 📦 Containers solve the *"works on my machine"* problem by packaging everything an app needs
- 🔁 **Build once, run anywhere** — one image works across all environments
- ⚠️ **Containers are ephemeral** — changes made inside a running container are lost when it stops
- 🎻 **Docker Compose** manages multiple containers together with a single file
- 🌐 **Docker Hub** has thousands of ready made images — no need to build everything from scratch
- ⚡ Containers start in **seconds** making scaling fast and efficient
- 📄 A Dockerfile is the **recipe**, the Image is the **packaged meal**, the Container is the **served meal**

---

*Next up → [02 - Basic Docker Commands](./02-basic-docker-commands.md)* 🚀
