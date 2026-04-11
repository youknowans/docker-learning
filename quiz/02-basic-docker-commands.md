# 🌶️ Docker Basic Commands — Spicy Quiz & Scenarios

> A challenging self-test quiz with real world scenarios to reinforce understanding of Docker basic commands.
> Completed as part of my DevOps bootcamp journey.

---

## 📌 How to Use This Quiz

1. Read each question and scenario carefully
2. Write down or think about your answer
3. Once you've answered all questions scroll down to the **Answers & Explanations** section at the bottom

---

## ❓ Questions

---

### Question 1 — Port Mapping Trap 🌶️

You run this command:

```bash
docker run -d -p 3000:5002 --name my-app hello-flask
```

Your mate tries to visit the app by going to `http://localhost:5002` in their browser on the same laptop.

**What happens and why?**

- A) It works fine — Flask is running on 5002 inside the container
- B) It doesn't load — the app is only accessible on port 3000 on the laptop
- C) It crashes — you can't use different port numbers
- D) It works — Docker automatically redirects 5002 to 3000

---

### Question 2 — Layer Caching 🌶️

You have this Dockerfile:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5002
CMD ["python", "app.py"]
```

You build and run it successfully. Then you make a **tiny change to app.py** and rebuild.

**Which layers does Docker actually rebuild?**

- A) All layers from scratch every time
- B) Only the CMD layer — that's the one that runs the app
- C) COPY and everything after it — RUN pip install flask runs again too
- D) Only the COPY layer — Docker is smart enough to skip pip install

---

### Question 3 — Containers vs Images 🌶️

You run:
```bash
docker stop my-nginx
docker rm my-nginx
docker run -d -p 8080:80 --name my-nginx nginx
```

Your colleague says:
*"You deleted the container so you'll need to run docker pull nginx again to get the image back before running it!"*

**Are they right?**

- A) Yes — deleting the container deletes the image too
- B) No — deleting a container does not delete the image, docker run will work fine
- C) Yes — but only if you used docker rm -f
- D) No — but you do need to run docker pull to refresh it

---

### Question 4 — Scaling Containers 🌶️🌶️

You want to run **three copies** of your Flask app at the same time on the same laptop.

**Which of these commands would work?**

- A) You can't run more than one container from the same image

- B) Run the same command three times:
```bash
docker run -d -p 5002:5002 hello-flask
docker run -d -p 5002:5002 hello-flask
docker run -d -p 5002:5002 hello-flask
```

- C) Use different names but same ports:
```bash
docker run -d -p 5002:5002 --name app1 hello-flask
docker run -d -p 5002:5002 --name app2 hello-flask
docker run -d -p 5002:5002 --name app3 hello-flask
```

- D) Use different names AND different left side ports:
```bash
docker run -d -p 5002:5002 --name app1 hello-flask
docker run -d -p 5003:5002 --name app2 hello-flask
docker run -d -p 5004:5002 --name app3 hello-flask
```

---

### Question 5 — Ephemeral Containers 🌶️🌶️

You run:
```bash
docker exec -it my-nginx bash
```
Once inside the container you create a new file:
```bash
echo "hello" > /app/myfile.txt
exit
```
Then you stop and delete the container and start a brand new one from the same image:
```bash
docker rm -f my-nginx
docker run -d -p 8080:80 --name my-nginx nginx
docker exec -it my-nginx bash
ls /app/
```

**What do you see when you run `ls /app/`?**

- A) myfile.txt is there — Docker saves files between containers
- B) myfile.txt is gone — containers are ephemeral, changes don't persist
- C) An error — the /app folder doesn't exist in NGINX
- D) myfile.txt is there — because we used the same image

---

### Question 6 — docker system prune 🌶️🌶️

A junior DevOps engineer on your team runs:

```bash
docker system prune
```

They panic and ask *"Did I just delete all my Docker images and containers?!"*

**What did `docker system prune` actually delete?**

- A) Everything — all images, all containers, all data. Total wipe!
- B) Only stopped containers and unused images — running containers and their images are safe
- C) Only stopped containers — images are never touched by prune
- D) Nothing — prune just shows what could be deleted without actually deleting

---

### Question 7 — docker run vs docker start 🌶️🌶️🌶️

You see these two commands:

```bash
# Command A
docker run -d -p 8080:80 nginx

# Command B
docker start my-nginx
```

**What is the key difference between `docker run` and `docker start`?**

- A) No difference — they both start a container the same way
- B) docker run creates and starts a BRAND NEW container. docker start restarts an already EXISTING stopped container
- C) docker start is newer and better — you should always use it instead of docker run
- D) docker run is for images from Docker Hub. docker start is for images you built yourself

---

### Question 8 — Updating a Dockerfile 🌶️🌶️🌶️🔥

You have this Dockerfile:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5002
CMD ["python", "app.py"]
```

Your manager asks you to:
1. Install a second library called `requests` alongside Flask
2. Change the app to run on port `8000` instead of `5002`

**Without changing `app.py` — which Dockerfile lines need to change and what do you change them to?**

- A) Change RUN to `pip install flask requests` and change EXPOSE to 8000
- B) Change CMD to include requests and change WORKDIR to 8000
- C) Change FROM to include requests and change COPY to port 8000
- D) Only change EXPOSE to 8000 — Docker handles library installs automatically

---
---

## ✅ Answers & Explanations

> ⚠️ **Spoiler Warning** — make sure you've attempted all questions before reading on!

---

### Question 1 — Answer: B) It doesn't load — the app is only accessible on port 3000

**Explanation:**

```bash
docker run -d -p 3000:5002 --name my-app hello-flask
#                 ↑     ↑
#              laptop  container
```

Flask IS running on `5002` — but that's inside the container. From your laptop you can only reach it through the LEFT side which is `3000`. Port `5002` on your laptop is not mapped to anything.

```
✅ http://localhost:3000  ← works!
❌ http://localhost:5002  ← nothing there on your laptop!
```

> 🧠 **Key rule:** Always look at the **LEFT side** of `-p` for what you type in the browser. The right side is internal to the container only!

---

### Question 2 — Answer: C) COPY and everything after it — RUN pip install flask runs again too

**Explanation:**

When Docker detects a layer has changed it rebuilds that layer **and every single layer after it** — no exceptions!

```dockerfile
FROM python:3.8-slim    # ✅ Cached
WORKDIR /app            # ✅ Cached
COPY . .                # ❌ Changed! (app.py was edited)
RUN pip install flask   # ❌ Rebuilds — even though flask didn't change!
EXPOSE 5002             # ❌ Rebuilds
CMD ["python", "app.py"]# ❌ Rebuilds
```

This is exactly why layer order matters. Swapping `COPY` and `RUN` would cache the pip install:

```dockerfile
FROM python:3.8-slim    # ✅ Cached
WORKDIR /app            # ✅ Cached
RUN pip install flask   # ✅ Cached — flask didn't change!
COPY . .                # ❌ Rebuilds — but this is fast!
EXPOSE 5002             # ❌ Rebuilds
CMD ["python", "app.py"]# ❌ Rebuilds
```

> 💡 **Rule of thumb:** Put things that change **rarely** at the top. Put things that change **often** at the bottom.

---

### Question 3 — Answer: B) No — deleting a container does not delete the image

**Explanation:**

Containers and images are completely separate things!

```
docker rm my-nginx    ← deletes the CONTAINER 🏃
                         image still sits on your machine 📦
docker rmi nginx      ← this would delete the IMAGE
```

> 🍪 **Analogy:** Deleting a container is like throwing away a meal — the recipe (image) is still in your kitchen ready to make another one instantly!

---

### Question 4 — Answer: D) Different names AND different left side ports

**Explanation:**

Running the same command three times fails for two reasons:

**Problem 1 — Port conflict:**
```bash
docker run -d -p 5002:5002 --name app1 hello-flask  # ✅ Works
docker run -d -p 5002:5002 --name app2 hello-flask  # ❌ Port 5002 already taken!
docker run -d -p 5002:5002 --name app3 hello-flask  # ❌ Port 5002 already taken!
```
Two containers can't use the same port on your laptop at the same time!

**Problem 2 — Name conflict:**
You can't have two containers with the same name — Docker throws an error.

**The correct approach:**
```bash
docker run -d -p 5002:5002 --name app1 hello-flask  # visit localhost:5002
docker run -d -p 5003:5002 --name app2 hello-flask  # visit localhost:5003
docker run -d -p 5004:5002 --name app3 hello-flask  # visit localhost:5004
```

> The right side stays `5002` because Flask is always listening on `5002` inside every container — only the left side ports and names change!

---

### Question 5 — Answer: B) myfile.txt is gone — containers are ephemeral

**Explanation:**

Containers are **ephemeral** — meaning temporary. Any changes made directly inside a running container are lost the moment it's deleted. The image it was built from is completely untouched.

> 🧠 This is exactly why **Docker Volumes** exist — they let you store data outside the container so it persists even when the container is deleted. You'll cover this later in the bootcamp!

---

### Question 6 — Answer: B) Only stopped containers and unused images — running containers and their images are safe

**Explanation:**

`docker system prune` only cleans up things that aren't actively being used:

```
✅ Stopped containers    → deleted
✅ Unused images         → deleted
✅ Unused networks       → deleted
✅ Build cache           → deleted

🛡️ Running containers   → completely safe
🛡️ Images in use        → completely safe
```

> ⚠️ The only truly dangerous version is `docker system prune -a --volumes` — that removes pretty much everything including volumes. Always double check before running that one!

---

### Question 7 — Answer: B) docker run creates a new container. docker start restarts an existing one

**Explanation:**

```
docker run   → CREATE + START a brand new container from an image
docker start → START an already existing but stopped container
```

> 🚗 **Analogy:** `docker run` is buying and starting a **brand new car**. `docker start` is starting a car **you already own** that was parked!

---

### Question 8 — Answer: A) Change RUN to `pip install flask requests` and change EXPOSE to 8000

**Explanation:**

Here's exactly what the updated Dockerfile looks like:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install flask requests   # ← added requests here
EXPOSE 8000                      # ← changed from 5002 to 8000
CMD ["python", "app.py"]
```

> ⚠️ **Important caveat:** Changing `EXPOSE` in the Dockerfile alone isn't enough to change the port! You'd also need to update `app.py` to run on port `8000` and update your `-p` flag when running the container. `EXPOSE` is really just a label/documentation — the actual port is set inside your app!

---

## 💡 Key Takeaways

- 🔌 **Port mapping** — LEFT is your laptop (what you type in browser), RIGHT is the container (where your app listens). They don't have to match!
- 🥞 **Layer caching** — when a layer changes, everything AFTER it rebuilds too. Put rarely changing things at the TOP
- 🗑️ **Containers vs Images** — deleting a container never deletes the image. They are completely separate!
- 🚀 **Scaling** — each container needs a unique name AND a unique left side port
- 👻 **Ephemeral** — changes inside a running container are lost when it's deleted. Use Docker Volumes to persist data
- 🧹 **docker system prune** — only removes unused/stopped things. Running containers are always safe
- 🆕 **docker run vs docker start** — run creates a brand new container, start restarts an existing stopped one
- 📄 **EXPOSE** — is just a label in the Dockerfile. The real port is set inside your app code!

---

*Next up → [03 - Dockerfile](./03-dockerfile.md)* 🚀