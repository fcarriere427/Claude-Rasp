# Modèles de données
# Application Claude API sur Raspberry Pi

## Vue d'ensemble

Ce document définit les modèles de données utilisés par l'application Claude API sur Raspberry Pi. Les modèles sont implémentés avec SQLAlchemy pour le backend et représentent la structure de la base de données.

## Modèles principaux

### Utilisateur (User)

**Objectif:** Représente un utilisateur de l'application avec ses informations d'authentification et permissions.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `username` (String, unique): Nom d'utilisateur
- `email` (String, unique): Adresse email
- `hashed_password` (String): Mot de passe haché (bcrypt)
- `is_active` (Boolean, default=True): État du compte
- `is_admin` (Boolean, default=False): Droits administrateur
- `created_at` (DateTime): Date de création du compte
- `last_login` (DateTime, nullable): Dernière connexion

**Relations:**
- `conversations` (one-to-many): Conversations créées par l'utilisateur
- `usage_records` (one-to-many): Enregistrements d'utilisation
- `limits` (one-to-one): Limites d'utilisation

**Méthodes:**
- `verify_password(plain_password)`: Vérifie si le mot de passe fourni correspond
- `set_password(plain_password)`: Définit un nouveau mot de passe

**Exemple d'implémentation:**
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relations
    conversations = relationship("Conversation", back_populates="user")
    usage_records = relationship("UsageRecord", back_populates="user")
    limits = relationship("UserLimit", back_populates="user", uselist=False)
    
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)
    
    def set_password(self, plain_password):
        self.hashed_password = pwd_context.hash(plain_password)
```

### Conversation

**Objectif:** Représente une conversation entre un utilisateur et Claude.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `title` (String): Titre de la conversation
- `user_id` (Integer, FK): Identifiant de l'utilisateur propriétaire
- `created_at` (DateTime): Date de création
- `updated_at` (DateTime): Date de dernière mise à jour

**Relations:**
- `user` (many-to-one): Utilisateur propriétaire
- `messages` (one-to-many): Messages dans la conversation

**Exemple d'implémentation:**
```python
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", 
                            order_by="Message.created_at")
```

### Message

**Objectif:** Représente un message individuel dans une conversation.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `conversation_id` (Integer, FK): Identifiant de la conversation
- `role` (String): Rôle de l'émetteur ('user' ou 'assistant')
- `content` (Text): Contenu du message
- `created_at` (DateTime): Date de création
- `input_tokens` (Integer, nullable): Nombre de tokens en entrée (pour le calcul de coût)
- `output_tokens` (Integer, nullable): Nombre de tokens en sortie (pour le calcul de coût)
- `cost` (Float, nullable): Coût estimé du message

**Relations:**
- `conversation` (many-to-one): Conversation contenant le message

**Exemple d'implémentation:**
```python
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # 'user' ou 'assistant'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Métriques
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    
    # Relations
    conversation = relationship("Conversation", back_populates="messages")
```

### Enregistrement d'utilisation (UsageRecord)

**Objectif:** Agrège les statistiques d'utilisation par jour et par utilisateur.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `user_id` (Integer, FK): Identifiant de l'utilisateur
- `date` (Date): Date du jour
- `input_tokens` (Integer, default=0): Nombre total de tokens en entrée
- `output_tokens` (Integer, default=0): Nombre total de tokens en sortie
- `cost` (Float, default=0.0): Coût total estimé

**Relations:**
- `user` (many-to-one): Utilisateur concerné

**Exemple d'implémentation:**
```python
class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    
    # Relations
    user = relationship("User", back_populates="usage_records")
    
    # Contrainte d'unicité par utilisateur et par jour
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
```

### Limites utilisateur (UserLimit)

**Objectif:** Définit les limites d'utilisation par utilisateur.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `user_id` (Integer, FK): Identifiant de l'utilisateur
- `daily_limit` (Float): Limite quotidienne (en euros)
- `monthly_limit` (Float): Limite mensuelle (en euros)
- `alert_threshold_70` (Boolean, default=True): Alerte à 70% de la limite
- `alert_threshold_90` (Boolean, default=True): Alerte à 90% de la limite
- `kill_switch_enabled` (Boolean, default=True): Blocage à l'atteinte de la limite

**Relations:**
- `user` (one-to-one): Utilisateur concerné

**Exemple d'implémentation:**
```python
class UserLimit(Base):
    __tablename__ = "user_limits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    daily_limit = Column(Float)  # en euros
    monthly_limit = Column(Float)  # en euros
    alert_threshold_70 = Column(Boolean, default=True)
    alert_threshold_90 = Column(Boolean, default=True)
    kill_switch_enabled = Column(Boolean, default=True)
    
    # Relations
    user = relationship("User", back_populates="limits")
```

### Serveur MCP (MCPServer) - V2

**Objectif:** Stocke les informations sur les serveurs MCP externes.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `name` (String): Nom du serveur
- `url` (String): URL du serveur
- `auth_token` (String, nullable): Token d'authentification (si nécessaire)
- `enabled` (Boolean, default=True): État d'activation
- `last_check` (DateTime, nullable): Dernière vérification de statut
- `status` (String, nullable): Statut du serveur ('online', 'offline', 'error')

**Exemple d'implémentation:**
```python
class MCPServer(Base):
    __tablename__ = "mcp_servers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    auth_token = Column(String, nullable=True)
    enabled = Column(Boolean, default=True)
    last_check = Column(DateTime, nullable=True)
    status = Column(String, nullable=True)
```

### Alerte (Alert)

**Objectif:** Enregistre les alertes générées par le système.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `user_id` (Integer, FK): Identifiant de l'utilisateur concerné
- `type` (String): Type d'alerte ('daily_70', 'daily_90', 'monthly_70', 'monthly_90', 'kill_switch')
- `message` (String): Message de l'alerte
- `created_at` (DateTime): Date de création
- `acknowledged` (Boolean, default=False): Si l'alerte a été reconnue

**Relations:**
- `user` (many-to-one): Utilisateur concerné

**Exemple d'implémentation:**
```python
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)
    
    # Relations
    user = relationship("User")
```

## Modèles auxiliaires

### Tarification (Pricing)

**Objectif:** Stocke les informations de tarification pour différents modèles Claude.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `model` (String): Nom du modèle ('claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', etc.)
- `input_price` (Float): Prix par million de tokens en entrée
- `output_price` (Float): Prix par million de tokens en sortie
- `currency` (String, default='EUR'): Devise
- `updated_at` (DateTime): Date de dernière mise à jour

**Exemple d'implémentation:**
```python
class Pricing(Base):
    __tablename__ = "pricing"
    
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True)
    input_price = Column(Float)  # Prix par million de tokens
    output_price = Column(Float)  # Prix par million de tokens
    currency = Column(String, default="EUR")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Configuration système (SystemConfig)

**Objectif:** Stocke les configurations globales du système.

**Attributs:**
- `id` (Integer, PK): Identifiant unique
- `key` (String, unique): Clé de configuration
- `value` (String): Valeur de configuration
- `description` (String, nullable): Description de la configuration
- `updated_at` (DateTime): Date de dernière mise à jour

**Exemple d'implémentation:**
```python
class SystemConfig(Base):
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)
    description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## Relations entre les modèles

![Diagramme des relations](../docs/images/data_model_relationships.png)

## Schéma de migration

Les migrations de la base de données sont gérées avec Alembic. Voici un exemple de migration initiale pour créer les tables principales :

```python
"""initial migration

Revision ID: 01a1b2c3d4e5
Revises: 
Create Date: 2025-04-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '01a1b2c3d4e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Création de la table users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    
    # Création de la table user_limits
    op.create_table('user_limits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('daily_limit', sa.Float(), nullable=False),
        sa.Column('monthly_limit', sa.Float(), nullable=False),
        sa.Column('alert_threshold_70', sa.Boolean(), nullable=False, default=True),
        sa.Column('alert_threshold_90', sa.Boolean(), nullable=False, default=True),
        sa.Column('kill_switch_enabled', sa.Boolean(), nullable=False, default=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_limits_id'), 'user_limits', ['id'], unique=False)
    
    # Création de la table conversations
    op.create_table('conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)
    
    # Création de la table messages
    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('input_tokens', sa.Integer(), nullable=True),
        sa.Column('output_tokens', sa.Integer(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    
    # Création de la table usage_records
    op.create_table('usage_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('input_tokens', sa.Integer(), nullable=False, default=0),
        sa.Column('output_tokens', sa.Integer(), nullable=False, default=0),
        sa.Column('cost', sa.Float(), nullable=False, default=0.0),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'date', name='unique_user_date')
    )
    op.create_index(op.f('ix_usage_records_id'), 'usage_records', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_usage_records_id'), table_name='usage_records')
    op.drop_table('usage_records')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_conversations_id'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_user_limits_id'), table_name='user_limits')
    op.drop_table('user_limits')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
```

## Règles de validation

Les schémas Pydantic sont utilisés pour valider les données en entrée et en sortie de l'API. Voici quelques exemples des schémas qui correspondraient aux modèles de données définis ci-dessus :

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date

# Schémas utilisateur
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schémas conversation
class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

class ConversationInDB(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schémas message
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageInDB(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost: Optional[float] = None

    class Config:
        orm_mode = True

# Schémas limite utilisateur
class UserLimitBase(BaseModel):
    daily_limit: float
    monthly_limit: float
    alert_threshold_70: bool = True
    alert_threshold_90: bool = True
    kill_switch_enabled: bool = True

class UserLimitCreate(UserLimitBase):
    user_id: int

class UserLimitUpdate(BaseModel):
    daily_limit: Optional[float] = None
    monthly_limit: Optional[float] = None
    alert_threshold_70: Optional[bool] = None
    alert_threshold_90: Optional[bool] = None
    kill_switch_enabled: Optional[bool] = None

class UserLimitInDB(UserLimitBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Schémas utilisation
class UsageRecordCreate(BaseModel):
    user_id: int
    date: date
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0

class UsageRecordInDB(UsageRecordCreate):
    id: int

    class Config:
        orm_mode = True

# Schémas statistiques
class DailyUsage(BaseModel):
    date: date
    input_tokens: int
    output_tokens: int
    cost: float

class MonthlyUsage(BaseModel):
    month: int
    year: int
    input_tokens: int
    output_tokens: int
    cost: float
```

## Notes d'implémentation

1. **Authentification**: L'authentification est gérée via des tokens JWT. Le modèle User est responsable de la vérification des mots de passe.

2. **Coûts et limites**: Les coûts sont calculés en temps réel lors de l'ajout des messages, puis agrégés dans les enregistrements d'utilisation (UsageRecord). Les limites (UserLimit) sont vérifiées avant chaque appel à l'API Claude.

3. **Stockage des tokens d'API**: Les tokens d'API (Claude, Brave, etc.) ne sont pas stockés dans la base de données mais dans des variables d'environnement pour des raisons de sécurité.

4. **Scalabilité**: Pour la V1, SQLite est suffisant étant donné la charge attendue. Pour la V2 avec support multi-utilisateurs, une migration vers PostgreSQL pourrait être nécessaire pour de meilleures performances et une scalabilité accrue.

5. **Indexation**: Des index sont créés sur les champs fréquemment utilisés dans les requêtes (IDs, noms d'utilisateurs, dates) pour optimiser les performances des requêtes.
