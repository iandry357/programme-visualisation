# 🎵 Concert Viewer

Plateforme web de visualisation de programmes de concert avec navigation interactive et téléchargement PDF.

## 🌐 Accès direct

- **Frontend (Viewer)** : https://frontend-programme-visualisation-production.up.railway.app
- **Backend (API)** : https://backend-programme-visualisation-production.up.railway.app
- **Documentation API** : https://backend-programme-visualisation-production.up.railway.app/docs

## ✨ Fonctionnalités

### Pour les spectateurs
- **Navigation intuitive** : Parcourez les pages du programme avec les flèches du clavier, boutons ou swipe mobile
- **Téléchargement PDF** : Récupérez le programme complet en un clic
- **Accès rapide via QR code** : Scannez le QR code affiché au concert pour accéder directement au programme
- **Responsive** : Interface optimisée pour mobile et desktop

### Technique
- Affichage haute qualité des pages (format PNG)
- Indicateur de progression (Page X/15)
- Chargement optimisé des images
- Analytics intégré (Google Analytics)

## 🏗️ Architecture

### Backend
- **Framework** : FastAPI (Python 3.11)
- **Base de données** : MySQL (Railway)
- **Conteneurisation** : Docker
- **API REST** : 5 endpoints pour gérer concerts, pages et fichiers

**Stack technique :**
```
FastAPI + SQLAlchemy + PyMySQL
Docker + docker-compose (développement local)
```

### Frontend
- **Framework** : Next.js 14 (App Router)
- **Language** : TypeScript
- **Styling** : Tailwind CSS
- **Déploiement** : Railway (Git integration)

**Stack technique :**
```
Next.js + React + TypeScript
Tailwind CSS
Google Analytics (GA4)
```

### Infrastructure
- **Hébergement** : Railway
- **Déploiement** :
  - Backend : Docker image depuis `backend/Dockerfile`
  - Frontend : Git integration depuis `frontend/`
- **Base de données** : MySQL managed service (Railway addon)

## 📖 Guide d'utilisation

### Accès au programme

**Option 1 : URL directe**
1. Rendez-vous sur https://frontend-programme-visualisation-production.up.railway.app
2. Le programme s'affiche automatiquement

**Option 2 : QR Code**
1. Scannez le QR code affiché au concert avec votre smartphone
2. Le programme s'ouvre directement dans votre navigateur

### Navigation

**Sur ordinateur :**
- `←` / `→` : Page précédente/suivante
- Survolez l'image : Boutons de navigation apparaissent
- Cliquez sur le bouton PDF (en-tête) pour télécharger

**Sur mobile :**
- Swipe gauche/droite pour changer de page
- Bouton PDF flottant en bas à droite
- Tap sur l'image pour masquer/afficher l'interface

### Téléchargement PDF

1. Cliquez sur le bouton **"Télécharger le PDF"** (en-tête desktop ou bouton flottant mobile)
2. Le programme complet se télécharge automatiquement
3. Format : `programme-concert.pdf`

## 🔧 Développement local

### Prérequis
- Docker + Docker Compose
- Node.js 18+ (pour le frontend)
- Python 3.11+ (optionnel, pour scripts)

### Backend

```bash
cd backend
docker-compose up
```

API disponible sur http://localhost:8000  
Documentation Swagger : http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Interface disponible sur http://localhost:3000

### Variables d'environnement

**Backend (.env)**
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/concert_viewer
FRONTEND_URL=http://localhost:3000
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

## 📊 Structure du projet

```
concert-viewer/
├── backend/
│   ├── app/
│   │   ├── api/routes/concerts.py   # Endpoints API
│   │   ├── models.py                # Models SQLAlchemy
│   │   ├── database.py              # Connexion BDD
│   │   └── main.py                  # Application FastAPI
│   ├── scripts/
│   │   ├── generate_init.py         # Génération SQL
│   │   └── upload_to_db.py          # Upload données
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/
│   ├── app/
│   │   ├── concerts/[id]/page.tsx   # Viewer principal
│   │   ├── page.tsx                 # Page d'accueil
│   │   ├── not-found.tsx            # Page 404
│   │   └── error.tsx                # Page erreur
│   ├── components/
│   │   ├── Header.tsx               # En-tête + PDF
│   │   └── ImageViewer.tsx          # Viewer + navigation
│   └── lib/api.ts                   # Fetch API
│
└── README.md
```

## 🚀 Déploiement (Railway)

### Backend
1. Service Docker depuis `backend/`
2. Addon MySQL attaché
3. Variables d'env : `DATABASE_URL`, `FRONTEND_URL`

### Frontend
1. Service Git depuis `frontend/`
2. Variables d'env : `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_GA_ID`

### Upload des données
```bash
python backend/scripts/upload_to_db.py --host <mysql-railway-url>
```

## 📝 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/concerts` | Liste des concerts |
| GET | `/api/concerts/{id}` | Détails d'un concert |
| GET | `/api/concerts/{id}/pages` | Liste des pages (metadata) |
| GET | `/api/concerts/{id}/pages/{num}/png` | Stream PNG d'une page |
| GET | `/api/concerts/{id}/pdf` | Stream PDF complet |

## 🎯 Roadmap future

- [ ] Interface admin pour upload de nouveaux concerts
- [ ] Authentification (si multi-organisations)
- [ ] Support multi-concerts avec liste
- [ ] Statistiques de consultation
- [ ] Cache Redis pour optimisation

## 📄 License

Projet privé - Concert Viewer

---
