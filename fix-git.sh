#!/bin/bash
# Script to remove database files from git tracking and add only tracked files

cd /workspaces/Data-Gov

echo "Removing docker volumes from git index..."
# Remove the entire docker-volume directory from git index
git rm -r --cached docker-setup/docker-volume 2>/dev/null || echo "docker-volume not in git index"

echo "Removing openmetadata-config from git index..."
# Remove openmetadata-config from git index if it exists
git rm -r --cached docker-setup/openmetadata-config 2>/dev/null || echo "openmetadata-config not in git index"

echo "Adding files to git (this will respect .gitignore and skip permission-denied files)..."
# Add files individually to avoid permission errors
git add .gitignore 2>/dev/null || true
git add README.md 2>/dev/null || true
git add LICENSE 2>/dev/null || true
git add fix-git.sh 2>/dev/null || true
git add docker-setup/*.yml 2>/dev/null || true
git add docker-setup/.gitignore 2>/dev/null || true
git add docker-setup/dags/ 2>/dev/null || true
git add docker-setup/plugins/ 2>/dev/null || true
git add docker-setup/data/ 2>/dev/null || true
git add docker-setup/requirements.txt 2>/dev/null || true
git add database/ 2>/dev/null || true
git add scripts/ 2>/dev/null || true

echo ""
echo "Done! Database files are excluded from git."
echo "Run 'git status' to see what will be committed."
