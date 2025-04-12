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

# Analyser les arguments
DEV_ENVIRONMENT=false
for arg in "$@"; do
  case $arg in
    --dev)
      DEV_ENVIRONMENT=true
      shift
      ;;
  esac
done

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

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances de production
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    # Installation directe des dépendances si le fichier requirements.txt n'existe pas
    pip install fastapi uvicorn gunicorn sqlalchemy pydantic alembic python-jose[cryptography] passlib[bcrypt] httpx python-multipart pyyaml
fi

# Installer les dépendances de développement si l'option --dev est fournie
if [ "$DEV_ENVIRONMENT" = "true" ]; then
    print_step "Installation des outils de développement"
    if [ -f requirements-dev.txt ]; then
        pip install -r requirements-dev.txt
    else
        # Installation directe des dépendances de développement
        pip install pytest pytest-cov black isort flake8
    fi
    print_success "Outils de développement installés"
fi

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

# Copier le frontend vers /var/www
sudo mkdir -p /var/www/claude.letsq.xyz
sudo cp -r dist/* /var/www/claude.letsq.xyz/
# S'assurer que favicon.ico est bien copié
sudo cp -f public/favicon.ico /var/www/claude.letsq.xyz/
sudo chown -R www-data:www-data /var/www/claude.letsq.xyz/
print_success "Frontend déployé vers /var/www/claude.letsq.xyz"

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

if [ "$DEV_ENVIRONMENT" = "true" ]; then
    echo -e "${YELLOW}Les outils de développement (black, isort, flake8, pytest) ont été installés.${NC}"
    echo -e "${YELLOW}Vous pouvez les utiliser avec 'python -m black', 'python -m isort', etc.${NC}"
else
    echo -e "${YELLOW}Pour installer les outils de développement, relancez le script avec l'option --dev${NC}"
fi

echo -e "${YELLOW}Vous pouvez accéder à l'application via https://claude.letsq.xyz${NC}"
