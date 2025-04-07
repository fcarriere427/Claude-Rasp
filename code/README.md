# Application Claude API sur Raspberry Pi

Ce projet est une application web auto-hébergée permettant d'interagir avec l'API Claude (3.7 Sonnet) depuis n'importe quel navigateur, avec une gestion des coûts et un système d'authentification sécurisé.

## Fonctionnalités

- Interface de conversation interactive avec Claude
- Authentification sécurisée
- Intégration MCP (Multi-Claude Process) pour utiliser des outils externes
- Monitoring des coûts et gestion des limites
- Support du markdown dans les conversations
- Réponses en streaming
- Export des conversations

## Structure du projet

```
claude-rasp/
├── code/
│   ├── .github/                    # CI/CD configurations (à venir)
│   ├── docs/                       # Documentation
│   ├── frontend/                   # Application Vue.js
│   │   ├── public/                 # Fichiers statiques
│   │   └── src/                    # Code source
│   │       ├── assets/              # Ressources (images, etc.)
│   │       ├── components/          # Composants Vue
│   │       ├── views/                # Pages Vue
│   │       ├── router/               # Configuration des routes
│   │       ├── store/                # Gestion de l'état (Pinia)
│   │       ├── services/             # Services API
│   │       └── utils/                # Utilitaires
│   ├── backend/                    # Application FastAPI
│   │   ├── app/                    # Code source
│   │   │   ├── api/                 # Endpoints API
│   │   │   ├── core/                # Configuration
│   │   │   ├── db/                  # Gestion base de données
│   │   │   ├── models/              # Modèles SQLAlchemy
│   │   │   ├── schemas/             # Schémas Pydantic
│   │   │   ├── services/            # Services métier
│   │   │   └── utils/               # Utilitaires
│   │   └── tests/                  # Tests unitaires et intégration
│   ├── config/                     # Configuration de l'application
│   │   ├── mcp_config.yaml         # Configuration MCP
│   │   ├── nginx.conf              # Configuration Nginx
│   │   └── systemd/                # Services systemd
│   └── scripts/                    # Scripts utilitaires
│       ├── install.sh              # Installation
│       ├── deploy.sh               # Déploiement complet
│       ├── deploy_frontend.sh      # Déploiement frontend uniquement
│       ├── backup.sh               # Sauvegarde et restauration
│       └── setup_permissions.sh    # Configuration des permissions
└── storage/                    # Données persistantes
    ├── database/              # Fichiers SQLite
    ├── logs/                  # Logs
    └── backups/               # Sauvegardes
```

## Prérequis

- Raspberry Pi 4 (2GB RAM minimum)
- Raspberry Pi OS (64-bit)
- Python 3.9+
- Node.js 18+
- Nginx
- Git

## Installation 

### Sur Raspberry Pi

1. Clonez ce dépôt sur votre Raspberry Pi :
   ```bash
   git clone https://github.com/fcarriere427/claude-rasp.git ~/claude-rasp
   ```

2. Exécutez le script d'installation :
   ```bash
   cd ~/claude-rasp
   bash code/scripts/install.sh
   ```

3. Configurez les fichiers d'environnement :
   - Modifiez `code/backend/.env` avec votre clé API Claude
   - Ajustez les limites par défaut si nécessaire

4. Accédez à l'application via votre navigateur :
   ```
   https://claude.letsq.xyz/
   ```
   ou via l'adresse IP de votre Raspberry Pi

## Développement

### Backend (FastAPI)

1. Créez et activez un environnement virtuel :
   ```bash
   cd code/backend
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
   ```

2. Installez les dépendances avec pip :
   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn gunicorn sqlalchemy pydantic alembic python-jose[cryptography] passlib[bcrypt] httpx python-multipart pyyaml
   ```

3. Démarrez le serveur de développement :
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Accédez à la documentation API :
   ```
   http://localhost:8000/docs
   ```

### Frontend (Vue.js)

1. Installez les dépendances :
   ```bash
   cd code/frontend
   npm install
   ```

2. Démarrez le serveur de développement :
   ```bash
   npm run serve
   ```

3. Pour déployer le frontend :
   ```bash
   cd ../scripts
   ./deploy_frontend.sh
   ```

### Configuration Vue.js

Un fichier `vue.config.js` est inclus à la racine du projet frontend pour assurer une compilation correcte :

```javascript
module.exports = {
  publicPath: '/',
  configureWebpack: {
    devtool: 'source-map'
  }
}
```

Ce fichier est nécessaire pour éviter l'erreur `ReferenceError: process is not defined` lors de l'exécution de l'application.

## Scripts disponibles

| Script | Description |
|--------|-------------|
| `install.sh` | Installation initiale de l'application |
| `deploy.sh` | Déploiement et mise à jour complète de l'application |
| `deploy_frontend.sh` | Déploiement du frontend uniquement |
| `backup.sh` | Sauvegarde et restauration des données |
| `setup_permissions.sh` | Configuration des permissions pour les scripts |

Pour plus de détails sur l'utilisation des scripts, consultez le fichier `scripts-guide.md` à la racine du projet.

## Résolution des problèmes courants

### Erreur "ReferenceError: process is not defined"

Si vous rencontrez cette erreur dans la console du navigateur :

1. Vérifiez que le fichier `vue.config.js` existe dans le répertoire frontend
2. Exécutez à nouveau le script de déploiement frontend :
   ```bash
   cd ~/claude-rasp/code/scripts
   ./deploy_frontend.sh
   ```

### Problèmes d'installation du backend

Si vous rencontrez des problèmes avec l'installation du backend :

1. Supprimez l'environnement virtuel existant :
   ```bash
   cd ~/claude-rasp/code/backend
   rm -rf .venv
   ```

2. Créez-en un nouveau et installez les dépendances avec pip :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install fastapi uvicorn gunicorn sqlalchemy pydantic alembic python-jose[cryptography] passlib[bcrypt] httpx python-multipart pyyaml
   ```

## Licence

Ce projet est destiné à un usage personnel ou en petite équipe. L'utilisation de l'API Claude est soumise aux conditions d'utilisation d'Anthropic.
