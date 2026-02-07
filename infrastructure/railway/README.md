# 🚂 Deploy to Railway.app

## Deploy your User Service in ~10 minutes

This guide walks you through deploying the **User Service** (and optionally more services) to Railway using the config already in this repo.

---

## ✅ What’s already set up

- **`Dockerfile`** (project root) – builds and runs the User Service
- **`railway.json`** (project root) – tells Railway how to build and start the app
- **User Service** – reads **`PORT`** from the environment (Railway sets this)

---

## 🚀 Step-by-step deploy

### 1. Push your code to GitHub

```bash
git add .
git commit -m "Add Railway deployment config"
git push origin main
```

### 2. Sign up / log in on Railway

1. Open **https://railway.app**
2. Click **“Login”** → **“Login with GitHub”**
3. Authorize Railway to access your GitHub account

### 3. Create a new project from GitHub

1. In the Railway dashboard, click **“New Project”**.
2. Choose **“Deploy from GitHub repo”**.
3. Select the **Meera** repository (or the repo that contains this code).
4. Railway will detect the **Dockerfile** and **railway.json** and start a build.

### 4. Add a database (MySQL)

The app expects a **MySQL** database and a **`DATABASE_URL`** env var.

1. In your project, click **“New”**.
2. Click **“Database”** → **“Add MySQL”** (or **“Add Plugin”** and pick MySQL if shown).
3. Wait until the MySQL service is provisioned.
4. Click the MySQL service → **“Variables”** (or **“Connect”**) and copy the **connection URL** (e.g. `mysql://...` or `mysql+pymysql://...`).
5. Go back to your **User Service** (the one built from the repo).
6. Open **“Variables”** and add:
   - **`DATABASE_URL`** = the MySQL connection URL you copied.

If Railway only offers **PostgreSQL** and no MySQL:

- You can add **PostgreSQL** and set **`DATABASE_URL`** to the Postgres URL, but you would then need to change the app to use PostgreSQL (different driver and possibly schema). For the least friction, use **MySQL** if available.

### 5. Set required environment variables

In the **User Service** → **“Variables”**, ensure at least:

| Variable | Example / note |
|----------|-----------------|
| `DATABASE_URL` | From MySQL plugin (see above) |
| `JWT_SECRET_KEY` | e.g. `your-super-secret-key-change-in-production` |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `ENVIRONMENT` | `production` (so reload is disabled) |

Optional (for full platform later):

- `REDIS_URL` – if you add a Redis plugin
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET_NAME` – for S3/media
- `OPENAI_API_KEY`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `SENDGRID_API_KEY`, `TWILIO_*` – for other features

### 6. Get a public URL

1. Open your **User Service**.
2. Go to **“Settings”** → **“Networking”** (or **“Deployments”** → **“Settings”**).
3. Click **“Generate Domain”** (or **“Add domain”**).
4. Copy the URL (e.g. `https://your-app.up.railway.app`).

### 7. Redeploy (if you added variables after first deploy)

- **“Deployments”** → open the latest deployment → **“Redeploy”**,  
  or push a new commit; Railway will redeploy automatically.

### 8. Test the API

```bash
# Replace with your Railway URL
curl https://YOUR-APP.up.railway.app/health
```

Expected: `{"status":"healthy"}`.

- **API docs:** `https://YOUR-APP.up.railway.app/docs`
- **OpenAPI JSON:** `https://YOUR-APP.up.railway.app/openapi.json`

---

## 📦 Deploying more services (Content, Product, Order, etc.)

You can run **one service per Railway project** (or per “service” inside one project), each from the same repo with a different start command.

1. **New Project** (or **New Service** in same project) → **Deploy from GitHub repo** → same repo.
2. In **Settings** (or **Build**):
   - Use the **same Dockerfile** (project root).
   - Override **Start Command** for that service, e.g.:
     - Content: `python backend/services/content-service/src/main.py`
     - Product: `python backend/services/product-service/src/main.py`
     - Order: `python backend/services/order-service/src/main.py`
3. Each service needs its own **Variables** (e.g. `DATABASE_URL`, `JWT_SECRET_KEY`, and any service-specific keys).
4. **Generate Domain** for each service so you get URLs like:
   - `https://user-svc.up.railway.app`
   - `https://content-svc.up.railway.app`
   - etc.

Then point your mobile app or web app at these base URLs per service.

---

## 🔧 Custom domain

1. User Service → **Settings** → **Domains** (or **Networking**).
2. **Custom Domain** → e.g. `api.yourdomain.com`.
3. Add the CNAME (or A) record Railway shows in your DNS provider.
4. Railway will issue and attach SSL for that domain.

---

## 📊 Logs and monitoring

- **Logs:** Open the service → **“Deployments”** → select a deployment → **“View Logs”**.
- **Metrics:** Railway shows CPU/memory and request metrics in the dashboard.
- **Restarts:** Configured in **railway.json** (`restartPolicyType`, `restartPolicyMaxRetries`).

---

## 💰 Free tier

- **500 hours/month** free usage.
- **$5 credit** per month on free tier.
- MySQL/Redis and other plugins may have their own limits; check Railway’s current pricing.

---

## ✅ Checklist before you start

- [ ] Code pushed to GitHub (including `Dockerfile`, `railway.json`).
- [ ] Railway account linked to GitHub.
- [ ] MySQL database added and `DATABASE_URL` set on the User Service.
- [ ] `JWT_SECRET_KEY` and `ENVIRONMENT=production` set.
- [ ] Public domain generated for the User Service.
- [ ] `/health` and `/docs` tested with your Railway URL.

For more options (Render, Fly.io, local + ngrok), see **`START_HERE.md`** and **`FREE_DEPLOYMENT_GUIDE.md`** in the project root.
