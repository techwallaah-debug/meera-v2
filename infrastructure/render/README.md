# Deploy Meera on Render.com

Deploy the **User Service** (and optionally more services) on Render using the config in this repo.

---

## What’s already set up

- **`render.yaml`** (project root) – Blueprint for the User Service
- **User Service** – reads **`PORT`** and **`ENVIRONMENT`** from the environment (Render sets `PORT`)

---

## Option A: Deploy with Blueprint (recommended)

### 1. Push code to GitHub

```bash
cd /path/to/Meera
git add . && git commit -m "Add Render config" && git push origin main
```

### 2. Sign up / log in on Render

1. Go to **https://render.com**
2. **Login** → **Login with GitHub**
3. Authorize Render for your GitHub account

### 3. Create a Blueprint from the repo

1. In the Render dashboard, click **“New +”** → **“Blueprint”**
2. Connect the **Meera** repository (or the repo that contains this code)
3. Render will detect **`render.yaml`** and create the **meera-user-service** web service
4. Click **“Apply”** to create the service

### 4. Database (MySQL)

The app expects **MySQL** and a **`DATABASE_URL`** env var. Render’s free DB is **PostgreSQL**, so use one of:

- **External MySQL** (e.g. [PlanetScale](https://planetscale.com) free tier, or [Railway](https://railway.app) MySQL)
- Create the DB, copy the connection URL (e.g. `mysql+pymysql://user:pass@host:3306/db`)

In Render:

1. Open **meera-user-service** → **Environment**
2. Add variable: **`DATABASE_URL`** = your MySQL connection URL
3. Add variable: **`JWT_SECRET_KEY`** = a long random secret (e.g. from a password generator)

### 5. Deploy

Render will build and deploy. When it’s done:

- **URL:** e.g. `https://meera-user-service.onrender.com`
- **Health:** `https://meera-user-service.onrender.com/health`
- **Docs:** `https://meera-user-service.onrender.com/docs`

---

## Option B: Manual Web Service (no Blueprint)

### 1. New Web Service

1. **New +** → **Web Service**
2. Connect the **Meera** GitHub repo
3. Use branch **main**

### 2. Configure build and start

- **Name:** `meera-user-service`
- **Region:** Oregon (or closest)
- **Root Directory:** *(leave empty)*
- **Environment:** Python 3
- **Build Command:** `pip install -r backend/requirements.txt`
- **Start Command:** `python backend/services/user-service/src/main.py`
- **Plan:** Free

### 3. Environment variables

Add at least:

| Variable | Value |
|----------|--------|
| `DATABASE_URL` | Your MySQL connection URL (external DB) |
| `JWT_SECRET_KEY` | Long random secret |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `ENVIRONMENT` | `production` |

Render sets **`PORT`** automatically; the app uses it.

### 4. Create Web Service

Click **Create Web Service**. Render will build and deploy.

---

## Free tier notes

- **Services sleep** after ~15 minutes of no traffic
- **First request** after sleep can take ~30 seconds (cold start)
- **750 hours/month** free; enough for one small service
- **Database:** Use external MySQL (PlanetScale, Railway, etc.); Render’s free DB is PostgreSQL

---

## Custom domain

1. **meera-user-service** → **Settings** → **Custom Domains**
2. Add your domain (e.g. `api.yourdomain.com`)
3. Add the CNAME (or A) record Render shows at your DNS provider
4. Render will handle SSL

---

## Deploy more services (Content, Product, Order)

Repeat **Option B** for each service with:

- **Content:** start command `python backend/services/content-service/src/main.py`, port 8002
- **Product:** `python backend/services/product-service/src/main.py`, port 8003
- **Order:** `python backend/services/order-service/src/main.py`, port 8004

Or extend **`render.yaml`** with more `services` entries and redeploy the Blueprint.

---

## Quick checklist

- [ ] Code pushed to GitHub (including `render.yaml`)
- [ ] Render account linked to GitHub
- [ ] Blueprint created from Meera repo (or Web Service created manually)
- [ ] `DATABASE_URL` set (external MySQL)
- [ ] `JWT_SECRET_KEY` set
- [ ] Service has a public URL; `/health` and `/docs` work

Full Render docs: **https://render.com/docs**
