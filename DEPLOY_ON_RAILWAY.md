# Deploy Meera on Railway

**We're going with Railway.** This is the single guide for deploying the Meera User Service.

---

## What’s ready

- **Dockerfile** (root) – builds and runs User Service
- **railway.json** (root) – Railway build and deploy config
- **.dockerignore** (root) – faster builds
- **User Service** – uses `PORT` and `ENVIRONMENT` from env (Railway sets `PORT`)

---

## Deploy in ~10 minutes

### 1. Push to GitHub

```bash
cd /path/to/Meera
git add . && git commit -m "Ready for Railway" && git push origin main
```

If you need to set up the remote or fix push issues, see **`PUSH_OR_NEW_REPO.md`**.

### 2. Sign up / log in on Railway

1. Go to **https://railway.app**
2. **Login** → **Login with GitHub**
3. Authorize Railway for your GitHub account

### 3. Create a project from GitHub

1. **New Project**
2. **Deploy from GitHub repo**
3. Select the **Meera** repository
4. Railway will detect the **Dockerfile** and **railway.json** and start building

### 4. Add MySQL

1. In the project, click **New**
2. **Database** → **Add MySQL** (or **Add Plugin** → MySQL)
3. Wait for the MySQL service to be ready
4. Open the MySQL service → **Variables** or **Connect** and copy the **connection URL**

### 5. Set environment variables (User Service)

1. Open your **User Service** (the one built from the repo)
2. Go to **Variables**
3. Add (or link from MySQL):

| Variable | Value |
|---------|--------|
| `DATABASE_URL` | MySQL connection URL from step 4 |
| `JWT_SECRET_KEY` | Long random secret (e.g. from a password generator) |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `ENVIRONMENT` | `production` |

### 6. Get a public URL

1. Open your **User Service**
2. **Settings** → **Networking** (or **Deployments** → **Settings**)
3. **Generate Domain** (or **Add domain**)
4. Copy the URL (e.g. `https://meera-production.up.railway.app`)

### 7. Test

- **Health:** `https://YOUR-URL/health` → `{"status":"healthy"}`
- **Docs:** `https://YOUR-URL/docs` → Swagger UI

---

## Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created from Meera repo
- [ ] MySQL added and `DATABASE_URL` set on User Service
- [ ] `JWT_SECRET_KEY` and `ENVIRONMENT=production` set
- [ ] Domain generated for User Service
- [ ] `/health` and `/docs` work on the generated URL

---

## More detail

- **Step-by-step:** **`infrastructure/railway/README.md`**
- **Checklist:** **`RAILWAY_DEPLOYMENT_CHECKLIST.md`**

---

## Troubleshooting

If the build or app fails, see **[\`DEPLOY_TROUBLESHOOTING.md\`](DEPLOY_TROUBLESHOOTING.md)** for common errors and fixes.

**Quick fixes:**
- **Build timeout / out of memory** – The Dockerfile now uses **minimal** `requirements-user-service.txt` (no torch/opencv). Redeploy.
- **ModuleNotFoundError: shared** – Dockerfile sets `PYTHONPATH=/app/backend`. Redeploy.
- **App crash / 503** – In Railway **Variables**, set `DATABASE_URL` (MySQL URL) and `JWT_SECRET_KEY`. Check **Logs** for the exact error.

You’re set for Railway.
