# Suivi de Projet: Application Claude API sur Raspberry Pi

## Journal de progression

| Date | Phase | Tâche | Statut | Commentaires |
|------|-------|-------|--------|-------------|
| 06/04/2025 | Phase 0 | Création du document de suivi | ✅ | Document initial pour suivre la progression du projet |
| 06/04/2025 | Phase 0 | Préparation du Raspberry Pi | ✅ | Raspberry Pi déjà disponible, installé et fonctionnel |
| 06/04/2025 | Phase 0 | Installation des outils de développement | ✅ | Python, Node.js, Git, Nginx et autres outils déjà installés |
| 06/04/2025 | Phase 0 | Création de la structure de répertoires | ✅ | Structure de répertoires créée selon l'architecture définie |
| 06/04/2025 | Phase 0 | Configuration des outils de qualité de code | ✅ | Configuration de Black, isort, flake8 pour le backend et ESLint, Prettier pour le frontend |
| 06/04/2025 | Phase 0 | Spécifications techniques | ✅ | Documentation des API, modèles de données et flux d'authentification
| 06/04/2025 | Phase 0 | Intégration à la configuration Nginx existante | ✅ | Configuration de claude.letsq.xyz, adaptation des fichiers de configuration
| 07/04/2025 | Phase 0 | Mise à jour des chemins d'installation | ✅ | Modification des chemins de "Claude-Rasp" à "claude-rasp" dans les fichiers de configuration
| 07/04/2025 | Phase 0 | Création des scripts de déploiement et sauvegarde | ✅ | Ajout des scripts deploy.sh, backup.sh et setup_permissions.sh
| 07/04/2025 | Phase 0 | Documentation des scripts | ✅ | Création d'un guide d'utilisation des scripts (scripts-guide.md)
| 07/04/2025 | Phase 0 | Correction des chemins dans les scripts | ✅ | Correction du script install.sh pour respecter la structure de répertoires avec sous-dossier code
| 07/04/2025 | Phase 1 | Correction des erreurs d'installation | ✅ | Correction de l'installation de Poetry et ajout de la structure minimale du frontend

## Phase 0: Préparation et setup (1-2 semaines)

### 1. Préparation du Raspberry Pi
- [x] Installation de Raspberry Pi OS (64-bit)
- [x] Configuration réseau et sécurité de base
- [x] Installation des outils de développement

### 2. Mise en place de l'environnement de développement
- [x] Configuration du dépôt Git
- [x] Création des structures de répertoires
- [x] Initialisation des projets backend et frontend
- [x] Configuration des outils de qualité de code (linters, formatters)

### 3. Préparation des spécifications techniques
- [x] Spécifications détaillées des API
- [x] Définition des modèles de données
- [x] Documentation du flux d'authentification
- [x] Création des maquettes UI

### 4. Configuration infrastructures communes
- [x] Setup Nginx comme reverse proxy (intégré à la configuration existante de letsq.xyz)
- [x] Configuration des certificats SSL (utilisation du certificat existant de letsq.xyz)
- [x] Mise en place de systemd pour les services
- [x] Scripts d'installation et de déploiement

## Phase 1: MVP - Fonctionnalités essentielles (3-4 semaines)

### 1. Frontend - Interface utilisateur minimaliste
- [x] Structure Vue.js de base
- [x] Interface de login/password
- [x] Interface de conversation
- [x] Interface de monitoring des coûts
- [x] Interface de paramètres

### 2. Backend - Fonctionnalités de base
- [ ] Implémentation de l'API REST avec FastAPI
- [ ] Système d'authentification avec JWT
- [ ] Intégration avec l'API Claude
- [ ] Modèles de base de données essentiels

### 3. Système MCP v1
- [ ] Parser de configuration YAML pour les outils MCP
- [ ] Intégration avec Brave Search API
- [ ] Routage des appels aux outils

### 4. Monitoring simple
- [ ] Comptage des tokens et conversion en coûts
- [ ] Stockage des métriques d'utilisation
- [ ] Implémentation du kill switch

## Phase 2: Amélioration du monitoring et des limites (2-3 semaines)
*À démarrer après la complétion de la Phase 1*

## Phase 3: Amélioration de l'interface MCP et de l'UX (2-3 semaines)
*À démarrer après la complétion de la Phase 2*

## Phase 4: Authentification Google et multi-utilisateurs (2-3 semaines)
*À démarrer après la complétion de la Phase 3*

## Phase 5: Polissage et fonctionnalités avancées (2-3 semaines)
*À démarrer après la complétion de la Phase 4*

## Notes et décisions importantes
- *Cette section servira à documenter les décisions importantes prises pendant le développement*
