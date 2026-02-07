# Railway Deployment – Checklist

## Is everything ready?

| Item | Status |
|------|--------|
| **Dockerfile** (root) | ✅ Builds User Service, uses Python 3.11, copies `backend/` |
| **railway.json** (root) | ✅ Builder: DOCKERFILE, start: user-service, restart on failure |
| **User Service PORT** | ✅ Reads `PORT` from env (Railway sets this) |
| **User Service ENVIRONMENT** | ✅ Uses `ENVIRONMENT=production` to disable reload |
| **.dockerignore** (root) | ✅ Speeds build (excludes frontend, .git, tests, etc.) |
| **shared imports** | ✅ User service finds `shared` via `sys.path` |
| **DATABASE_URL** | ✅ Read from env (set in Railway Variables) |
| **/health** | ✅ Exists for Railway health checks |

---

## Required in Railway dashboard

1. **Deploy from GitHub** – Connect repo `techwallaah-debug/Meera` (or your repo).
2. **Add MySQL** – Database → Add MySQL; copy connection URL.
3. **Variables** (User Service):
   - `DATABASE_URL` = MySQL URL from step 2
   - `JWT_SECRET_KEY` = long random secret
   - `JWT_ALGORITHM` = `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
   - `ENVIRONMENT` = `production`
4. **Generate domain** – Settings → Networking → Generate Domain.

---

## Optional improvements

- **Lighter build:** `backend/requirements.txt` includes torch, opencv, etc. If build is slow, consider a minimal `backend/requirements-minimal.txt` for User Service and use it in the Dockerfile.
- **Health check:** Railway can use `GET /health`; no extra config needed if the path exists (it does).

---

## Quick deploy steps

1. Push project to GitHub (see `PUSH_OR_NEW_REPO.md` if needed).
2. Railway → New Project → Deploy from GitHub repo → select Meera.
3. Add MySQL, set Variables, Generate Domain.
4. Open the generated URL → `/health` and `/docs` should work.

Full guide: **`infrastructure/railway/README.md`**
