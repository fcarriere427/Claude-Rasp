# Spécifications API
# Application Claude API sur Raspberry Pi

## Vue d'ensemble

Cette documentation détaille les endpoints API de l'application Claude API sur Raspberry Pi. L'API est organisée selon les principes RESTful, avec des routes pour l'authentification, les conversations, l'intégration MCP, et le monitoring.

Base URL: `http://localhost:8000` (développement) ou `https://claude-rasp.local/api` (production)

## Authentification

Tous les endpoints (à l'exception de `/auth/login` et `/auth/register`) nécessitent une authentification via un token JWT, passé dans le header HTTP `Authorization` sous la forme `Bearer {token}`.

### Endpoints d'authentification

#### `POST /api/v1/auth/login`

Authentifie un utilisateur et retourne un token JWT.

**Requête:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Réponse:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "is_active": "boolean",
    "is_admin": "boolean"
  }
}
```

**Codes de statut:**
- `200 OK`: Authentification réussie
- `401 Unauthorized`: Identifiants invalides

#### `POST /api/v1/auth/logout`

Déconnecte l'utilisateur courant (invalide le token).

**Réponse:**
```json
{
  "message": "Déconnexion réussie"
}
```

**Codes de statut:**
- `200 OK`: Déconnexion réussie
- `401 Unauthorized`: Token invalide

#### `POST /api/v1/auth/register` (admin uniquement en V1)

Crée un nouveau compte utilisateur.

**Requête:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "is_admin": "boolean" (optionnel, défaut: false)
}
```

**Réponse:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "created_at": "datetime"
}
```

**Codes de statut:**
- `201 Created`: Utilisateur créé avec succès
- `400 Bad Request`: Données invalides
- `409 Conflict`: Le nom d'utilisateur ou l'email existe déjà
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur

#### `GET /api/v1/auth/me`

Retourne les informations de l'utilisateur courant.

**Réponse:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "created_at": "datetime",
  "last_login": "datetime"
}
```

**Codes de statut:**
- `200 OK`: Informations récupérées avec succès
- `401 Unauthorized`: Token invalide

#### `PUT /api/v1/auth/password`

Change le mot de passe de l'utilisateur courant.

**Requête:**
```json
{
  "current_password": "string",
  "new_password": "string"
}
```

**Réponse:**
```json
{
  "message": "Mot de passe modifié avec succès"
}
```

**Codes de statut:**
- `200 OK`: Mot de passe modifié avec succès
- `400 Bad Request`: Mot de passe actuel invalide
- `401 Unauthorized`: Token invalide

## Conversations

### Gestion des conversations

#### `GET /api/v1/conversations`

Récupère la liste des conversations de l'utilisateur.

**Paramètres de requête:**
- `limit` (optionnel): Nombre maximum de conversations à retourner (défaut: 20)
- `offset` (optionnel): Décalage pour la pagination (défaut: 0)

**Réponse:**
```json
{
  "total": "integer",
  "items": [
    {
      "id": "integer",
      "title": "string",
      "created_at": "datetime",
      "updated_at": "datetime",
      "message_count": "integer",
      "last_message_preview": "string"
    }
  ]
}
```

**Codes de statut:**
- `200 OK`: Liste récupérée avec succès
- `401 Unauthorized`: Token invalide

#### `POST /api/v1/conversations`

Crée une nouvelle conversation.

**Requête:**
```json
{
  "title": "string"
}
```

**Réponse:**
```json
{
  "id": "integer",
  "title": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Codes de statut:**
- `201 Created`: Conversation créée avec succès
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Token invalide

#### `GET /api/v1/conversations/{id}`

Récupère les détails d'une conversation et ses messages.

**Réponse:**
```json
{
  "id": "integer",
  "title": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "messages": [
    {
      "id": "integer",
      "role": "string",
      "content": "string",
      "created_at": "datetime",
      "input_tokens": "integer",
      "output_tokens": "integer",
      "cost": "float"
    }
  ]
}
```

**Codes de statut:**
- `200 OK`: Conversation récupérée avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'est pas propriétaire de la conversation
- `404 Not Found`: Conversation non trouvée

#### `DELETE /api/v1/conversations/{id}`

Supprime une conversation.

**Réponse:**
```json
{
  "message": "Conversation supprimée avec succès"
}
```

**Codes de statut:**
- `200 OK`: Conversation supprimée avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'est pas propriétaire de la conversation
- `404 Not Found`: Conversation non trouvée

### Gestion des messages

#### `POST /api/v1/conversations/{id}/messages`

Ajoute un message à une conversation et obtient une réponse de Claude.

**Requête:**
```json
{
  "content": "string"
}
```

**Réponse:**
```json
{
  "id": "integer",
  "role": "assistant",
  "content": "string",
  "created_at": "datetime",
  "input_tokens": "integer",
  "output_tokens": "integer",
  "cost": "float"
}
```

**Codes de statut:**
- `201 Created`: Message ajouté avec succès
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'est pas propriétaire de la conversation
- `404 Not Found`: Conversation non trouvée
- `429 Too Many Requests`: Limite d'utilisation atteinte

#### `GET /api/v1/conversations/{id}/export`

Exporte une conversation au format Markdown.

**Paramètres de requête:**
- `format` (optionnel): Format d'export (`markdown` ou `pdf`, défaut: `markdown`)

**Réponse:**
- Pour format `markdown`: Contenu en texte brut avec le header `Content-Type: text/markdown`
- Pour format `pdf`: Fichier PDF avec le header `Content-Type: application/pdf`

**Codes de statut:**
- `200 OK`: Export réussi
- `400 Bad Request`: Format invalide
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'est pas propriétaire de la conversation
- `404 Not Found`: Conversation non trouvée

## Intégration MCP (Multi-Claude Process)

### Configuration MCP (V1)

#### `GET /api/v1/mcp/config`

Récupère la configuration MCP actuelle.

**Réponse:**
```json
{
  "version": "string",
  "tools": [
    {
      "name": "string",
      "display_name": "string",
      "description": "string",
      "enabled": "boolean",
      "parameters": [
        {
          "name": "string",
          "type": "string",
          "required": "boolean",
          "default": "any",
          "description": "string"
        }
      ]
    }
  ],
  "settings": {
    "log_requests": "boolean",
    "log_responses": "boolean",
    "timeout_seconds": "integer",
    "retry_count": "integer",
    "retry_delay_seconds": "integer"
  }
}
```

**Codes de statut:**
- `200 OK`: Configuration récupérée avec succès
- `401 Unauthorized`: Token invalide

#### `GET /api/v1/mcp/tools`

Récupère la liste des outils MCP disponibles.

**Réponse:**
```json
[
  {
    "name": "string",
    "display_name": "string",
    "description": "string",
    "enabled": "boolean"
  }
]
```

**Codes de statut:**
- `200 OK`: Liste récupérée avec succès
- `401 Unauthorized`: Token invalide

### Administration MCP (V2)

#### `GET /api/v1/mcp/servers`

Récupère la liste des serveurs MCP.

**Réponse:**
```json
[
  {
    "id": "integer",
    "name": "string",
    "url": "string",
    "enabled": "boolean",
    "status": "string",
    "last_check": "datetime"
  }
]
```

**Codes de statut:**
- `200 OK`: Liste récupérée avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur

#### `POST /api/v1/mcp/servers`

Ajoute un serveur MCP.

**Requête:**
```json
{
  "name": "string",
  "url": "string",
  "enabled": "boolean",
  "auth_token": "string" (optionnel)
}
```

**Réponse:**
```json
{
  "id": "integer",
  "name": "string",
  "url": "string",
  "enabled": "boolean",
  "status": "string",
  "last_check": "datetime"
}
```

**Codes de statut:**
- `201 Created`: Serveur ajouté avec succès
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur

#### `PUT /api/v1/mcp/servers/{id}`

Modifie un serveur MCP.

**Requête:**
```json
{
  "name": "string",
  "url": "string",
  "enabled": "boolean",
  "auth_token": "string" (optionnel)
}
```

**Réponse:**
```json
{
  "id": "integer",
  "name": "string",
  "url": "string",
  "enabled": "boolean",
  "status": "string",
  "last_check": "datetime"
}
```

**Codes de statut:**
- `200 OK`: Serveur modifié avec succès
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `404 Not Found`: Serveur non trouvé

#### `DELETE /api/v1/mcp/servers/{id}`

Supprime un serveur MCP.

**Réponse:**
```json
{
  "message": "Serveur supprimé avec succès"
}
```

**Codes de statut:**
- `200 OK`: Serveur supprimé avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `404 Not Found`: Serveur non trouvé

#### `GET /api/v1/mcp/servers/{id}/status`

Vérifie le statut d'un serveur MCP.

**Réponse:**
```json
{
  "id": "integer",
  "name": "string",
  "status": "string",
  "last_check": "datetime",
  "response_time": "float",
  "available_tools": [
    {
      "name": "string",
      "display_name": "string",
      "description": "string"
    }
  ]
}
```

**Codes de statut:**
- `200 OK`: Statut récupéré avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `404 Not Found`: Serveur non trouvé

## Monitoring

### Suivi d'utilisation

#### `GET /api/v1/monitor/usage/daily`

Récupère les données d'utilisation quotidienne.

**Paramètres de requête:**
- `start_date` (optionnel): Date de début au format YYYY-MM-DD (défaut: 7 jours avant la date actuelle)
- `end_date` (optionnel): Date de fin au format YYYY-MM-DD (défaut: date actuelle)

**Réponse:**
```json
[
  {
    "date": "date",
    "input_tokens": "integer",
    "output_tokens": "integer",
    "cost": "float"
  }
]
```

**Codes de statut:**
- `200 OK`: Données récupérées avec succès
- `400 Bad Request`: Paramètres de date invalides
- `401 Unauthorized`: Token invalide

#### `GET /api/v1/monitor/usage/monthly`

Récupère les données d'utilisation mensuelle.

**Paramètres de requête:**
- `year` (optionnel): Année (défaut: année courante)

**Réponse:**
```json
[
  {
    "month": "integer",
    "year": "integer",
    "input_tokens": "integer",
    "output_tokens": "integer",
    "cost": "float"
  }
]
```

**Codes de statut:**
- `200 OK`: Données récupérées avec succès
- `400 Bad Request`: Paramètres invalides
- `401 Unauthorized`: Token invalide

### Gestion des limites

#### `GET /api/v1/monitor/limits`

Récupère les limites définies pour l'utilisateur.

**Réponse:**
```json
{
  "daily_limit": "float",
  "monthly_limit": "float",
  "alert_threshold_70": "boolean",
  "alert_threshold_90": "boolean",
  "kill_switch_enabled": "boolean",
  "current_daily_usage": "float",
  "current_monthly_usage": "float",
  "daily_percentage": "float",
  "monthly_percentage": "float"
}
```

**Codes de statut:**
- `200 OK`: Limites récupérées avec succès
- `401 Unauthorized`: Token invalide

#### `PUT /api/v1/monitor/limits`

Modifie les limites de l'utilisateur.

**Requête:**
```json
{
  "daily_limit": "float",
  "monthly_limit": "float",
  "alert_threshold_70": "boolean",
  "alert_threshold_90": "boolean",
  "kill_switch_enabled": "boolean"
}
```

**Réponse:**
```json
{
  "daily_limit": "float",
  "monthly_limit": "float",
  "alert_threshold_70": "boolean",
  "alert_threshold_90": "boolean",
  "kill_switch_enabled": "boolean"
}
```

**Codes de statut:**
- `200 OK`: Limites modifiées avec succès
- `400 Bad Request`: Limites invalides
- `401 Unauthorized`: Token invalide

#### `GET /api/v1/monitor/status`

Récupère le statut global d'utilisation.

**Réponse:**
```json
{
  "status": "string",
  "daily_usage": {
    "limit": "float",
    "current": "float",
    "percentage": "float"
  },
  "monthly_usage": {
    "limit": "float",
    "current": "float",
    "percentage": "float"
  },
  "kill_switch_active": "boolean",
  "alerts": [
    {
      "type": "string",
      "message": "string",
      "triggered_at": "datetime"
    }
  ]
}
```

**Codes de statut:**
- `200 OK`: Statut récupéré avec succès
- `401 Unauthorized`: Token invalide

## Administration (V2)

### Gestion des utilisateurs

#### `GET /api/v1/admin/users`

Récupère la liste des utilisateurs (admin uniquement).

**Paramètres de requête:**
- `limit` (optionnel): Nombre maximum d'utilisateurs à retourner (défaut: 20)
- `offset` (optionnel): Décalage pour la pagination (défaut: 0)

**Réponse:**
```json
{
  "total": "integer",
  "items": [
    {
      "id": "integer",
      "username": "string",
      "email": "string",
      "is_active": "boolean",
      "is_admin": "boolean",
      "created_at": "datetime",
      "last_login": "datetime"
    }
  ]
}
```

**Codes de statut:**
- `200 OK`: Liste récupérée avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur

#### `POST /api/v1/admin/users`

Crée un nouvel utilisateur (admin uniquement).

**Requête:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "is_admin": "boolean",
  "is_active": "boolean"
}
```

**Réponse:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "created_at": "datetime"
}
```

**Codes de statut:**
- `201 Created`: Utilisateur créé avec succès
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `409 Conflict`: Le nom d'utilisateur ou l'email existe déjà

#### `PUT /api/v1/admin/users/{id}`

Modifie un utilisateur (admin uniquement).

**Requête:**
```json
{
  "username": "string",
  "email": "string",
  "is_admin": "boolean",
  "is_active": "boolean",
  "password": "string" (optionnel)
}
```

**Réponse:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "created_at": "datetime",
  "last_login": "datetime"
}
```

**Codes de statut:**
- `200 OK`: Utilisateur modifié avec succès
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `404 Not Found`: Utilisateur non trouvé
- `409 Conflict`: Le nom d'utilisateur ou l'email existe déjà

#### `DELETE /api/v1/admin/users/{id}`

Supprime un utilisateur (admin uniquement).

**Réponse:**
```json
{
  "message": "Utilisateur supprimé avec succès"
}
```

**Codes de statut:**
- `200 OK`: Utilisateur supprimé avec succès
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `404 Not Found`: Utilisateur non trouvé

#### `PUT /api/v1/admin/users/{id}/limits`

Définit les limites d'un utilisateur (admin uniquement).

**Requête:**
```json
{
  "daily_limit": "float",
  "monthly_limit": "float",
  "alert_threshold_70": "boolean",
  "alert_threshold_90": "boolean",
  "kill_switch_enabled": "boolean"
}
```

**Réponse:**
```json
{
  "user_id": "integer",
  "daily_limit": "float",
  "monthly_limit": "float",
  "alert_threshold_70": "boolean",
  "alert_threshold_90": "boolean",
  "kill_switch_enabled": "boolean"
}
```

**Codes de statut:**
- `200 OK`: Limites définies avec succès
- `400 Bad Request`: Limites invalides
- `401 Unauthorized`: Token invalide
- `403 Forbidden`: L'utilisateur n'a pas les droits d'administrateur
- `404 Not Found`: Utilisateur non trouvé

## Versions et compatibilité

Cette API est versionnée via le préfixe de chemin (`/api/v1/`). Les futures versions utiliseront des préfixes différents (ex: `/api/v2/`) pour assurer la compatibilité des applications existantes.
