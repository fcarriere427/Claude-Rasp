#!/bin/bash

# Script de déploiement du frontend
# À exécuter après avoir modifié le frontend

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
FRONTEND_DIR="$HOME/claude-rasp/code/frontend"
if [ ! -d "$FRONTEND_DIR" ]; then
    print_error "Le répertoire frontend n'existe pas."
fi

# Aller dans le répertoire frontend
cd "$FRONTEND_DIR" || print_error "Impossible d'accéder au répertoire frontend"

# Construire le frontend
print_step "Construction du frontend"
npm run build
print_success "Frontend construit"

# Copier les fichiers vers /var/www
print_step "Déploiement vers /var/www"
sudo mkdir -p /var/www/claude.letsq.xyz
sudo cp -r dist/* /var/www/claude.letsq.xyz/
sudo chown -R www-data:www-data /var/www/claude.letsq.xyz/
print_success "Frontend déployé vers /var/www/claude.letsq.xyz"

# Recharger Nginx
print_step "Rechargement de Nginx"
sudo systemctl reload nginx
print_success "Nginx rechargé"

print_step "Déploiement terminé!"
echo -e "${GREEN}Le frontend a été déployé avec succès.${NC}"
echo -e "${YELLOW}Accédez à l'application via https://claude.letsq.xyz${NC}"
