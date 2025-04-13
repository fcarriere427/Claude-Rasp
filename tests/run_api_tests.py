"""
Script principal pour exécuter tous les tests API
"""
import os
import sys
import importlib
from colorama import Fore, Style, init

# Initialiser colorama
init(autoreset=True)

def print_title(text):
    """Afficher un titre"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*20} {text} {'='*20}{Style.RESET_ALL}")

def print_header(text):
    """Afficher un en-tête"""
    print(f"\n{Fore.YELLOW}{'-'*5} {text} {'-'*5}{Style.RESET_ALL}")

def print_success(text):
    """Afficher un message de succès"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Afficher un message d'erreur"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def run_all_tests():
    """Exécuter tous les tests API disponibles"""
    print_title("API TESTS")
    
    # Définir le répertoire des tests API
    api_test_dir = os.path.join(os.path.dirname(__file__), 'api')
    
    # Liste des fichiers de test (commençant par test_)
    test_files = [
        f[:-3] for f in os.listdir(api_test_dir) 
        if f.startswith('test_') and f.endswith('.py')
    ]
    
    if not test_files:
        print_error("Aucun fichier de test trouvé dans le répertoire 'api'")
        return False
    
    # Résultats des tests
    results = {}
    
    # Exécuter chaque fichier de test
    for test_file in test_files:
        print_header(f"Exécution des tests dans {test_file}")
        
        try:
            # Importer dynamiquement le module de test
            module_name = f'tests.api.{test_file}'
            module = importlib.import_module(module_name)
            
            # Trouver toutes les fonctions de test
            test_functions = [
                func for func_name, func in module.__dict__.items()
                if func_name.startswith('test_') and callable(func)
            ]
            
            if not test_functions:
                print_error(f"Aucune fonction de test trouvée dans {test_file}")
                results[test_file] = False
                continue
            
            # Exécuter chaque fonction de test
            file_results = []
            for test_func in test_functions:
                try:
                    result = test_func()
                    file_results.append(result)
                    if result:
                        print_success(f"Test {test_func.__name__} réussi")
                    else:
                        print_error(f"Test {test_func.__name__} échoué")
                except Exception as e:
                    print_error(f"Exception dans {test_func.__name__}: {str(e)}")
                    file_results.append(False)
            
            # Résultat global pour ce fichier
            results[test_file] = all(file_results)
            
        except Exception as e:
            print_error(f"Erreur lors du chargement du module {test_file}: {str(e)}")
            results[test_file] = False
    
    # Afficher les résultats globaux
    print_title("RÉSULTATS DES TESTS")
    
    for test_file, result in results.items():
        status = f"{Fore.GREEN}✓ SUCCÈS" if result else f"{Fore.RED}✗ ÉCHEC"
        print(f"{test_file}: {status}")
    
    success_count = sum(1 for result in results.values() if result)
    print(f"\nTotal: {success_count}/{len(results)} fichiers de test réussis")
    
    return all(results.values())

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
