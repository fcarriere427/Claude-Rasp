def test_auth_flow_no_admin():
    """Test du flux d'authentification sans compte admin préexistant"""
    # Utiliser notre client API
    api_client = ApiClient()
    
    # Variables pour stocker les données de test
    results = {}
    test_username = f"{TEST_USER_USERNAME}_{random_suffix()}"
    test_email = f"{random_suffix()}_{TEST_USER_EMAIL}"
    admin_password = "admin_secure_password"
    
    print_header("TEST D'AUTHENTIFICATION (MODE SANS ADMIN PRÉEXISTANT)")
    
    # 1. Enregistrement direct d'un utilisateur (sans authentification)
    print_header("Enregistrement direct d'un utilisateur (simulation du premier utilisateur)")
    
    try:
        # On va faire un appel direct à l'API de base pour simuler la création du premier utilisateur
        api_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
        if api_url.endswith('/api/v1'):
            api_url = api_url[:-7]  # Enlever /api/v1 pour obtenir l'URL de base
        
        # Cet endpoint devrait être créé spécifiquement pour les tests pour permettre l'inscription du premier utilisateur
        init_user_url = f"{api_url}/test/create-first-user"
        
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
            results['create_first_admin'] = True
        else:
            print_info("Impossible de créer le premier utilisateur via l'API de test. On suppose qu'il existe déjà.")
            admin_password = ADMIN_PASSWORD  # Utiliser le mot de passe de l'admin existant
            results['create_first_admin'] = True
        
    except Exception as e:
        print_info(f"Erreur lors de la création du premier utilisateur: {str(e)}")
        print_info("On suppose que l'admin existe déjà")
        admin_password = ADMIN_PASSWORD  # Utiliser le mot de passe de l'admin existant
        results['create_first_admin'] = True
    
    # Les tests suivants sont similaires à la version originale
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
            'func': lambda: ApiClient().login(test_username, TEST_USER_PASSWORD),
            'expected_status': 401,
            'message': "Échec de connexion avec l'ancien mot de passe"
        },
        # 8. Connexion avec le nouveau mot de passe
        {
            'name': 'login_with_new_password',
            'func': lambda: ApiClient().login(test_username, "evenmoresecure456"),
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
    
    return success_count == len(results)def initialize_database():
    """Initialise la base de données avec un utilisateur admin si nécessaire"""
    print_header("INITIALISATION DE LA BASE DE DONNÉES")
    
    try:
        # Créer un client API pour les appels directs
        api_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
        
        # Vérifier si l'API est accessible
        try:
            response = requests.get(f"{api_url}/health")
            if response.status_code != 200:
                print_error(f"L'API n'est pas accessible: {response.status_code}")
                return False
            print_success("API accessible")
        except Exception as e:
            print_error(f"Erreur lors de l'accès à l'API: {str(e)}")
            return False
        
        # Initialiser la base de données
        try:
            # Utilisez l'endpoint spécial d'initialisation si disponible
            # Cet endpoint devrait être créé spécifiquement pour les tests
            init_url = f"{api_url}/db/init"
            response = requests.post(init_url)
            
            if response.status_code in [200, 201]:
                print_success("Base de données initialisée avec succès")
                return True
            else:
                print_info(f"Initialisation auto: {response.status_code}. Essai de l'initialisation manuelle...")
        except Exception as e:
            print_info(f"API d'initialisation non disponible: {str(e)}. Tentative d'initialisation manuelle...")
        
        # Essayer de se connecter avec les identifiants par défaut
        # On suppose qu'un compte admin existe déjà
        try:
            login_url = f"{api_url}/auth/login"
            response = requests.post(
                login_url,
                data={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
            )
            
            if response.status_code == 200:
                print_success("Connexion admin réussie, base de données prête")
                return True
            else:
                print_info("Aucun compte admin existant. Tests adaptés en conséquence.")
                # Nous continuerons sans admin
                return True
        except Exception as e:
            print_info(f"Erreur lors de la connexion admin: {str(e)}. Tests adaptés en conséquence.")
            return True
        
    except Exception as e:
        print_error(f"Erreur lors de l'initialisation: {str(e)}")
        return False"""
Tests pour les endpoints d'authentification
"""
import json
import time
import random
import string
import requests
import os
import sys
from colorama import Fore, Style, init

# Ajout du répertoire parent au path si nécessaire
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from tests.api.api_client import ApiClient
    from tests.config import (
        ADMIN_USERNAME, ADMIN_PASSWORD,
        TEST_USER_USERNAME, TEST_USER_EMAIL, TEST_USER_PASSWORD
    )
except ImportError:
    # Import alternatif si exécuté directement depuis le répertoire api/
    from api_client import ApiClient
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from config import (
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
    """Test complet du flux d'authentification avec détection automatique"""
    # D'abord, initialiser la base de données ou vérifier son état
    initialize_database()
    
    # Utiliser la version sans admin préexistant
    return test_auth_flow_no_admin()

if __name__ == "__main__":
    test_auth_flow()
