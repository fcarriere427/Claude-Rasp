# Guide d'utilisation des scripts
# Application Claude API sur Raspberry Pi

Ce document explique comment et quand utiliser les différents scripts disponibles dans le projet. Ces scripts sont conçus pour faciliter l'installation, le déploiement, la maintenance et la sauvegarde de l'application.

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Installation initiale](#installation-initiale)
3. [Déploiement et mises à jour](#déploiement-et-mises-à-jour)
4. [Sauvegarde et restauration](#sauvegarde-et-restauration)
5. [Résolution des problèmes courants](#résolution-des-problèmes-courants)

## Vue d'ensemble

Voici les scripts disponibles et leur fonction principale :

| Script | Emplacement | Description |
|--------|-------------|-------------|
| `install.sh` | code/scripts/ | Installation initiale de l'application |
| `deploy.sh` | code/scripts/ | Déploiement et mise à jour de l'application |
| `backup.sh` | code/scripts/ | Sauvegarde et restauration des données |
| `setup_permissions.sh` | code/scripts/ | Configuration des permissions pour les scripts |

**Note importante** : Tous les scripts doivent être exécutés sur le Raspberry Pi, et tous (sauf `setup_permissions.sh`) nécessitent des droits sudo pour certaines opérations.

## Installation initiale

### Quand utiliser `install.sh`

Utilisez ce script lorsque vous :
- Installez l'application pour la première fois sur votre Raspberry Pi
- Souhaitez réinstaller l'application complètement

### Comment utiliser `install.sh`

1. Assurez-vous que votre Raspberry Pi est connecté à Internet
2. Clonez le dépôt Git du projet
   ```bash
   git clone https://github.com/fcarriere427/claude-rasp.git ~/claude-rasp-temp
   ```

3. Rendez le script exécutable
   ```bash
   chmod +x ~/claude-rasp-temp/code/scripts/install.sh
   ```

4. Exécutez le script d'installation
   ```bash
   ~/claude-rasp-temp/code/scripts/install.sh
   ```

5. Configurez vos fichiers d'environnement (`.env`)
   - Modifiez `~/claude-rasp/code/backend/.env` avec votre clé API Claude
   - Modifiez `~/claude-rasp/code/frontend/.env` si nécessaire

6. Accédez à l'application via votre navigateur à l'adresse : https://claude.letsq.xyz

### Ce que fait `install.sh`

- Crée la structure de répertoires nécessaire
- Clone le dépôt Git à l'emplacement spécifié
- Configure l'environnement virtuel Python pour le backend
- Installe les dépendances avec Poetry
- Configure les fichiers d'environnement à partir des exemples
- Installe les dépendances du frontend et construit l'application
- Configure Nginx
- Configure et démarre le service systemd

## Déploiement et mises à jour

### Quand utiliser `deploy.sh`

Utilisez ce script lorsque vous :
- Mettez à jour l'application avec de nouvelles fonctionnalités ou correctifs
- Synchronisez votre instance avec la dernière version du dépôt Git

### Comment utiliser `deploy.sh`

1. Accédez au répertoire de scripts
   ```bash
   cd ~/claude-rasp/code/scripts
   ```

2. Exécutez le script de déploiement
   ```bash
   ./deploy.sh
   ```

3. Suivez les instructions à l'écran, en particulier si des modifications locales sont détectées

### Ce que fait `deploy.sh`

- Crée une sauvegarde avant toute modification
- Récupère les dernières modifications depuis le dépôt Git
- Met à jour les dépendances du backend et du frontend
- Exécute les migrations de base de données si nécessaire
- Reconstruit le frontend
- Redémarre les services

## Sauvegarde et restauration

### Quand utiliser `backup.sh`

Utilisez ce script pour :
- Effectuer une sauvegarde régulière des données (planifiez-le avec cron)
- Sauvegarder manuellement avant des opérations risquées
- Restaurer l'application à partir d'une sauvegarde précédente

### Comment utiliser `backup.sh`

#### Pour effectuer une sauvegarde :

```bash
cd ~/claude-rasp/code/scripts
./backup.sh -b
# ou simplement
./backup.sh
```

#### Pour restaurer à partir d'une sauvegarde :

```bash
cd ~/claude-rasp/code/scripts
./backup.sh -r backup_20250407_120000.tar.gz
```

#### Pour afficher l'aide :

```bash
./backup.sh -h
```

### Ce que fait `backup.sh`

- En mode sauvegarde :
  - Arrête temporairement le service
  - Crée une archive des données et configurations essentielles
  - Supprime les sauvegardes anciennes (garde les 7 plus récentes)
  - Redémarre le service

- En mode restauration :
  - Arrête le service
  - Crée une sauvegarde temporaire des données actuelles (par sécurité)
  - Restaure les données à partir de la sauvegarde spécifiée
  - Redémarre le service

## Résolution des problèmes courants

### Permissions des scripts

Si vous rencontrez des erreurs de permission en exécutant les scripts, utilisez `setup_permissions.sh` :

```bash
cd ~/claude-rasp/code/scripts
chmod +x setup_permissions.sh
./setup_permissions.sh
```

### Erreurs de service systemd

Si le service systemd ne démarre pas correctement :

1. Vérifiez son statut :
   ```bash
   sudo systemctl status claude-rasp-backend.service
   ```

2. Consultez les journaux :
   ```bash
   sudo journalctl -u claude-rasp-backend.service -n 50
   ```

3. Redémarrez le service manuellement :
   ```bash
   sudo systemctl restart claude-rasp-backend.service
   ```

### Restauration en cas d'échec de déploiement

Si un déploiement échoue et que l'application ne fonctionne plus :

1. Identifiez la dernière sauvegarde disponible :
   ```bash
   ls -la ~/claude-rasp/storage/backups/
   ```

2. Restaurez à partir de cette sauvegarde :
   ```bash
   cd ~/claude-rasp/code/scripts
   ./backup.sh -r [nom_du_fichier_de_sauvegarde]
   ```

## Planification des sauvegardes

Pour configurer des sauvegardes automatiques quotidiennes, ajoutez une tâche cron :

```bash
crontab -e
```

Puis ajoutez la ligne suivante pour une sauvegarde quotidienne à 2h du matin :

```
0 2 * * * /home/florian/claude-rasp/code/scripts/backup.sh -b
```
