#!/bin/bash

# Script de déploiement du backend
# À exécuter après avoir modifié le backend

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

# Vérifier que le répertoire d'application existe
BACKEND_DIR="$HOME/claude-rasp/code/backend"
if [ ! -d "$BACKEND_DIR" ]; then
    print_error "Le répertoire backend n'existe pas."
fi

# Aller dans le répertoire backend
cd "$BACKEND_DIR" || print_error "Impossible d'accéder au répertoire backend"

# Activer l'environnement virtuel
source .venv/bin/activate || print_error "Impossible d'activer l'environnement virtuel"

# Mise à jour des dépendances
print_step "Mise à jour des dépendances"
pip install -r requirements.txt
print_success "Dépendances mises à jour"

# Exécution des migrations de base de données (si Alembic est utilisé)
if [ -d "alembic" ]; then
    print_step "Application des migrations"
    alembic upgrade head || print_error "Erreur lors de la migration de la base de données"
    print_success "Migrations de base de données appliquées"
fi

# Redémarrage du service
print_step "Redémarrage du service backend"
sudo systemctl restart claude-rasp-backend.service || print_error "Erreur lors du redémarrage du service"
sleep 2
sudo systemctl status claude-rasp-backend.service --no-pager
print_success "Service backend redémarré"

print_step "Déploiement backend terminé!"
echo -e "${GREEN}Le backend a été déployé avec succès.${NC}"
