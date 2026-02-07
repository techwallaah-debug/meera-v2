#!/bin/bash
# Switch to a NEW GitHub repo and push (use if existing repo doesn't work)
# Run: ./scripts/setup-new-repo.sh https://github.com/YOUR_USERNAME/NEW_REPO.git
# Or run without args and paste the URL when prompted.

set -e
cd "$(dirname "$0")/.."

if [ -n "$1" ]; then
  NEW_REPO_URL="$1"
else
  echo "Enter the NEW repo URL (e.g. https://github.com/techwallaah-debug/Meera-v2.git):"
  read -r NEW_REPO_URL
fi

if [ -z "$NEW_REPO_URL" ]; then
  echo "No URL provided. Exiting."
  exit 1
fi

echo "→ Removing old origin..."
git remote remove origin 2>/dev/null || true

echo "→ Adding new origin: $NEW_REPO_URL"
git remote add origin "$NEW_REPO_URL"

echo "→ Pushing to origin main..."
git push -u origin main

echo "✅ Done. Your project is now on the new repo."
