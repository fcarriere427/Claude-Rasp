<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">My Own Personal Claude</h1>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input 
            id="username"
            v-model="username"
            type="text"
            required
            class="form-control"
            placeholder="Entrez votre nom d'utilisateur"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input 
            id="password"
            v-model="password"
            type="password"
            required
            class="form-control"
            placeholder="Entrez votre mot de passe"
          />
        </div>
        
        <div class="form-check">
          <input 
            id="remember"
            v-model="rememberMe"
            type="checkbox"
            class="form-check-input"
          />
          <label for="remember" class="form-check-label">Se souvenir de moi</label>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? 'Connexion en cours...' : 'Se connecter' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      error: null,
      loading: false
    }
  },
  methods: {
    async login() {
      this.loading = true
      this.error = null
      
      try {
        // Dans une implémentation réelle, vous appelleriez votre API d'authentification ici
        // Pour l'instant, nous simulons une connexion réussie
        console.log('Tentative de connexion avec:', this.username, this.password)
        
        // Simuler un délai d'API
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Pour le prototype, nous acceptons tout utilisateur/mot de passe
        localStorage.setItem('token', 'dummy-token')
        localStorage.setItem('user', JSON.stringify({ 
          username: this.username,
          isAdmin: this.username === 'admin'
        }))
        
        // Redirection vers la page d'accueil
        this.$router.push('/')
      } catch (error) {
        this.error = "Erreur de connexion. Veuillez vérifier vos identifiants."
        console.error('Erreur de connexion:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f3f4f6;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  color: #6366f1;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-control {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.form-check {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.login-button {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #6366f1;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #4f46e5;
}

.login-button:disabled {
  background-color: #a5a6f6;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>
