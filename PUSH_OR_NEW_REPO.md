# Push Meera to GitHub – Or Create a New Repo

Your project is **fully stored locally** and committed. Follow one path below.

---

## Option 1: Push to existing repo (techwallaah-debug/Meera)

Run this **in your terminal** (you’ll be prompted for GitHub username and token):

```bash
cd /Users/sangmeshwargurushete/Cursor/Meera

# Merge remote into local (if any), then push
git fetch origin
git pull origin main --allow-unrelated-histories --no-edit
git push -u origin main
```

- **Username:** `techwallaah-debug`
- **Password:** your GitHub **Personal Access Token** (not your GitHub password)

If you get **“rejected – non-fast-forward”** and you’re fine **replacing** what’s on GitHub with your local project:

```bash
git push origin main --force
```

---

## Option 2: Create a new repo on GitHub and push there

Use this if the existing repo keeps failing (auth, conflicts, etc.) or you want a fresh repo.

### Step 1: Create new repo on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** e.g. `Meera` or `Meera-v2`
3. **Description (optional):** `AI-Powered Social Commerce Platform`
4. Choose **Public**
5. **Do not** add README, .gitignore, or license (your project already has them)
6. Click **Create repository**

### Step 2: Add the new repo as remote and push

In your terminal, from the **Meera project folder**:

```bash
cd /Users/sangmeshwargurushete/Cursor/Meera

# Remove old remote (optional – only if you're switching to a new repo)
git remote remove origin

# Add the NEW repo as origin (replace YOUR_USERNAME and NEW_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/NEW_REPO_NAME.git

# Push your local project to the new repo
git push -u origin main
```

**Example:** New repo `Meera-v2` under `techwallaah-debug`:

```bash
git remote remove origin
git remote add origin https://github.com/techwallaah-debug/Meera-v2.git
git push -u origin main
```

When prompted:

- **Username:** your GitHub username  
- **Password:** your **Personal Access Token**

### Step 3: Verify

Open **https://github.com/YOUR_USERNAME/NEW_REPO_NAME** – you should see all your project files.

---

## If you keep both remotes

If you want to keep the old repo and also push to a new one:

```bash
# Keep origin as existing repo
git remote add newrepo https://github.com/YOUR_USERNAME/NEW_REPO_NAME.git

# Push to the new repo
git push -u newrepo main
```

---

## GitHub Personal Access Token

1. **https://github.com/settings/tokens**
2. **Generate new token (classic)**
3. Name it (e.g. “Meera push”), set expiry, enable **repo**
4. Generate → **copy the token once** and use it as the password when Git asks

Never commit or share the token.

---

## Quick reference

| Goal                         | Command |
|-----------------------------|--------|
| Push to existing Meera repo | `git push -u origin main` (after pull if needed) |
| Overwrite existing repo     | `git push origin main --force` |
| Use a new repo              | Remove/add `origin`, then `git push -u origin main` |

All project files are stored locally in the Meera folder; pushing just uploads them to GitHub.
