# Render – meera-user-service: Variables to Enter

When creating the **meera-user-service** web service on Render, set these variables:

---

## 1. DATABASE_URL

**What it is:** Connection URL for your MySQL database.

**Render does not offer MySQL** (only PostgreSQL). Use one of these:

### Option A: PlanetScale (free MySQL)

1. Sign up at **https://planetscale.com** (free tier).
2. Create a database → get the connection URL.
3. It looks like: `mysql://username:password@host/database?sslaccept=strict`
4. **Change `mysql://` to `mysql+pymysql://`** so Python can connect:
   - **Value:** `mysql+pymysql://username:password@host/database?sslaccept=strict`

### Option B: Railway MySQL

1. In **Railway**, create a project → add **MySQL** (Database).
2. Open the MySQL service → **Variables** or **Connect**.
3. Copy the **connection URL** (e.g. `mysql://root:xxx@host:3306/railway`).
4. **Change `mysql://` to `mysql+pymysql://`**:
   - **Value:** `mysql+pymysql://root:password@host:3306/railway`

### Option C: Any other MySQL host

Use the URL in this form:

- **Value:** `mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE`

Replace `USER`, `PASSWORD`, `HOST`, `DATABASE` with your MySQL details.

---

## 2. JWT_SECRET_KEY

**What it is:** Secret key used to sign JWT tokens. Must be long and random.

**How to get a value:**

1. **Option A – Generate online:** Use a generator like https://randomkeygen.com (e.g. “CodeIgniter Encryption Keys”) and copy one 32+ character string.
2. **Option B – Terminal:**
   ```bash
   openssl rand -hex 32
   ```
   Copy the output (e.g. `a1b2c3d4e5f6...`).
3. **Option C – Any long random string:** e.g. 32+ random letters/numbers.

**Value example:**  
`your-super-secret-key-at-least-32-chars-long-change-this`

**Important:** Do not share this value or commit it to Git. Use it only in Render’s Environment variables.

---

## Summary for Render “Environment” / “Variables”

| Key             | Value |
|-----------------|--------|
| **DATABASE_URL** | Your MySQL URL with `mysql+pymysql://` (from PlanetScale, Railway, or your MySQL host). |
| **JWT_SECRET_KEY** | A long random string (e.g. from `openssl rand -hex 32` or a password generator). |

Optional but recommended:

| Key             | Value |
|-----------------|--------|
| **JWT_ALGORITHM** | `HS256` |
| **ACCESS_TOKEN_EXPIRE_MINUTES** | `30` |
| **ENVIRONMENT** | `production` |

Save the variables, then deploy. The service will use these when it starts.
