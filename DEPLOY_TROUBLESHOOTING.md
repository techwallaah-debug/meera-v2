# Railway Deployment – Troubleshooting

Common errors and fixes when deploying Meera on Railway.

---

## 1. Build fails / timeout / out of memory

**Symptom:** Build runs a long time, then fails or times out.

**Cause:** Full `backend/requirements.txt` includes **torch**, **opencv-python**, **sentence-transformers**, which are very large and often break Railway builds.

**Fix (already applied):** The **Dockerfile** now uses **`requirements-user-service.txt`** (minimal deps: FastAPI, SQLAlchemy, PyMySQL, JWT, etc.). No torch/opencv.

- If you changed the Dockerfile back to `requirements.txt`, switch to `requirements-user-service.txt` again.
- Re-deploy (push to GitHub or Redeploy in Railway).

---

## 2. ModuleNotFoundError: No module named 'shared'

**Symptom:** Logs show `ModuleNotFoundError: No module named 'shared'` (or `shared.database`, `shared.auth`).

**Cause:** Python can’t find the `shared` package (path not set).

**Fix (already applied):** The **Dockerfile** sets **`ENV PYTHONPATH=/app/backend`** so `shared` resolves to `/app/backend/shared`.

- If you use a custom Dockerfile, add: `ENV PYTHONPATH=/app/backend`
- Redeploy.

---

## 3. Application crash / 503 / "Application failed to respond"

**Symptom:** Service starts then crashes, or Railway shows 503 / "Application failed to respond".

**Possible causes and fixes:**

| Cause | What to do |
|-------|------------|
| **DATABASE_URL missing or wrong** | In Railway → User Service → **Variables**: set `DATABASE_URL` to the MySQL connection URL from your MySQL plugin (e.g. `mysql+pymysql://user:pass@host:port/db`). |
| **MySQL not reachable** | Use Railway’s **MySQL** plugin in the same project and use the **internal** connection URL Railway gives you. |
| **App not listening on PORT** | The app already reads `PORT` from the environment. Don’t hardcode the port; leave it as in the code. |
| **JWT_SECRET_KEY missing** | In **Variables**, add `JWT_SECRET_KEY` (long random string) and `ENVIRONMENT=production`. |

Check **Logs** in the Railway service for the exact error (e.g. connection refused, auth error).

---

## 4. Build fails: "requirements.txt" or pip error

**Symptom:** `pip install` fails (e.g. package not found, version conflict).

**Fix:** The Dockerfile uses **`requirements-user-service.txt`**. Ensure that file exists in the repo under `backend/requirements-user-service.txt` and that the Dockerfile line is:

```dockerfile
COPY backend/requirements-user-service.txt .
RUN pip install --no-cache-dir -r requirements-user-service.txt
```

Then push and redeploy.

---

## 5. Health check fails / service marked unhealthy

**Symptom:** Railway says the service is unhealthy or the generated URL returns 502/503.

**Checks:**

- **Logs:** In Railway → your service → **Deployments** → latest deployment → **View Logs**. Look for tracebacks or "Address already in use", "Connection refused", etc.
- **Variables:** Confirm `DATABASE_URL`, `JWT_SECRET_KEY`, and `ENVIRONMENT=production` are set.
- **URL:** Open `https://YOUR-SERVICE.up.railway.app/health` in a browser; you should see `{"status":"healthy"}`.

---

## 6. "No such file or directory" or wrong path in Docker

**Symptom:** Logs show file not found for `backend/` or `main.py`.

**Fix:** The Dockerfile assumes:

- **Build context** is the **repo root** (where `Dockerfile` and `backend/` live).
- **Working directory** in the image is `/app`.
- Copy is: `COPY backend/ ./backend/` and run is: `python backend/services/user-service/src/main.py`.

Don’t change the build context to `backend/`; keep it at repo root so `COPY backend/` works.

---

## Quick checklist

- [ ] Dockerfile uses **`requirements-user-service.txt`** (not full `requirements.txt`).
- [ ] Dockerfile has **`ENV PYTHONPATH=/app/backend`**.
- [ ] **Variables** in Railway: `DATABASE_URL`, `JWT_SECRET_KEY`, `ENVIRONMENT=production`.
- [ ] **MySQL** is added in the same Railway project and `DATABASE_URL` is the URL Railway provides.
- [ ] **Logs** checked for the exact error message.

---

## Still failing?

1. Copy the **exact error message** from Railway **Logs** (build or runtime).
2. Check which step fails: **Build** (pip/Docker) or **Deploy** (app startup/crash).
3. Share that error and step so we can target the fix (e.g. missing env var, wrong DB URL, or another dependency).
