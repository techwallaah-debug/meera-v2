# Push this project to GitHub

Your repo is initialized and the **initial commit is done**. Follow these steps to push to GitHub.

---

## 1. Create a new repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** e.g. `Meera` (or `social-commerce-platform`)
3. **Description (optional):** e.g. `AI-Powered Social Commerce Platform`
4. Choose **Public**
5. **Do not** add a README, .gitignore, or license (this project already has them)
6. Click **Create repository**

---

## 2. Add the remote and push

In your terminal, from the project root (`Meera`):

```bash
cd /Users/sangmeshwargurushete/Cursor/Meera

# Add your GitHub repo as remote (replace YOUR_USERNAME and YOUR_REPO with yours)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push the main branch
git push -u origin main
```

**Example:** If your GitHub username is `johndoe` and the repo is `Meera`:

```bash
git remote add origin https://github.com/johndoe/Meera.git
git push -u origin main
```

If you use **SSH** instead of HTTPS:

```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## 3. Verify

- Open **https://github.com/YOUR_USERNAME/YOUR_REPO** in your browser.
- You should see all project files and the initial commit.

---

## 4. Deploy to Railway (optional)

After the repo is on GitHub:

1. Go to **https://railway.app** → **New Project** → **Deploy from GitHub repo**
2. Select this repository
3. Follow **infrastructure/railway/README.md** (add MySQL, set variables, generate domain)

---

## Troubleshooting

- **"remote origin already exists"**  
  Use: `git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git`  
  Then: `git push -u origin main`

- **"rejected – non-fast-forward" / "your branch is behind"**  
  The repo on GitHub has commits (e.g. initial README) that your local branch doesn’t have. From your **project folder** (the one with all your code), run:

  ```bash
  cd /path/to/your/Meera   # your workspace, NOT the clone

  git fetch origin
  git pull origin main --allow-unrelated-histories
  # Resolve conflicts if asked (e.g. keep your README), then:
  git push origin main
  ```

  If you want to overwrite GitHub with your local code (and don’t care about what’s on GitHub):

  ```bash
  git push origin main --force
  ```

  Only use `--force` if you’re sure; it replaces the remote history.

- **Authentication failed**  
  Use a **Personal Access Token** (GitHub → Settings → Developer settings → Personal access tokens) as password when pushing over HTTPS, or set up SSH keys.

- **Branch name**  
  If GitHub created the repo with default branch `master`, either:
  - Rename locally: `git branch -M main` then `git push -u origin main`, or
  - Push to `master`: `git push -u origin master`
