# Maquettes UI
# Application Claude API sur Raspberry Pi

## Vue d'ensemble

Ce document présente les maquettes des principales interfaces utilisateur de l'application Claude API sur Raspberry Pi. Ces maquettes sont conçues pour être minimalistes mais fonctionnelles, en accord avec les contraintes de ressources du Raspberry Pi.

L'interface utilisateur s'inspire du design de Claude Desktop tout en ajoutant des fonctionnalités spécifiques comme le monitoring des coûts et la gestion des limites.

## Palette de couleurs et thème

L'application utilise une palette de couleurs simple mais élégante :

- **Couleur principale** : #6366F1 (indigo)
- **Couleur d'accentuation** : #3B82F6 (bleu)
- **Couleur d'alerte** : #EF4444 (rouge)
- **Couleur de succès** : #10B981 (vert)
- **Arrière-plan clair** : #F3F4F6 (gris très clair)
- **Texte foncé** : #1F2937 (gris foncé)
- **Texte clair** : #F9FAFB (blanc cassé)

Deux thèmes sont disponibles :
- **Clair** (défaut)
- **Sombre** (activation manuelle ou automatique selon les préférences du système)

## Écrans principaux

### 1. Écran de connexion

![Écran de connexion](mockups/login_screen.png)

L'écran de connexion contient :
- Logo de l'application
- Champ de nom d'utilisateur
- Champ de mot de passe
- Bouton de connexion
- Option "Se souvenir de moi"
- Message d'erreur (si applicable)

```
┌───────────────────────────────────────────────────┐
│                                                   │
│                   Claude API                      │
│                                                   │
│    ┌───────────────────────────────────────┐     │
│    │ Nom d'utilisateur                     │     │
│    └───────────────────────────────────────┘     │
│                                                   │
│    ┌───────────────────────────────────────┐     │
│    │ Mot de passe                          │     │
│    └───────────────────────────────────────┘     │
│                                                   │
│    □ Se souvenir de moi                           │
│                                                   │
│    ┌───────────────────────────────────────┐     │
│    │            Se connecter               │     │
│    └───────────────────────────────────────┘     │
│                                                   │
└───────────────────────────────────────────────────┘
```

### 2. Écran principal (Conversations)

![Écran principal](mockups/main_screen.png)

L'écran principal est divisé en deux parties :
- Barre latérale à gauche avec la liste des conversations
- Zone principale de conversation à droite

```
┌───────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────┐ ┌─────────────────────────────────────────┐   │
│ │   Claude API        │ │ Conversation Title              [⚙️]    │   │
│ │ ┌─────────────────┐ │ │                                         │   │
│ │ │ + Nouvelle conv.│ │ │                                         │   │
│ │ └─────────────────┘ │ │                                         │   │
│ │                     │ │                                         │   │
│ │ Conversations:      │ │  [Assistant] Lorem ipsum dolor sit amet,│   │
│ │ • Introduction      │ │  consectetur adipiscing elit. Nullam... │   │
│ │ • Projet XYZ        │ │                                         │   │
│ │ • Analyse doc       │ │  [Utilisateur] Pouvez-vous m'expliquer  │   │
│ │ • Questions         │ │  comment fonctionne la tokenisation?    │   │
│ │                     │ │                                         │   │
│ │                     │ │  [Assistant] La tokenisation est le     │   │
│ │                     │ │  processus qui consiste à découper du   │   │
│ │                     │ │  texte en unités plus petites...        │   │
│ │                     │ │                                         │   │
│ │                     │ │                                         │   │
│ │                     │ ├─────────────────────────────────────────┤   │
│ │                     │ │ ┌─────────────────────────────────┐ [⏎]│   │
│ │                     │ │ │ Tapez votre message ici...      │     │   │
│ │                     │ │ └─────────────────────────────────┘     │   │
│ └─────────────────────┘ └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

### 3. Monitoring des coûts

![Monitoring](mockups/monitoring_screen.png)

L'écran de monitoring affiche :
- Graphique d'utilisation quotidienne
- Progression vers les limites
- Statistiques d'utilisation
- Options de configuration des limites

```
┌───────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────┐ ┌─────────────────────────────────────────┐   │
│ │   Claude API        │ │ Monitoring des coûts                    │   │
│ │ ┌─────────────────┐ │ │                                         │   │
│ │ │ + Nouvelle conv.│ │ │  Utilisation quotidienne                │   │
│ │ └─────────────────┘ │ │  ┌─────────────────────────────────┐   │   │
│ │                     │ │  │                                 │   │   │
│ │ • Conversations     │ │  │  [Graphique d'utilisation]      │   │   │
│ │ • Monitoring     🔴 │ │  │                                 │   │   │
│ │ • Paramètres        │ │  └─────────────────────────────────┘   │   │
│ │                     │ │                                         │   │
│ │                     │ │  Limite quotidienne: 2,5€ utilisés sur 5€  │
│ │                     │ │  [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░] 50%      │   │
│ │                     │ │                                         │   │
│ │                     │ │  Limite mensuelle: 18,7€ utilisés sur 50€  │
│ │                     │ │  [▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░] 37%    │   │
│ │                     │ │                                         │   │
│ │                     │ │  Paramètres des limites                 │   │
│ │                     │ │  ┌─────────┐   ┌─────────┐              │   │
│ │                     │ │  │ Modifier│   │Historique│             │   │
│ └─────────────────────┘ └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

### 4. Configuration des limites

![Configuration](mockups/limits_config_screen.png)

L'écran de configuration des limites permet :
- Définir la limite quotidienne
- Définir la limite mensuelle
- Configurer les alertes (70%, 90%)
- Activer/désactiver le kill switch

```
┌───────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────┐ ┌─────────────────────────────────────────┐   │
│ │   Claude API        │ │ Configuration des limites               │   │
│ │ ┌─────────────────┐ │ │                                         │   │
│ │ │ + Nouvelle conv.│ │ │  Limites de coûts                       │   │
│ │ └─────────────────┘ │ │                                         │   │
│ │                     │ │  Limite quotidienne:                    │   │
│ │ • Conversations     │ │  ┌─────────────────────┐ EUR            │   │
│ │ • Monitoring        │ │  │ 5,00                │                │   │
│ │ • Paramètres        │ │  └─────────────────────┘                │   │
│ │                     │ │                                         │   │
│ │                     │ │  Limite mensuelle:                      │   │
│ │                     │ │  ┌─────────────────────┐ EUR            │   │
│ │                     │ │  │ 50,00               │                │   │
│ │                     │ │  └─────────────────────┘                │   │
│ │                     │ │                                         │   │
│ │                     │ │  ☑ Alerte à 70% de la limite           │   │
│ │                     │ │  ☑ Alerte à 90% de la limite           │   │
│ │                     │ │  ☑ Activer le kill switch               │   │
│ │                     │ │                                         │   │
│ │                     │ │  ┌─────────┐   ┌─────────┐              │   │
│ │                     │ │  │ Annuler │   │ Enregistrer │          │   │
│ └─────────────────────┘ └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

### 5. Paramètres MCP (Multi-Claude Process)

![MCP Settings](mockups/mcp_settings_screen.png)

L'écran de configuration MCP permet :
- Voir les outils disponibles
- Activer/désactiver des outils
- Configurer les paramètres de chaque outil
- (V2) Gérer les serveurs MCP

```
┌───────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────┐ ┌─────────────────────────────────────────┐   │
│ │   Claude API        │ │ Outils MCP                             │   │
│ │ ┌─────────────────┐ │ │                                         │   │
│ │ │ + Nouvelle conv.│ │ │  Outils disponibles:                     │   │
│ │ └─────────────────┘ │ │                                         │   │
│ │                     │ │  ☑ Recherche Web (Brave Search)            │   │
│ │ • Conversations     │ │     Paramètres ⇒ Limit: 5, Timeout: 10s    │   │
│ │ • Monitoring        │ │                                         │   │
│ │ • MCP            🔴 │ │  ☑ Recherche Locale (Brave Search)         │   │
│ │ • Paramètres        │ │     Paramètres ⇒ Limit: 3, Timeout: 5s     │   │
│ │                     │ │                                         │   │
│ │                     │ │  ☐ Analyse d'image (V2)                   │   │
│ │                     │ │     Non disponible dans cette version     │   │
│ │                     │ │                                         │   │
│ │                     │ │  Paramètres globaux:                     │   │
│ │                     │ │  ☑ Journalisation des requêtes            │   │
│ │                     │ │  ☑ Journalisation des réponses            │   │
│ │                     │ │                                         │   │
│ │                     │ │  ┌─────────┐   ┌─────────┐              │   │
│ │                     │ │  │ Annuler │   │ Enregistrer │              │   │
│ └─────────────────────┘ └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

### 6. Administration des utilisateurs (V2)

![Admin Users](mockups/admin_users_screen.png)

L'écran d'administration des utilisateurs permet :
- Voir tous les utilisateurs
- Créer de nouveaux utilisateurs
- Modifier les paramètres des utilisateurs existants
- Définir des limites par utilisateur

```
┌───────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────┐ ┌─────────────────────────────────────────┐   │
│ │   Claude API        │ │ Administration des utilisateurs          │   │
│ │ ┌─────────────────┐ │ │                                         │   │
│ │ │ + Nouvelle conv.│ │ │  ┌─────────────────────────────────────┐  │   │
│ │ └─────────────────┘ │ │  │ + Nouvel utilisateur               │  │   │
│ │                     │ │  └─────────────────────────────────────┘  │   │
│ │ • Conversations     │ │                                         │   │
│ │ • Monitoring        │ │  ┌─────────────────────────────────────┐  │   │
│ │ • MCP              │ │  │ Nom | Email | Rôle | Statut | Actions │  │   │
│ │ • Administration  🔴 │ │  ├─────────────────────────────────────┤  │   │
│ │ • Paramètres        │ │  │ admin | admin@... | Admin | Actif | ✎✂ │  │   │
│ │                     │ │  │ user1 | user1@... | User  | Actif | ✎✂ │  │   │
│ │                     │ │  │ user2 | user2@... | User  | Inactif| ✎✂ │  │   │
│ │                     │ │  └─────────────────────────────────────┘  │   │
│ │                     │ │                                         │   │
│ │                     │ │                                         │   │
│ │                     │ │                                         │   │
│ │                     │ │                                         │   │
│ │                     │ │                                         │   │
│ │                     │ │                                         │   │
│ └─────────────────────┘ └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

## Composants d'interface

### Barres d'en-tête

La barre d'en-tête contient :
- Titre de la section actuelle
- Bouton de paramètres (si applicable)
- Informations de connexion (utilisateur actuel)
- Indicateur de coût en cours

### Champ de saisie

Le champ de saisie pour les messages possède les fonctionnalités suivantes :
- Support du markdown
- Bouton d'envoi
- Option pour téléverser des fichiers (version future)
- Auto-redimensionnement

### Bulles de message

Les messages sont affichés dans des bulles distinctes :
- Messages utilisateur alignés à droite
- Messages assistant alignés à gauche
- Affichage des métadonnées (heure, coût) au survol
- Support du markdown et mise en forme du code

### Indicateurs de statut

Des indicateurs visuels de statut sont utilisés :
- Point rouge 🔴 pour les alertes et notifications
- Icônes pour les actions communes (modifier, supprimer, etc.)
- Barres de progression pour les limites

## Mise en œuvre technique

### Frameworks et bibliothèques

Les interfaces utilisateur seront développées avec :
- **Vue.js 3** : Framework principal
- **PrimeVue** : Bibliothèque de composants UI
- **Chart.js** : Visualisations de données
- **Marked** : Rendu markdown
- **Highlight.js** : Colorisation syntaxique du code
- **Pinia** : Gestion de l'état

### Considérations de performance

Pour assurer des performances optimales sur Raspberry Pi :
- Chargement différé des composants non essentiels
- Virtualisation des listes longues
- Utilisation du SSR pour le rendu initial
- Optimisation des assets statiques

### Responsive design

L'application s'adapte aux différentes tailles d'écran :
- **Desktop** : Affichage complet avec barre latérale visible
- **Tablette** : Barre latérale rétractable
- **Mobile** : Navigation simplifiée avec menus déroulants

## Évolutions futures

Ces maquettes représentent la V1 et le début de la V2. Les évolutions futures pourront inclure :

1. Partage de conversations entre utilisateurs
2. Support pour les pièces jointes dans les conversations
3. Interface d'administration plus riche
4. Visualisations avancées pour l'analyse des coûts
5. Intégration d'un éditeur de texte enrichi

## Notes d'implémentation

Les éléments d'interface doivent être soigneusement documentés durant le développement pour faciliter la maintenance et l'évolution future de l'application. Les composants doivent être modulaires et réutilisables.
