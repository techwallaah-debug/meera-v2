#!/bin/bash
# Push local Meera project to GitHub (existing or new repo)
# Run from project root: ./scripts/push-to-github.sh
# You will be prompted for GitHub username and Personal Access Token.

set -e
cd "$(dirname "$0")/.."

echo "→ Current remote:"
git remote -v
echo ""

echo "→ Fetching from origin..."
if git fetch origin 2>/dev/null; then
  echo "→ Pulling and merging (allow unrelated histories)..."
  git pull origin main --allow-unrelated-histories --no-edit 2>/dev/null || true
fi

echo "→ Pushing to origin main..."
if git push -u origin main; then
  echo "✅ Done. Project is on GitHub."
else
  echo ""
  echo "⚠️  Push failed. Try:"
  echo "   1. Use a Personal Access Token as password (not GitHub password)"
  echo "   2. Or create a NEW repo and run:"
  echo "      git remote remove origin"
  echo "      git remote add origin https://github.com/YOUR_USERNAME/NEW_REPO.git"
  echo "      git push -u origin main"
  echo ""
  echo "   Full guide: PUSH_OR_NEW_REPO.md"
  exit 1
fi
