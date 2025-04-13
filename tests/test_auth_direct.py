#!/usr/bin/env python3
"""
Script direct pour tester l'authentification
Peut être exécuté depuis le répertoire des tests
"""

import os
import sys

# Ajout du répertoire actuel au path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import du test d'authentification
from api.test_auth import test_auth_flow

if __name__ == "__main__":
    # Exécuter le test d'authentification
    success = test_auth_flow()
    
    # Sortir avec un code d'état en fonction du résultat des tests
    sys.exit(0 if success else 1)
