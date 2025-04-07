<template>
  <div class="home-container">
    <header class="header">
      <h1>Claude API Application</h1>
      <div class="user-info" v-if="isLoggedIn">
        <span>{{ userInfo.username }}</span>
        <button @click="logout" class="logout-button">
          Déconnexion
        </button>
      </div>
    </header>

    <main class="main-content">
      <div v-if="isLoggedIn" class="dashboard">
        <div class="card">
          <h2>Conversations</h2>
          <p>Gérez vos conversations avec Claude</p>
          <router-link to="/conversations" class="button">
            Accéder
          </router-link>
        </div>

        <div class="card">
          <h2>Monitoring</h2>
          <p>Suivez votre consommation et vos coûts</p>
          <router-link to="/monitoring" class="button">
            Accéder
          </router-link>
        </div>

        <div class="card">
          <h2>Paramètres</h2>
          <p>Configurez l'application et vos préférences</p>
          <router-link to="/settings" class="button">
            Accéder
          </router-link>
        </div>
      </div>

      <div v-else class="welcome">
        <h2>Bienvenue sur l'Application Claude API</h2>
        <p>Connectez-vous pour accéder à l'interface</p>
        <router-link to="/login" class="button">
          Se connecter
        </router-link>
      </div>
    </main>

    <footer class="footer">
      <p>Claude API Application v0.1.0</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      userInfo: null
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.userInfo
    }
  },
  mounted() {
    // Récupérer les informations utilisateur depuis le localStorage
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        this.userInfo = JSON.parse(userStr)
      } catch (e) {
        console.error('Erreur lors de la récupération des infos utilisateur:', e)
      }
    }
  },
  methods: {
    logout() {
      // Supprimer les informations d'authentification du localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.userInfo = null
      
      // Rediriger vers la page de connexion
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background-color: #6366f1;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-button {
  background-color: transparent;
  border: 1px solid white;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  padding: 2rem;
}

.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.welcome {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

.button {
  display: inline-block;
  background-color: #6366f1;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  margin-top: 1rem;
  transition: background-color 0.2s;
}

.button:hover {
  background-color: #4f46e5;
}

.footer {
  background-color: #f3f4f6;
  color: #4b5563;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style>
