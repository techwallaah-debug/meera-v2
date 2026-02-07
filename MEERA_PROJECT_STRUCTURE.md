# Meera Project – Where Everything Is Stored

All project files are stored in **this folder** (the Meera project root).

---

## Project root = Meera folder

When you clone the repo or open the project, **this directory** is the Meera folder. Everything below is part of the project.

```
Meera/                          ← You are here (project root)
├── backend/                    # All backend services
│   ├── services/               # user, content, product, order, search, etc.
│   └── shared/                 # auth, database, cache, utils
├── frontend/
│   ├── mobile/                 # React Native app
│   └── web/                    # Next.js dashboard
├── infrastructure/             # Railway, Render, Hostinger, Docker, K8s
├── scripts/                   # start-local, sync-to-github, deploy, etc.
├── tests/                      # pytest unit and integration tests
├── .env.example                # Environment template
├── docker-compose.yml          # Local dev stack
├── Dockerfile                  # Railway/production build
├── railway.json                # Railway config
├── README.md                   # Main readme
└── ...                         # Other config and docs
```

---

## What is stored where

| Folder / file        | Contents                                      |
|----------------------|-----------------------------------------------|
| **backend/**        | FastAPI services, shared auth/DB/cache        |
| **frontend/mobile/** | React Native app (screens, store, api)        |
| **frontend/web/**   | Next.js app (dashboard, components)           |
| **infrastructure/** | Deployment configs (Railway, Render, etc.)    |
| **scripts/**        | Run scripts (local, deploy, sync-to-github)   |
| **tests/**          | Pytest tests                                  |
| **Root**            | Dockerfile, railway.json, docker-compose, docs |

---

## Nested `Meera/` folder

If you see a subfolder named **Meera/** inside this project, it is a clone of the same repo (e.g. from testing) and is **ignored by Git** (see `.gitignore`). The real project is **this** folder; you can delete the inner `Meera/` if you don’t need it.

---

**Summary:** All project files are in this Meera folder (the repo root). There is no other “Meera” folder that holds the real project.
