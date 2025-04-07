#!/bin/bash

# Script de déploiement pour l'application Claude API sur Raspberry Pi
# Ce script met à jour l'application à partir du dépôt Git et redémarre les services

# Définition des couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages d'étape
print_step() {
    echo -e "${YELLOW}==== $1 ====${NC}"
}

# Fonction pour afficher les messages de succès
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Fonction pour afficher les erreurs
print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# Définition des chemins
APP_DIR="$HOME/claude-rasp"
BACKEND_DIR="$APP_DIR/code/backend"
FRONTEND_DIR="$APP_DIR/code/frontend"
BACKUP_DIR="$APP_DIR/storage/backups"

# Vérifier que le répertoire d'application existe
if [ ! -d "$APP_DIR" ]; then
    print_error "Le répertoire d'application n'existe pas. Exécutez d'abord le script d'installation."
fi

# Création d'une sauvegarde avant mise à jour
print_step "Création d'une sauvegarde"
BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_$BACKUP_DATE.tar.gz"

# Sauvegarde des fichiers de configuration et base de données
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_FILE" -C "$APP_DIR" storage/database .env code/backend/.env code/frontend/.env
print_success "Sauvegarde créée: $BACKUP_FILE"

# Mise à jour du code source depuis le dépôt Git
print_step "Mise à jour du code source"
cd "$APP_DIR" || print_error "Impossible d'accéder au répertoire de l'application"

# Vérifier les changements locaux non commités
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}ATTENTION: Des modifications locales non commités ont été détectées.${NC}"
    echo -e "Ces modifications pourraient être écrasées lors de la mise à jour."
    read -p "Voulez-vous continuer? (o/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        print_error "Déploiement annulé."
    fi
    # Option: sauvegarder les changements locaux
    git stash
    print_success "Modifications locales sauvegardées"
fi

# Récupérer les dernières modifications
git pull origin main || print_error "Impossible de récupérer les dernières modifications"
print_success "Code source mis à jour"

# Mise à jour du backend
print_step "Mise à jour du backend"
cd "$BACKEND_DIR" || print_error "Impossible d'accéder au répertoire backend"
source .venv/bin/activate

# Mise à jour des dépendances
poetry install
print_success "Dépendances backend mises à jour"

# Exécution des migrations de base de données (si Alembic est utilisé)
if [ -d "alembic" ]; then
    alembic upgrade head || print_error "Erreur lors de la migration de la base de données"
    print_success "Migrations de base de données appliquées"
fi

# Mise à jour du frontend
print_step "Mise à jour du frontend"
cd "$FRONTEND_DIR" || print_error "Impossible d'accéder au répertoire frontend"

# Mise à jour des dépendances
npm install
print_success "Dépendances frontend mises à jour"

# Construction du frontend
npm run build
print_success "Frontend construit"

# Redémarrage des services
print_step "Redémarrage des services"
sudo systemctl restart claude-rasp-backend.service
sudo systemctl status claude-rasp-backend.service --no-pager
print_success "Services redémarrés"

print_step "Déploiement terminé!"
echo -e "${GREEN}L'application Claude API a été mise à jour avec succès.${NC}"
echo -e "${YELLOW}Si vous rencontrez des problèmes, vous pouvez restaurer la sauvegarde: $BACKUP_FILE${NC}"
