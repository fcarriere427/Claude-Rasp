"""
Configuration pour les tests de l'API
"""
import os
from dotenv import load_dotenv

# Chemin du fichier .env (créer une copie de .env.test.example et la renommer en .env.test)
env_path = os.path.join(os.path.dirname(__file__), '.env.test')

# Charger les variables d'environnement depuis .env.test
load_dotenv(dotenv_path=env_path)

# Configuration de l'API
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api/v1')

# Utilisateurs de test
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'adminpassword')

# Utilisateur de test généré
TEST_USER_USERNAME = os.getenv('TEST_USER_USERNAME', 'testuser')
TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'testuser@example.com')
TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', 'securepassword123')
TEST_USER_NEW_PASSWORD = 'evenmoresecure456'
