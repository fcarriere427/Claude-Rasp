# Document d'Architecture
# Application Claude API sur Raspberry Pi

## 1. Vue d'ensemble de l'architecture

### 1.1 Architecture générale
L'application suit une architecture classique client-serveur avec les composants suivants:

```
┌─────────────────┐     ┌─────────────────────────────────────┐     ┌───────────────┐
│                 │     │            Raspberry Pi             │     │               │
│   Navigateurs   │     │                                     │     │  API Claude   │
│   (Clients)     │◄────┤  Frontend ◄───► Backend ◄───► DB    │◄────┤  & Services   │
│                 │     │     │           │                   │     │  Externes     │
└─────────────────┘     └─────┼───────────┼───────────────────┘     └───────────────┘
                              │           │
                              ▼           ▼
                        ┌─────────┐ ┌────────────┐
                        │ Système │ │ Monitoring │
                        │ de      │ │    &       │
                        │ fichiers│ │ Logging    │
                        └─────────┘ └────────────┘
```

### 1.2 Composants principaux
1. **Frontend**: Interface utilisateur web responsive
2. **Backend**: API RESTful gérant la logique métier
3. **Base de données**: Stockage persistant des données
4. **Gestionnaire d'authentification**: Service dédié à l'authentification
5. **Gestionnaire MCP**: Service pour l'intégration des outils MCP
6. **Système de monitoring**: Suivi et visualisation des coûts
7. **Système de limites**: Implémentation du kill switch et des alertes

## 2. Stack technologique

### 2.1 Backend
- **Langage**: Python 3.9+
- **Framework**: FastAPI (choisi pour ses performances et son typage statique)
- **ASGI Server**: Uvicorn avec Gunicorn comme gestionnaire de processus
- **Authentification**: JWT (JSON Web Tokens), Bcrypt pour le hachage
- **Documentation API**: Swagger UI (intégré à FastAPI)

### 2.2 Frontend
- **Framework**: Vue.js 3 (version légère, adaptée aux performances du Raspberry Pi)
- **HTTP Client**: Axios
- **UI Components**: PrimeVue (léger, accessible, responsive)
- **State Management**: Pinia
- **Visualisations**: Chart.js pour les graphiques de monitoring

### 2.3 Base de données
- **V1**: SQLite (faible empreinte ressource, adapté au Raspberry Pi)
- **V2**: Option de migration vers PostgreSQL pour plus de robustesse
- **ORM**: SQLAlchemy pour les interactions avec la DB
- **Migrations**: Alembic pour les évolutions de schéma

### 2.4 Infrastructure
- **OS**: Raspberry Pi OS (64-bit recommandé)
- **Serveur web**: Nginx comme reverse proxy
- **SSL/TLS**: Let's Encrypt pour HTTPS
- **Conteneurisation**: Docker (optionnel pour simplifier le déploiement)
- **Process Manager**: Systemd pour les services

### 2.5 Outils de développement
- **Gestion des dépendances**: pip (pour simplicité d'utilisation sur Raspberry Pi)
- **Linting & Formatting**: Black, isort, flake8
- **Testing**: Pytest avec pytest-cov pour la couverture
- **CI**: GitHub Actions (tests automatisés)

## 3. Structure des fichiers

```
claude-rasp/
├── code/                        # Code source de l'application
│   ├── docs/                    # Documentation
│   ├── frontend/                # Application Vue.js
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── assets/          # Ressources (images, etc.)
│   │   │   ├── components/      # Composants Vue
│   │   │   │   ├── conversation/ # Composants de conversation
│   │   │   │   ├── auth/        # Composants d'authentification
│   │   │   │   ├── dashboard/   # Composants de monitoring
│   │   │   │   └── admin/       # Composants d'administration (V2)
│   │   │   ├── views/           # Pages Vue
│   │   │   ├── router/          # Configuration des routes
│   │   │   ├── store/           # Gestion de l'état (Pinia)
│   │   │   ├── services/        # Services API
│   │   │   └── utils/           # Utilitaires
│   │   ├── .env.example
│   │   ├── package.json
│   │   └── vue.config.js        # Configuration Vue
│   ├── backend/                 # Application FastAPI
│   │   ├── app/
│   │   │   ├── api/             # Endpoints API
│   │   │   │   ├── v1/
│   │   │   │   │   ├── auth.py  # Authentification
│   │   │   │   │   ├── chat.py  # Conversations
│   │   │   │   │   ├── mcp.py   # Gestion MCP
│   │   │   │   │   └── monitor.py # Monitoring
│   │   │   │   └── v2/          # Endpoints V2 (futur)
│   │   │   ├── core/            # Configuration et utilitaires
│   │   │   ├── db/              # Gestion base de données
│   │   │   ├── models/          # Modèles SQLAlchemy
│   │   │   ├── schemas/         # Schémas Pydantic
│   │   │   ├── services/        # Services métier
│   │   │   ├── utils/           # Utilitaires
│   │   │   └── main.py          # Point d'entrée
│   │   ├── tests/               # Tests unitaires et intégration
│   │   ├── .env.example
│   │   └── requirements.txt     # Dépendances Python
│   ├── config/                  # Configuration de l'application
│   │   ├── mcp_config.yaml      # Configuration MCP (V1)
│   │   ├── nginx.conf           # Configuration Nginx
│   │   └── systemd/             # Services systemd
│   └── scripts/                 # Scripts utilitaires
│       ├── install.sh           # Installation
│       ├── deploy.sh            # Déploiement complet
│       ├── deploy_frontend.sh   # Déploiement frontend uniquement
│       ├── backup.sh            # Sauvegarde et restauration
│       └── setup_permissions.sh # Configuration des permissions
└── storage/                     # Données persistantes
    ├── database/                # Fichiers SQLite
    ├── logs/                    # Logs applicatifs
    └── backups/                 # Sauvegardes
```

## 4. Modèles de données

### 4.1 Modèle utilisateur
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relations
    conversations = relationship("Conversation", back_populates="user")
    usage_records = relationship("UsageRecord", back_populates="user")
    limits = relationship("UserLimit", back_populates="user")
```

### 4.2 Modèle conversation
```python
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", 
                            order_by="Message.created_at")
```

### 4.3 Modèle message
```python
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # 'user' ou 'assistant'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Métriques
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    
    # Relations
    conversation = relationship("Conversation", back_populates="messages")
```

### 4.4 Modèle utilisation
```python
class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    
    # Relations
    user = relationship("User", back_populates="usage_records")
```

### 4.5 Modèle limites
```python
class UserLimit(Base):
    __tablename__ = "user_limits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    daily_limit = Column(Float)  # en euros
    monthly_limit = Column(Float)  # en euros
    alert_threshold_70 = Column(Boolean, default=True)
    alert_threshold_90 = Column(Boolean, default=True)
    kill_switch_enabled = Column(Boolean, default=True)
    
    # Relations
    user = relationship("User", back_populates="limits")
```

## 5. API Endpoints

### 5.1 Authentification
- `POST /api/v1/auth/login` - Authentification utilisateur
- `POST /api/v1/auth/logout` - Déconnexion
- `POST /api/v1/auth/register` - Création de compte (admin seulement en V1)
- `GET /api/v1/auth/me` - Infos utilisateur courant
- `PUT /api/v1/auth/password` - Changement de mot de passe

### 5.2 Conversations
- `GET /api/v1/conversations` - Liste des conversations
- `POST /api/v1/conversations` - Nouvelle conversation
- `GET /api/v1/conversations/{id}` - Détails d'une conversation
- `DELETE /api/v1/conversations/{id}` - Suppression d'une conversation
- `POST /api/v1/conversations/{id}/messages` - Ajout d'un message
- `GET /api/v1/conversations/{id}/export` - Export d'une conversation

### 5.3 MCP (V1)
- `GET /api/v1/mcp/config` - Configuration MCP actuelle
- `GET /api/v1/mcp/tools` - Liste des outils disponibles

### 5.4 MCP (V2)
- `GET /api/v1/mcp/servers` - Liste des serveurs MCP
- `POST /api/v1/mcp/servers` - Ajout d'un serveur MCP
- `PUT /api/v1/mcp/servers/{id}` - Modification d'un serveur
- `DELETE /api/v1/mcp/servers/{id}` - Suppression d'un serveur
- `GET /api/v1/mcp/servers/{id}/status` - Statut d'un serveur

### 5.5 Monitoring
- `GET /api/v1/monitor/usage/daily` - Usage quotidien
- `GET /api/v1/monitor/usage/monthly` - Usage mensuel
- `GET /api/v1/monitor/limits` - Limites définies
- `PUT /api/v1/monitor/limits` - Modification des limites
- `GET /api/v1/monitor/status` - Statut global (% des limites)

### 5.6 Admin (V2)
- `GET /api/v1/admin/users` - Liste des utilisateurs
- `POST /api/v1/admin/users` - Création d'utilisateur
- `PUT /api/v1/admin/users/{id}` - Modification d'utilisateur
- `DELETE /api/v1/admin/users/{id}` - Suppression d'utilisateur
- `PUT /api/v1/admin/users/{id}/limits` - Définition des limites

## 6. Flux d'interaction

### 6.1 Flux d'authentification
```
┌──────────┐                                 ┌──────────┐                            ┌──────────┐
│          │                                 │          │                            │          │
│  Client  │                                 │ Backend  │                            │  Database│
│          │                                 │          │                            │          │
└────┬─────┘                                 └────┬─────┘                            └────┬─────┘
     │                                            │                                       │
     │ POST /api/v1/auth/login                    │                                       │
     │ {username, password}                       │                                       │
     │ ──────────────────────────────────────────>│                                       │
     │                                            │                                       │
     │                                            │ SELECT user                           │
     │                                            │ ─────────────────────────────────────>│
     │                                            │                                       │
     │                                            │ User record                           │
     │                                            │ <─────────────────────────────────────│
     │                                            │                                       │
     │                                            │ Verify password                       │
     │                                            │ Create JWT                            │
     │                                            │                                       │
     │ 200 OK                                     │                                       │
     │ {token, user}                              │                                       │
     │ <──────────────────────────────────────────│                                       │
     │                                            │                                       │
     │ Store token                                │                                       │
     │                                            │                                       │
     │                                            │                                       │
```

### 6.2 Flux de conversation
```
┌──────────┐                ┌──────────┐                 ┌──────────┐                ┌──────────┐
│          │                │          │                 │          │                │          │
│  Client  │                │ Backend  │                 │ Claude   │                │  Database│
│          │                │          │                 │   API    │                │          │
└────┬─────┘                └────┬─────┘                 └────┬─────┘                └────┬─────┘
     │                           │                            │                           │
     │ Auth: Bearer {token}      │                            │                           │
     │ ──────────────────────────>                            │                           │
     │                           │                            │                           │
     │ POST /api/v1/conversations│                            │                           │
     │ {title}                   │                            │                           │
     │ ──────────────────────────>                            │                           │
     │                           │                            │                           │
     │                           │ INSERT conversation        │                           │
     │                           │ ────────────────────────────────────────────────────────>
     │                           │                            │                           │
     │ 201 Created               │                            │                           │
     │ {id, title}               │                            │                           │
     │ <──────────────────────────                            │                           │
     │                           │                            │                           │
     │ POST /conversations/{id}/messages                      │                           │
     │ {content}                 │                            │                           │
     │ ──────────────────────────>                            │                           │
     │                           │                            │                           │
     │                           │ POST API request           │                           │
     │                           │ ─────────────────────────────>                         │
     │                           │                            │                           │
     │                           │ Stream response            │                           │
     │                           │ <─────────────────────────────                         │
     │                           │                            │                           │
     │ Stream response chunks    │                            │                           │
     │ <──────────────────────────                            │                           │
     │                           │                            │                           │
     │                           │ INSERT messages            │                           │
     │                           │ ────────────────────────────────────────────────────────>
     │                           │                            │                           │
     │                           │ UPDATE usage records       │                           │
     │                           │ ────────────────────────────────────────────────────────>
     │                           │                            │                           │
     │                           │ CHECK limits               │                           │
     │                           │ ────────────────────────────────────────────────────────>
     │                           │                            │                           │
```

### 6.3 Flux de monitoring
```
┌──────────┐                         ┌──────────┐                          ┌──────────┐
│          │                         │          │                          │          │
│  Client  │                         │ Backend  │                          │  Database│
│          │                         │          │                          │          │
└────┬─────┘                         └────┬─────┘                          └────┬─────┘
     │                                    │                                     │
     │ GET /api/v1/monitor/usage/daily   │                                     │
     │ ──────────────────────────────────>                                     │
     │                                    │                                     │
     │                                    │ SELECT FROM usage_records           │
     │                                    │ ─────────────────────────────────────>
     │                                    │                                     │
     │                                    │ Usage data                          │
     │                                    │ <─────────────────────────────────────
     │                                    │                                     │
     │ 200 OK                             │                                     │
     │ {usage data for visualization}     │                                     │
     │ <──────────────────────────────────│                                     │
     │                                    │                                     │
     │ GET /api/v1/monitor/limits         │                                     │
     │ ──────────────────────────────────>                                     │
     │                                    │                                     │
     │                                    │ SELECT FROM user_limits             │
     │                                    │ ─────────────────────────────────────>
     │                                    │                                     │
     │                                    │ Limits data                         │
     │                                    │ <─────────────────────────────────────
     │                                    │                                     │
     │ 200 OK                             │                                     │
     │ {limits, current usage percentage} │                                     │
     │ <──────────────────────────────────│                                     │
     │                                    │                                     │
```

## 7. Mécanismes de sécurité

### 7.1 Authentification
- Stockage sécurisé des mots de passe avec Bcrypt (hachage + sel)
- Tokens JWT avec expiration et rotation
- Protection CSRF avec tokens
- Limitation des tentatives de connexion (rate limiting)

### 7.2 Stockage des secrets
- Variables d'environnement pour les secrets (clés API)
- Fichier .env non versionné
- Option: intégration avec Vault pour V2

### 7.3 Communications
- HTTPS obligatoire avec certificats Let's Encrypt
- En-têtes de sécurité HTTP (CSP, X-Frame-Options, etc.)
- CORS configuré uniquement pour les domaines nécessaires

### 7.4 Validation des entrées
- Validation stricte avec Pydantic
- Protection contre les injections SQL via ORM
- Échappement HTML pour les sorties

## 8. Stratégie de déploiement

### 8.1 Installation initiale
1. Installation Raspberry Pi OS (64-bit)
2. Configuration réseau et sécurité de base
3. Installation des dépendances système (Python, Node.js, etc.)
4. Installation du code source via Git
5. Configuration des variables d'environnement
6. Installation des dépendances Python avec pip
7. Installation des dépendances Frontend (npm)
8. Configuration Nginx et Let's Encrypt
9. Configuration des services systemd
10. Initialisation de la base de données

### 8.2 Mise à jour
- Script de mise à jour automatisé (deploy.sh)
- Sauvegarde automatique avant mise à jour
- Mécanisme de rollback en cas d'échec
- Déploiement séparé du frontend si nécessaire (deploy_frontend.sh)
- Migration de schéma DB avec Alembic

### 8.3 Sauvegarde et restauration
- Script de sauvegarde quotidienne
- Rotation des sauvegardes (7 derniers jours)
- Procédure de restauration documentée
- Option: synchronisation avec stockage externe
