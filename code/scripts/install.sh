#!/bin/bash

# Script d'installation pour l'application Claude API sur Raspberry Pi
# À exécuter sur le Raspberry Pi

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

# Vérifier si le script est exécuté en tant que root
if [ "$EUID" -eq 0 ]; then
  print_error "Ce script ne doit pas être exécuté en tant que root. Utilisez votre utilisateur normal."
fi

# Définition des chemins
INSTALL_DIR="$HOME/claude-rasp"
CODE_DIR="$INSTALL_DIR/code"
BACKEND_DIR="$CODE_DIR/backend"
FRONTEND_DIR="$CODE_DIR/frontend"
CONFIG_DIR="$CODE_DIR/config"
STORAGE_DIR="$INSTALL_DIR/storage"
SYSTEMD_DIR="/etc/systemd/system"

# Création des répertoires
print_step "Création des répertoires"
mkdir -p "$BACKEND_DIR" "$FRONTEND_DIR" "$CONFIG_DIR" "$STORAGE_DIR/database" "$STORAGE_DIR/logs" "$STORAGE_DIR/backups"
print_success "Répertoires créés"

# Cloner le dépôt Git (à modifier avec votre URL)
print_step "Clonage du dépôt Git"
git clone https://github.com/fcarriere427/claude-rasp.git "$INSTALL_DIR/temp"
cp -r "$INSTALL_DIR/temp/"* "$INSTALL_DIR/"
rm -rf "$INSTALL_DIR/temp"
print_success "Dépôt cloné"

# Installation du backend
print_step "Installation du backend"
cd "$BACKEND_DIR" || print_error "Impossible d'accéder au répertoire backend"

# Créer un environnement virtuel Python
python3 -m venv .venv
source .venv/bin/activate

# Installer Poetry si nécessaire
if ! command -v poetry &> /dev/null; then
    pip install poetry
fi

# Installer les dépendances
poetry install

# Créer le fichier .env à partir de l'exemple
if [ ! -f .env ]; then
    cp .env.example .env
    print_success "Fichier .env créé. Pensez à le modifier avec vos clés API."
fi

print_success "Backend installé"

# Installation du frontend
print_step "Installation du frontend"
cd "$FRONTEND_DIR" || print_error "Impossible d'accéder au répertoire frontend"

# Installer les dépendances Node.js
npm install

# Créer le fichier .env à partir de l'exemple
if [ ! -f .env ]; then
    cp .env.example .env
    print_success "Fichier .env créé. Pensez à le modifier si nécessaire."
fi

# Construire le frontend
npm run build
print_success "Frontend installé et construit"

# Configuration Nginx
print_step "Configuration de Nginx"
sudo cp "$CONFIG_DIR/nginx.conf" /etc/nginx/sites-available/claude.letsq.xyz
sudo ln -sf /etc/nginx/sites-available/claude.letsq.xyz /etc/nginx/sites-enabled/
sudo nginx -t || print_error "Configuration Nginx invalide"
sudo systemctl reload nginx
print_success "Nginx configuré"

# Configuration Systemd
print_step "Configuration des services systemd"
sudo cp "$CONFIG_DIR/systemd/claude-rasp-backend.service" "$SYSTEMD_DIR/"
sudo systemctl daemon-reload
sudo systemctl enable claude-rasp-backend.service
sudo systemctl start claude-rasp-backend.service
print_success "Services systemd configurés"

print_step "Installation terminée!"
echo -e "${GREEN}L'application Claude API est maintenant installée sur votre Raspberry Pi.${NC}"
echo -e "${YELLOW}N'oubliez pas de configurer vos fichiers .env avec vos clés API et autres paramètres.${NC}"
echo -e "${YELLOW}Vous pouvez accéder à l'application via https://claude-rasp.local si vous avez configuré ce nom d'hôte.${NC}"
