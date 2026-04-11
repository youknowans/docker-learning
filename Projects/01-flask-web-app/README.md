# 🐳 Hello World — Flask App in Docker

> A simple beginner Docker project that containerises a Python Flask web application. Built as part of my DevOps bootcamp journey to learn the basics of Docker images, containers and Dockerfiles.

---

## 📌 What This Project Does

Runs a simple **"Hello, World!"** web page using:
- **Python Flask** — a lightweight web framework
- **Docker** — to package and run the app in a container

Once running, visiting `http://localhost:5002` in your browser will display:

```
Hello, World!
```

---

## 🛠️ Technologies Used

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

---

## 📁 Project Structure

```
hello-flask/
│
├── app.py          ← The Flask web application
├── Dockerfile      ← Instructions for building the Docker image
└── README.md       ← You are here!
```

---

## 🚀 How to Run This Project

### Prerequisites
Make sure you have Docker installed on your machine:
```bash
docker --version
```

### Step 1 — Clone the repo
```bash
git clone https://github.com/youknowans/hello-flask.git
cd hello-flask
```

### Step 2 — Build the Docker image
```bash
docker build -t hello-flask .
```

> This reads the Dockerfile and packages the app into an image called `hello-flask`

### Step 3 — Run the container
```bash
docker run -d -p 5002:5002 hello-flask
```

> This starts the container in the background and maps port 5002 on your machine to port 5002 inside the container

### Step 4 — View the app
Open your browser and visit:
```
http://localhost:5002
```

You should see **Hello, World!** displayed in the browser ✅

---

## 🔧 Useful Docker Commands

| Command | What it does |
|---------|-------------|
| `docker build -t hello-flask .` | Build the image |
| `docker run -d -p 5002:5002 hello-flask` | Run the container |
| `docker ps` | Check the container is running |
| `docker logs <container-id>` | View container logs |
| `docker stop <container-id>` | Stop the container |
| `docker rm <container-id>` | Delete the container |

---

## 🧠 What I Learned

- How to write a basic **Dockerfile** from scratch
- The difference between `RUN` (runs during build) and `CMD` (runs when container starts)
- How **port mapping** works with the `-p` flag
- How to build a Docker image with `docker build`
- How to run a container in detached mode with `-d`
- How Docker packages an app with all its dependencies so it runs consistently anywhere

---

## 📚 Key Dockerfile Instructions Explained

| Instruction | What it does |
|-------------|-------------|
| `FROM` | Sets the base image to start from. `python:3.8-slim` gives us a lightweight Python environment |
| `WORKDIR` | Creates and sets the working directory inside the container |
| `COPY` | Copies files from your local machine into the container |
| `RUN` | Executes a command during the **build** process — used to install Flask |
| `EXPOSE` | Documents which port the app listens on inside the container |
| `CMD` | The command that runs when the **container starts** — launches the Flask app |

---

*Part of my Docker Learning Journey — see the full repo [here](https://github.com/youknowans/docker-learning)* 🐳
