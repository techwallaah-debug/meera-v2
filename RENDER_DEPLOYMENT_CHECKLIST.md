# Render Deployment – Checklist

## Ready for Render

| Item | Status |
|------|--------|
| **render.yaml** (root) | ✅ Blueprint for meera-user-service |
| **User Service PORT** | ✅ Reads `PORT` from env (Render sets this) |
| **User Service ENVIRONMENT** | ✅ Uses `ENVIRONMENT=production` (no reload) |
| **/health** | ✅ Used for health checks |
| **Build command** | ✅ `pip install -r backend/requirements.txt` |
| **Start command** | ✅ `python backend/services/user-service/src/main.py` |

---

## You need to set

1. **Push to GitHub** (if not already) – see `PUSH_OR_NEW_REPO.md`
2. **Database** – App uses **MySQL**. Render’s free DB is PostgreSQL. Use external MySQL:
   - [PlanetScale](https://planetscale.com) (free tier), or
   - [Railway](https://railway.app) MySQL
   Copy the connection URL (e.g. `mysql+pymysql://...`)
3. **On Render** – In **meera-user-service** → **Environment**:
   - `DATABASE_URL` = your MySQL URL
   - `JWT_SECRET_KEY` = long random secret

---

## Deploy steps

1. Go to **https://render.com** → Login with GitHub
2. **New +** → **Blueprint** → Connect **Meera** repo
3. Render creates **meera-user-service** from `render.yaml`
4. Add **Environment** variables: `DATABASE_URL`, `JWT_SECRET_KEY`
5. Deploy; then open the service URL → `/health` and `/docs`

Full guide: **`infrastructure/render/README.md`**
