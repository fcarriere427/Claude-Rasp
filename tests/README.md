## Configuration du backend pour les tests

Pour que les tests fonctionnent correctement, assurez-vous que votre backend expose les endpoints de test nécessaires. Ces endpoints sont automatiquement activés lorsque la variable d'environnement `ENVIRONMENT` n'est pas définie à "production".

Important : Dans l'environnement de test, le backend expose des endpoints spéciaux pour :
1. Créer le premier utilisateur admin (`/test/create-first-user`)  
2. Réinitialiser la base de données (`/test/reset-database`)

Ces endpoints ne sont pas disponibles en production.

# Tests pour l'application Claude API sur Raspberry Pi

Ce répertoire contient les tests pour l'application Claude API.

## Structure

- `api/` - Tests des endpoints API
- `config.py` - Configuration pour les tests
- `run_api_tests.py` - Script pour exécuter tous les tests API

## Installation des dépendances

```bash
pip install -r requirements-test.txt
```

## Configuration

1. Copiez le fichier `.env.test.example` vers `.env.test`
2. Modifiez les valeurs dans `.env.test` selon votre environnement

```bash
cp .env.test.example .env.test
```

## Exécution des tests

### Tous les tests API

```bash
python run_api_tests.py
```

### Tests spécifiques

Vous pouvez exécuter des tests spécifiques directement :

```bash
# Test de l'authentification
python -m tests.api.test_auth
```

## Ajout de nouveaux tests

Pour ajouter de nouveaux tests API :

1. Créez un nouveau fichier dans le répertoire `api/` avec le préfixe `test_`
2. Implémentez vos fonctions de test avec le préfixe `test_`
3. Utilisez la classe `ApiClient` pour interagir avec l'API
4. Vos tests seront automatiquement détectés et exécutés par `run_api_tests.py`

## Structure recommandée pour les tests

```python
from tests.api.api_client import ApiClient
from tests.config import URL, USERNAME, PASSWORD

def test_some_feature():
    # Setup
    client = ApiClient()
    client.login(USERNAME, PASSWORD)
    
    # Test
    response = client.some_api_call()
    
    # Assertions
    assert response.status_code == 200
    
    # Cleanup if needed
    
    return response.status_code == 200
```
