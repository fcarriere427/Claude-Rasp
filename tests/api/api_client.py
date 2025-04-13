"""
Client API réutilisable pour les tests
"""
import requests
from tests.config import API_BASE_URL

class ApiClient:
    """Client pour interagir avec l'API dans les tests"""
    
    def __init__(self, base_url=None):
        """Initialisation du client API"""
        self.base_url = base_url or API_BASE_URL
        self.token = None
        self.user_data = None
    
    def set_token(self, token):
        """Définir le token d'authentification"""
        self.token = token
    
    def get_headers(self):
        """Obtenir les en-têtes HTTP avec l'authentification si disponible"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def login(self, username, password):
        """Se connecter et récupérer un token JWT"""
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
        """Se déconnecter"""
        response = requests.post(
            f"{self.base_url}/auth/logout",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            self.token = None
            self.user_data = None
        return response
    
    def register_user(self, username, email, password, is_active=True, is_admin=False):
        """Enregistrer un nouvel utilisateur (nécessite des droits admin)"""
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
        """Récupérer les informations de l'utilisateur connecté"""
        return requests.get(
            f"{self.base_url}/auth/me",
            headers=self.get_headers()
        )
    
    def change_password(self, current_password, new_password):
        """Changer le mot de passe de l'utilisateur connecté"""
        payload = {
            "current_password": current_password,
            "new_password": new_password
        }
        return requests.put(
            f"{self.base_url}/auth/password",
            json=payload,
            headers=self.get_headers()
        )
    
    # Méthodes pour les futurs endpoints de l'API...
    # Ces méthodes seront ajoutées au fur et à mesure que de nouveaux endpoints sont implémentés
