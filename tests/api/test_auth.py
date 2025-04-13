"""
Tests pour les endpoints d'authentification
"""
import json
import time
import random
import string
from colorama import Fore, Style, init

from tests.api.api_client import ApiClient
from tests.config import (
    ADMIN_USERNAME, ADMIN_PASSWORD,
    TEST_USER_USERNAME, TEST_USER_EMAIL, TEST_USER_PASSWORD
)

# Initialiser colorama pour les couleurs dans le terminal
init(autoreset=True)

def print_header(text):
    """Afficher un en-tête de test"""
    print(f"\n{Fore.CYAN}{'='*10} {text} {'='*10}{Style.RESET_ALL}")

def print_success(text):
    """Afficher un message de succès"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Afficher un message d'erreur"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Afficher un message d'information"""
    print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

def print_response(response):
    """Afficher les détails d'une réponse"""
    print(f"Status: {response.status_code}")
    if hasattr(response, 'json'):
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            print(f"Response (text): {response.text}")
    else:
        print(f"Response (text): {response.text}")

def random_suffix():
    """Générer un suffixe aléatoire pour les noms de test"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def test_auth_flow():
    """Test complet du flux d'authentification"""
    # Utiliser notre client API
    api_client = ApiClient()
    admin_client = ApiClient()
    
    # Variables pour stocker les données de test
    results = {}
    test_username = f"{TEST_USER_USERNAME}_{random_suffix()}"
    test_email = f"{random_suffix()}_{TEST_USER_EMAIL}"
    
    # Tests à exécuter
    tests = [
        # 1. Connexion en tant qu'admin
        {
            'name': 'login_admin',
            'func': lambda: admin_client.login(ADMIN_USERNAME, ADMIN_PASSWORD),
            'expected_status': 200,
            'message': "Connexion en tant qu'admin"
        },
        # 2. Création d'un utilisateur de test
        {
            'name': 'create_test_user',
            'func': lambda: admin_client.register_user(
                test_username, test_email, TEST_USER_PASSWORD
            ),
            'expected_status': 201,
            'message': "Création d'un utilisateur de test"
        },
        # 3. Connexion avec l'utilisateur de test
        {
            'name': 'login_test_user',
            'func': lambda: api_client.login(test_username, TEST_USER_PASSWORD),
            'expected_status': 200,
            'message': "Connexion avec l'utilisateur de test"
        },
        # 4. Récupération des informations utilisateur
        {
            'name': 'get_me',
            'func': lambda: api_client.get_me(),
            'expected_status': 200,
            'message': "Récupération des informations utilisateur"
        },
        # 5. Changement de mot de passe
        {
            'name': 'change_password',
            'func': lambda: api_client.change_password(
                TEST_USER_PASSWORD, "evenmoresecure456"
            ),
            'expected_status': 200,
            'message': "Changement de mot de passe"
        },
        # 6. Échec de connexion avec l'ancien mot de passe
        {
            'name': 'login_with_old_password',
            'func': lambda: ApiClient().login(test_username, TEST_USER_PASSWORD),
            'expected_status': 401,
            'message': "Échec de connexion avec l'ancien mot de passe"
        },
        # 7. Connexion avec le nouveau mot de passe
        {
            'name': 'login_with_new_password',
            'func': lambda: ApiClient().login(test_username, "evenmoresecure456"),
            'expected_status': 200,
            'message': "Connexion avec le nouveau mot de passe"
        },
        # 8. Déconnexion
        {
            'name': 'logout',
            'func': lambda: api_client.logout(),
            'expected_status': 200,
            'message': "Déconnexion"
        },
        # 9. Tentative d'accès après déconnexion
        {
            'name': 'access_after_logout',
            'func': lambda: api_client.get_me(),
            'expected_status': 401,
            'message': "Tentative d'accès après déconnexion"
        },
        # 10. Test d'inscription avec un utilisateur non admin
        {
            'name': 'register_as_non_admin',
            'func': lambda: api_client.register_user(
                f"another_{random_suffix()}", 
                f"another_{random_suffix()}@example.com", 
                "password123"
            ),
            'expected_status': 401,
            'message': "Tentative d'inscription en tant que non-admin"
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
    
    print(f"\nTotal: {success_count}/{len(tests)} tests réussis")
    
    return success_count == len(tests)

if __name__ == "__main__":
    test_auth_flow()
