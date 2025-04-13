#!/usr/bin/env python3
"""
Test simplifié d'authentification - indépendant des autres modules
"""
import json
import time
import random
import string
import os
import sys
import requests
from datetime import datetime

# Couleurs pour le terminal (fonctionne même sans colorama)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Configuration (hardcodée pour éviter les problèmes d'import)
API_BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpassword"
TEST_USER_USERNAME = "testuser"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "securepassword123"

# Fonctions d'affichage
def print_header(text):
    print(f"\n{Colors.CYAN}{'='*10} {text} {'='*10}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def print_response(response):
    print(f"Status: {response.status_code}")
    if hasattr(response, 'json'):
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            print(f"Response (text): {response.text}")
    else:
        print(f"Response (text): {response.text}")

def random_suffix():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Client API simplifié
class SimpleApiClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.token = None
        self.user_data = None
    
    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def login(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.user_data = data.get("user")
        return response
    
    def logout(self):
        response = requests.post(
            f"{self.base_url}/auth/logout",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            self.token = None
            self.user_data = None
        return response
    
    def register_user(self, username, email, password, is_active=True, is_admin=False):
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "is_active": is_active,
            "is_admin": is_admin
        }
        return requests.post(
            f"{self.base_url}/auth/register",
            json=payload,
            headers=self.get_headers()
        )
    
    def get_me(self):
        return requests.get(
            f"{self.base_url}/auth/me",
            headers=self.get_headers()
        )
    
    def change_password(self, current_password, new_password):
        payload = {
            "current_password": current_password,
            "new_password": new_password
        }
        return requests.put(
            f"{self.base_url}/auth/password",
            json=payload,
            headers=self.get_headers()
        )

def run_auth_test():
    """Test complet du flux d'authentification"""
    # Check if API is accessible
    print_header("VERIFICATION DE L'ACCÈS À L'API")
    
    try:
        # Get API base without /api/v1
        api_base = API_BASE_URL
        if api_base.endswith('/api/v1'):
            api_base = api_base[:-7]
        
        response = requests.get(f"{api_base}/health")
        if response.status_code != 200:
            print_error(f"L'API n'est pas accessible: {response.status_code}")
            return False
        print_success("API accessible")
    except Exception as e:
        print_error(f"Erreur lors de l'accès à l'API: {str(e)}")
        return False
    
    # Variables pour stocker les données de test
    api_client = SimpleApiClient()
    results = {}
    test_username = f"{TEST_USER_USERNAME}_{random_suffix()}"
    test_email = f"{random_suffix()}_{TEST_USER_EMAIL}"
    admin_password = ADMIN_PASSWORD
    
    # Tentative de création du premier utilisateur admin
    try:
        print_header("CRÉATION DU PREMIER UTILISATEUR ADMIN")
        if api_base.endswith('/api/v1'):
            api_base = api_base[:-7]
        
        init_user_url = f"{api_base}/test/create-first-user"
        response = requests.post(
            init_user_url,
            json={
                "username": ADMIN_USERNAME,
                "email": f"{ADMIN_USERNAME}@example.com",
                "password": admin_password,
                "is_admin": True
            }
        )
        
        print_response(response)
        
        if response.status_code in [200, 201]:
            print_success("Premier utilisateur (admin) créé avec succès")
        else:
            print_info("Impossible de créer le premier utilisateur via l'API de test. On suppose qu'il existe déjà.")
    except Exception as e:
        print_info(f"Erreur lors de la création du premier utilisateur: {str(e)}")
        print_info("On suppose que l'admin existe déjà")
    
    # Tests à exécuter
    tests = [
        # 1. Connexion en tant qu'admin
        {
            'name': 'login_admin',
            'func': lambda: api_client.login(ADMIN_USERNAME, admin_password),
            'expected_status': 200,
            'message': "Connexion en tant qu'admin"
        },
        # 2. Création d'un utilisateur de test
        {
            'name': 'create_test_user',
            'func': lambda: api_client.register_user(
                test_username, test_email, TEST_USER_PASSWORD
            ),
            'expected_status': 201,
            'message': "Création d'un utilisateur de test"
        },
        # 3. Déconnexion de l'admin
        {
            'name': 'logout_admin',
            'func': lambda: api_client.logout(),
            'expected_status': 200,
            'message': "Déconnexion de l'admin"
        },
        # 4. Connexion avec l'utilisateur de test
        {
            'name': 'login_test_user',
            'func': lambda: api_client.login(test_username, TEST_USER_PASSWORD),
            'expected_status': 200,
            'message': "Connexion avec l'utilisateur de test"
        },
        # 5. Récupération des informations utilisateur
        {
            'name': 'get_me',
            'func': lambda: api_client.get_me(),
            'expected_status': 200,
            'message': "Récupération des informations utilisateur"
        },
        # 6. Changement de mot de passe
        {
            'name': 'change_password',
            'func': lambda: api_client.change_password(
                TEST_USER_PASSWORD, "evenmoresecure456"
            ),
            'expected_status': 200,
            'message': "Changement de mot de passe"
        },
        # 7. Échec de connexion avec l'ancien mot de passe
        {
            'name': 'login_with_old_password',
            'func': lambda: SimpleApiClient().login(test_username, TEST_USER_PASSWORD),
            'expected_status': 401,
            'message': "Échec de connexion avec l'ancien mot de passe"
        },
        # 8. Connexion avec le nouveau mot de passe
        {
            'name': 'login_with_new_password',
            'func': lambda: SimpleApiClient().login(test_username, "evenmoresecure456"),
            'expected_status': 200,
            'message': "Connexion avec le nouveau mot de passe"
        },
        # 9. Déconnexion
        {
            'name': 'logout',
            'func': lambda: api_client.logout(),
            'expected_status': 200,
            'message': "Déconnexion"
        },
        # 10. Tentative d'accès après déconnexion
        {
            'name': 'access_after_logout',
            'func': lambda: api_client.get_me(),
            'expected_status': 401,
            'message': "Tentative d'accès après déconnexion"
        }
    ]
    
    # Exécuter les tests
    print_header("TESTS D'AUTHENTIFICATION")
    
    for test in tests:
        print_header(test['message'])
        
        try:
            response = test['func']()
            status_match = response.status_code == test['expected_status']
            
            print_response(response)
            
            if status_match:
                print_success(f"Test '{test['name']}' réussi")
                results[test['name']] = True
            else:
                print_error(
                    f"Test '{test['name']}' échoué. "
                    f"Statut attendu: {test['expected_status']}, "
                    f"Obtenu: {response.status_code}"
                )
                results[test['name']] = False
        except Exception as e:
            print_error(f"Exception lors du test '{test['name']}': {str(e)}")
            results[test['name']] = False
        
        # Petite pause entre les tests
        time.sleep(0.5)
    
    # Afficher les résultats
    print_header("RÉSULTATS DES TESTS")
    
    success_count = sum(1 for result in results.values() if result)
    for test_name, result in results.items():
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {success_count}/{len(results)} tests réussis")
    
    return success_count == len(results)

if __name__ == "__main__":
    print_header(f"DÉBUT DES TESTS D'AUTHENTIFICATION - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    success = run_auth_test()
    print_header(f"FIN DES TESTS - {'SUCCÈS' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)
