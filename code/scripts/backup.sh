#!/bin/bash

# Script de sauvegarde pour l'application Claude API sur Raspberry Pi
# Ce script effectue une sauvegarde des données essentielles de l'application

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

# Fonction d'affichage de l'aide
show_help() {
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -b, --backup    Effectue une sauvegarde (par défaut)"
    echo "  -r, --restore FILE  Restaure une sauvegarde depuis le fichier spécifié"
    echo "  -h, --help      Affiche cette aide"
    echo
    echo "Exemples:"
    echo "  $0 -b           # Effectue une sauvegarde"
    echo "  $0 -r backup_20250407_120000.tar.gz  # Restaure la sauvegarde spécifiée"
}

# Définition des chemins
APP_DIR="$HOME/claude-rasp"
BACKUP_DIR="$APP_DIR/storage/backups"
DATABASE_DIR="$APP_DIR/storage/database"

# Vérifier que le répertoire d'application existe
if [ ! -d "$APP_DIR" ]; then
    print_error "Le répertoire d'application n'existe pas. Exécutez d'abord le script d'installation."
fi

# Fonction de sauvegarde
do_backup() {
    print_step "Création d'une sauvegarde"
    
    # Création du répertoire de sauvegarde si nécessaire
    mkdir -p "$BACKUP_DIR"
    
    # Génération du nom de fichier avec date et heure
    BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/backup_$BACKUP_DATE.tar.gz"
    
    # Arrêt temporaire du service pour éviter les modifications pendant la sauvegarde
    sudo systemctl stop claude-rasp-backend.service
    print_success "Service arrêté temporairement pour la sauvegarde"
    
    # Sauvegarde des fichiers essentiels
    tar -czf "$BACKUP_FILE" \
        -C "$APP_DIR" storage/database \
        -C "$APP_DIR" code/backend/.env code/frontend/.env \
        -C "$APP_DIR" storage/logs \
        2>/dev/null
    
    # Redémarrage du service
    sudo systemctl start claude-rasp-backend.service
    print_success "Service redémarré"
    
    # Vérification de la création du fichier de sauvegarde
    if [ -f "$BACKUP_FILE" ]; then
        print_success "Sauvegarde créée: $BACKUP_FILE"
        
        # Nettoyage des anciennes sauvegardes (garder les 7 plus récentes)
        print_step "Nettoyage des anciennes sauvegardes"
        ls -t "$BACKUP_DIR"/backup_*.tar.gz | tail -n +8 | xargs -r rm
        print_success "Nettoyage terminé, les 7 sauvegardes les plus récentes sont conservées"
    else
        print_error "Erreur lors de la création de la sauvegarde"
    fi
}

# Fonction de restauration
do_restore() {
    RESTORE_FILE="$1"
    
    # Vérifier que le fichier existe
    if [ ! -f "$RESTORE_FILE" ]; then
        if [ -f "$BACKUP_DIR/$RESTORE_FILE" ]; then
            RESTORE_FILE="$BACKUP_DIR/$RESTORE_FILE"
        else
            print_error "Le fichier de sauvegarde spécifié n'existe pas: $RESTORE_FILE"
        fi
    fi
    
    print_step "Restauration depuis: $RESTORE_FILE"
    
    # Confirmation de l'utilisateur
    echo -e "${YELLOW}ATTENTION: Cette opération va remplacer les données actuelles de l'application.${NC}"
    read -p "Êtes-vous sûr de vouloir continuer? (o/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        print_error "Restauration annulée."
    fi
    
    # Arrêt du service
    sudo systemctl stop claude-rasp-backend.service
    print_success "Service arrêté pour la restauration"
    
    # Sauvegarde des données actuelles au cas où
    TEMP_BACKUP="$BACKUP_DIR/pre_restore_$(date +"%Y%m%d_%H%M%S").tar.gz"
    tar -czf "$TEMP_BACKUP" -C "$APP_DIR" storage/database code/backend/.env code/frontend/.env storage/logs 2>/dev/null
    print_success "Sauvegarde temporaire créée: $TEMP_BACKUP"
    
    # Extraction de la sauvegarde
    tar -xzf "$RESTORE_FILE" -C "$APP_DIR"
    
    # Redémarrage du service
    sudo systemctl start claude-rasp-backend.service
    print_success "Service redémarré"
    
    print_success "Restauration terminée avec succès"
}

# Traitement des arguments
MODE="backup"
RESTORE_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -b|--backup)
            MODE="backup"
            shift
            ;;
        -r|--restore)
            MODE="restore"
            RESTORE_FILE="$2"
            if [ -z "$RESTORE_FILE" ]; then
                print_error "Vous devez spécifier un fichier de sauvegarde à restaurer"
            fi
            shift 2
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
done

# Exécution du mode sélectionné
if [ "$MODE" = "backup" ]; then
    do_backup
elif [ "$MODE" = "restore" ]; then
    do_restore "$RESTORE_FILE"
fi
