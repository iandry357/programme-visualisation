# Concert Viewer - Phase 1 Setup
# Exécuter depuis la racine du repo git cloné

Write-Host "🎯 Setup Phase 1 : Structure Git & Dossiers" -ForegroundColor Cyan

# Créer structure backend
Write-Host "`n📁 Création structure backend..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "backend"
New-Item -ItemType Directory -Force -Path "backend/app"
New-Item -ItemType Directory -Force -Path "backend/app/api"
New-Item -ItemType Directory -Force -Path "backend/scripts"
New-Item -ItemType Directory -Force -Path "backend/data"
New-Item -ItemType Directory -Force -Path "backend/data/concert_photos"

# Créer structure frontend
Write-Host "📁 Création structure frontend..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "frontend"

# Créer .gitignore racine
Write-Host "`n📝 Création .gitignore racine..." -ForegroundColor Yellow
@"
# Environment
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

# Créer .gitignore backend
Write-Host "📝 Création backend/.gitignore..." -ForegroundColor Yellow
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Data & SQL
data/
init-data.sql
*.sql.bak

# Docker volumes
mariadb_data/

# Logs
*.log
"@ | Out-File -FilePath "backend/.gitignore" -Encoding UTF8

# Créer .gitignore frontend
Write-Host "📝 Création frontend/.gitignore..." -ForegroundColor Yellow
@"
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Next.js
.next/
out/
build/
dist/

# Production
*.tsbuildinfo
next-env.d.ts

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env*.local
"@ | Out-File -FilePath "frontend/.gitignore" -Encoding UTF8

# Créer README.md
Write-Host "📝 Création README.md..." -ForegroundColor Yellow
@"
# Concert Viewer

Plateforme de visualisation de programmes de concert.

## Structure

- **backend/** - API FastAPI + MariaDB (Docker)
- **frontend/** - Interface Next.js (Railway Git)

## Installation

Voir documentation dans chaque dossier.

## Stack

- Backend: FastAPI + MariaDB + Docker
- Frontend: Next.js + TypeScript + Tailwind CSS
- Déploiement: Railway
"@ | Out-File -FilePath "README.md" -Encoding UTF8

# Créer fichiers vides pour éviter erreurs
Write-Host "`n📄 Création fichiers placeholder..." -ForegroundColor Yellow
New-Item -ItemType File -Force -Path "backend/requirements.txt" | Out-Null
New-Item -ItemType File -Force -Path "backend/data/.gitkeep" | Out-Null
New-Item -ItemType File -Force -Path "backend/data/concert_photos/.gitkeep" | Out-Null

Write-Host "`n✅ Phase 1 terminée !" -ForegroundColor Green
Write-Host "`n📋 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Placer tes PNG dans backend/data/concert_photos/" -ForegroundColor White
Write-Host "  2. Placer ton PDF dans backend/data/concert.pdf" -ForegroundColor White
Write-Host "  3. git add . && git commit -m 'Phase 1: Structure initiale'" -ForegroundColor White
Write-Host "  4. Passer à Phase 2 (Docker)" -ForegroundColor White

# Afficher structure créée
Write-Host "`n🌳 Structure créée:" -ForegroundColor Cyan
tree /F /A