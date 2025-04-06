# Flux d'authentification
# Application Claude API sur Raspberry Pi

## Vue d'ensemble

Ce document détaille le flux d'authentification implémenté dans l'application Claude API sur Raspberry Pi. L'authentification est basée sur des tokens JWT (JSON Web Tokens) pour une sécurité robuste et une expérience utilisateur fluide.

## Fonctionnement général

L'authentification suit un modèle standard basé sur des tokens :
1. L'utilisateur s'authentifie avec ses identifiants (nom d'utilisateur/mot de passe)
2. Le serveur vérifie les identifiants et génère un token JWT signé
3. Ce token est renvoyé au client qui le stocke (localStorage)
4. Pour les requêtes ultérieures, le client inclut ce token dans le header HTTP
5. Le serveur vérifie la validité du token avant de traiter la requête

## Diagramme de séquence

```
┌──────────┐                                 ┌──────────┐                            ┌──────────┐
│          │                                 │          │                            │          │
│  Client  │                                 │ Backend  │                            │  Database│
│          │                                 │          │                            │          │
└────┬─────┘                                 └────┬─────┘                            └────┬─────┘
     │                                            │                                       │
     │ POST /api/v1/auth/login                    │                                       │
     │ {username, password}                       │                                       │
     │ ──────────────────────────────────────────>│                                       │
     │                                            │                                       │
     │                                            │ SELECT user                           │
     │                                            │ ─────────────────────────────────────>│
     │                                            │                                       │
     │                                            │ User record                           │
     │                                            │ <─────────────────────────────────────│
     │                                            │                                       │
     │                                            │ Verify password                       │
     │                                            │ Create JWT                            │
     │                                            │                                       │
     │ 200 OK                                     │                                       │
     │ {token, user}                              │                                       │
     │ <──────────────────────────────────────────│                                       │
     │                                            │                                       │
     │ Store token                                │                                       │
     │                                            │                                       │
     │ GET /api/v1/conversations                  │                                       │
     │ Authorization: Bearer {token}              │                                       │
     │ ──────────────────────────────────────────>│                                       │
     │                                            │ Verify token                          │
     │                                            │ Extract user_id                       │
     │                                            │                                       │
     │                                            │ SELECT conversations                  │
     │                                            │ WHERE user_id = {user_id}             │
     │                                            │ ─────────────────────────────────────>│
     │                                            │                                       │
     │                                            │ Conversations                         │
     │                                            │ <─────────────────────────────────────│
     │                                            │                                       │
     │ 200 OK                                     │                                       │
     │ {conversations}                            │                                       │
     │ <──────────────────────────────────────────│                                       │
     │                                            │                                       │
```

## Implémentation technique

### 1. Hachage des mots de passe

Les mots de passe ne sont jamais stockés en clair dans la base de données. Ils sont hachés avec l'algorithme bcrypt qui inclut automatiquement un sel (salt) pour résister aux attaques par dictionnaire et par force brute.

```python
from passlib.context import CryptContext

# Configuration du contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Vérification d'un mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Hachage d'un mot de passe
def get_password_hash(password):
    return pwd_context.hash(password)
```

### 2. Génération des tokens JWT

Les tokens JWT sont générés avec la bibliothèque python-jose. Ils contiennent le payload suivant :
- `sub` (subject): Identifiant de l'utilisateur
- `exp` (expiration): Date d'expiration du token
- `iat` (issued at): Date de création du token
- `type`: Type de token (access_token)

```python
from jose import jwt
from datetime import datetime, timedelta

# Configuration des paramètres JWT
SECRET_KEY = "your-secret-key-here"  # À stocker en variable d'environnement
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 heure

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access_token"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### 3. Vérification des tokens

Chaque requête API (sauf login et register) nécessite un token valide dans l'en-tête HTTP `Authorization`. FastAPI permet de le gérer efficacement avec des dépendances.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configuration du schéma OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Fonction pour récupérer l'utilisateur actuel
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Décodage du token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Récupération de l'utilisateur dans la DB
        user = db.users.get(user_id)
        if user is None:
            raise credentials_exception
        
        # Vérification que le compte est actif
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        return user
    except JWTError:
        raise credentials_exception
```

### 4. Endpoints d'authentification

#### 4.1 Login

```python
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Recherche de l'utilisateur
    user = db.users.get_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Vérification du mot de passe
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Mise à jour de la date de dernière connexion
    user.last_login = datetime.utcnow()
    db.users.update(user)
    
    # Création du token d'accès
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    }
```

#### 4.2 Logout

Le logout côté client consiste simplement à supprimer le token stocké. Côté serveur, on peut maintenir une liste noire des tokens révoqués (pour la V2).

```python
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    # Dans la V1, le logout est géré côté client
    # Dans la V2, on pourrait ajouter le token à une liste noire
    return {"message": "Déconnexion réussie"}
```

#### 4.3 Register (admin uniquement en V1)

```python
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, current_user: User = Depends(get_current_user)):
    # Vérification des droits d'admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    
    # Vérification de l'unicité du nom d'utilisateur et de l'email
    if db.users.get_by_username(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    
    if db.users.get_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Création de l'utilisateur
    hashed_password = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        is_active=user_create.is_active,
        is_admin=user_create.is_admin,
        created_at=datetime.utcnow()
    )
    
    # Sauvegarde en base
    db_user = db.users.create(user)
    
    # Création des limites par défaut
    user_limit = UserLimit(
        user_id=db_user.id,
        daily_limit=config.DEFAULT_DAILY_LIMIT,
        monthly_limit=config.DEFAULT_MONTHLY_LIMIT
    )
    db.user_limits.create(user_limit)
    
    return db_user
```

## Implémentation côté frontend

### 1. Stockage des tokens

Le token est stocké dans le localStorage du navigateur pour persister entre les sessions.

```javascript
// Fonction de login
async function login(username, password) {
  try {
    const response = await axios.post('/api/v1/auth/login', {
      username,
      password
    });
    
    // Stockage du token dans localStorage
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Authentication failed');
  }
}

// Fonction de logout
function logout() {
  // Suppression du token
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  
  // Redirection vers la page de login
  window.location.href = '/login';
}
```

### 2. Interception des requêtes

Axios permet d'intercepter toutes les requêtes pour ajouter automatiquement le token d'authentification :

```javascript
// Configuration de l'intercepteur Axios
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Gestion des erreurs d'authentification
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    // Si erreur 401, redirection vers la page de login
    if (error.response?.status === 401) {
      logout();
    }
    return Promise.reject(error);
  }
);
```

## Considérations de sécurité

1. **Protection CSRF** : Les tokens JWT sont envoyés via le header `Authorization` plutôt que dans un cookie, ce qui protège naturellement contre les attaques CSRF.

2. **Expiration des tokens** : Les tokens ont une durée de validité limitée (1 heure par défaut) pour réduire le risque en cas de vol.

3. **Stockage sécurisé** : La clé secrète utilisée pour signer les tokens est stockée dans une variable d'environnement, pas dans le code.

4. **Tentatives multiples** : Pour la V2, un mécanisme de rate-limiting sera implémenté pour bloquer les tentatives de force brute.

5. **HTTPS obligatoire** : Toutes les communications sont cryptées via HTTPS pour protéger les tokens en transit.

## Intégration Google Auth (V2)

Dans la V2, l'authentification Google sera ajoutée comme méthode alternative :

1. L'utilisateur clique sur "Se connecter avec Google"
2. Il est redirigé vers l'écran de consentement Google
3. Après authentification, Google renvoie un code d'autorisation
4. Le backend échange ce code contre un token d'accès Google
5. Le backend extrait les informations utilisateur (email, nom, etc.)
6. Si l'utilisateur existe, il est connecté ; sinon, un nouveau compte est créé
7. Un token JWT standard est généré et renvoyé au client

L'implémentation technique utilisera la bibliothèque `authlib` pour Flask/FastAPI.

## Sécurité en production

Pour le déploiement en production, les pratiques suivantes sont appliquées :

1. **Rotation des clés** : La clé secrète JWT est régulièrement changée.
2. **Validation stricte** : Tous les paramètres d'entrée sont validés avec Pydantic.
3. **En-têtes de sécurité** : Les en-têtes HTTP de sécurité sont configurés dans Nginx.
4. **Journalisation** : Toutes les tentatives de connexion sont journalisées.
5. **Surveillance** : Un système de détection d'anomalies est en place pour les V2.
