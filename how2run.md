# 🐳 how2run.md — Run This Django Project Like a Pro (and Have Fun Doing It!)

So you’ve just cloned this project, and now you want to see it in action.
Good news: this repo is containerized with **Docker** and set up with **VS Code Devcontainers**.
That means you don’t need to fight with Python versions, virtualenvs, or dependency chaos — everything is already wrapped up neatly inside a container. 🎁

Let’s get you running step-by-step.

---

## 🚀 Prerequisites

Before touching anything, make sure you have these installed on your machine:

1. **Docker Desktop** (or Docker Engine) → [Install Docker](https://docs.docker.com/get-docker/)

   * Check with:

     ```bash
     docker --version
     ```
2. **Visual Studio Code** → [Install VS Code](https://code.visualstudio.com/)
3. **Dev Containers Extension** in VS Code → [Install here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

---

## 🛠️ Open Project in Devcontainer

1. Clone this repo (if you haven’t yet)
2. Open VS Code in the repo folder
3. When VS Code detects the `.devcontainer/` config, it should ask:
   👉 “**Reopen in Container**”
   Click it! (Or press **F1** → search `Dev Containers: Reopen in Container`).

VS Code will now:

* Build the Docker image
* Spin up the container
* Install dependencies
* Drop you into a fully configured shell environment 🚀

---

## ▶️ Running the Django Application

Inside the container terminal, run:

```bash
python manage.py runserver 0.0.0.0:8000
```

Why `0.0.0.0`?
Because we want Django to accept requests from outside the container (your host machine).
Without it, the server would only talk to itself inside the container — and that’s kinda lonely.

---

## 🌍 Access the App

Open your browser and head to:

👉 [http://localhost:8000](http://localhost:8000)

Boom 💥 Your Django project should now be live!

---

## 🧹 Resetting the Database (When Things Get Messy)

Sometimes migrations go sideways, a table breaks, or the schema is just beyond saving.
Don’t panic 🚨 — we’ve got a **reset script** for that!

Inside the `utils/` folder, there’s a shell script that:

* Wipes the database 🗑️
* Re-applies the schema and migrations from scratch 🔄
* Gives you a clean slate to keep working 🎯

Run it from inside the container like this:

```bash
./utils/reset.sh
```

*(Make sure it’s executable — if not, run `chmod +x ./utils/reset.sh` once.)*

---

## 👑 Using the Django Admin

Django comes with a built-in **admin panel** that makes it super easy to manage users, events, and more. Here’s how to get in:

1. **Create an Admin User**
   Inside the container terminal, run:

   ```bash
   python manage.py createsuperuser
   ```

   * Enter a username, email, and password.
   * Congratulations, you are now a Django overlord 👑.

2. **Access the Admin Site**
   With the server running, open:
   👉 [http://localhost:8000/admin](http://localhost:8000/admin)

3. **Log In**
   Use the superuser credentials you just created.
   If you see the Django admin dashboard — you’ve officially leveled up ⚡.

4. **Admin Superpowers**
   From here, you can:

   * **Manage users** → add, edit, or deactivate them.
   * **Create and edit events** (if the project has an `Event` model registered).
   * Explore any other models registered with the admin.

Pro tip: If you want models (like `Event`) to appear here, make sure they’re registered in `admin.py`.

---