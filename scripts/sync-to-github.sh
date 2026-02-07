#!/bin/bash
# Sync local Meera project to GitHub (techwallaah-debug/Meera)
# Run from project root: ./scripts/sync-to-github.sh

set -e
cd "$(dirname "$0")/.."

REMOTE="https://github.com/techwallaah-debug/Meera.git"

# Ensure remote is set
if ! git remote get-url origin &>/dev/null; then
  echo "→ Adding remote origin..."
  git remote add origin "$REMOTE"
fi

echo "→ Fetching from origin..."
git fetch origin

echo "→ Merging remote into local (allow unrelated histories)..."
if git pull origin main --allow-unrelated-histories --no-edit; then
  echo "→ Merge OK. Pushing to origin main..."
  git push -u origin main
else
  echo ""
  echo "⚠️  Merge had conflicts or failed. To overwrite GitHub with your local project, run:"
  echo "   git push origin main --force"
  echo ""
  exit 1
fi

echo "✅ Done. Your local project is now on GitHub."
