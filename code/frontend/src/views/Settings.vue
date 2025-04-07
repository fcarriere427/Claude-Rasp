<template>
  <div class="settings-container">
    <h1>Paramètres</h1>
    
    <div class="settings-card">
      <h2>Paramètres du compte</h2>
      
      <div class="form-group">
        <label for="username">Nom d'utilisateur</label>
        <div class="form-control-static">{{ userInfo.username }}</div>
      </div>
      
      <div class="form-group">
        <label for="email">Email</label>
        <input 
          id="email" 
          v-model="userSettings.email" 
          type="email" 
          class="form-control"
        />
      </div>
      
      <div class="form-divider"></div>
      
      <h3>Changer le mot de passe</h3>
      
      <div class="form-group">
        <label for="currentPassword">Mot de passe actuel</label>
        <input 
          id="currentPassword" 
          v-model="passwordChange.current" 
          type="password" 
          class="form-control"
        />
      </div>
      
      <div class="form-group">
        <label for="newPassword">Nouveau mot de passe</label>
        <input 
          id="newPassword" 
          v-model="passwordChange.new" 
          type="password" 
          class="form-control"
        />
      </div>
      
      <div class="form-group">
        <label for="confirmPassword">Confirmer le mot de passe</label>
        <input 
          id="confirmPassword" 
          v-model="passwordChange.confirm" 
          type="password" 
          class="form-control"
        />
      </div>
      
      <div class="form-actions">
        <button @click="saveUserSettings" class="save-button" :disabled="!hasUserChanges">
          Enregistrer les modifications
        </button>
      </div>
    </div>
    
    <div class="settings-card">
      <h2>Paramètres MCP (Multi-Claude Process)</h2>
      
      <div v-if="loadingMcpConfig" class="loading">
        Chargement des paramètres MCP...
      </div>
      
      <div v-else>
        <div class="tools-section">
          <h3>Outils disponibles</h3>
          
          <div class="tool-card" v-for="tool in mcpConfig.tools" :key="tool.name">
            <div class="tool-header">
              <div class="tool-title">
                <h4>{{ tool.display_name }}</h4>
                <div class="tool-description">{{ tool.description }}</div>
              </div>
              <div class="tool-toggle">
                <input 
                  :id="'toggle-' + tool.name" 
                  v-model="tool.enabled" 
                  type="checkbox"
                  class="toggle-input"
                />
                <label :for="'toggle-' + tool.name" class="toggle-label"></label>
              </div>
            </div>
            
            <div v-if="tool.enabled && tool.parameters && tool.parameters.length > 0" class="tool-parameters">
              <h5>Paramètres</h5>
              <div class="parameter" v-for="param in tool.parameters" :key="param.name">
                <label :for="tool.name + '-' + param.name">{{ param.name }}</label>
                
                <input 
                  v-if="param.type === 'string'" 
                  :id="tool.name + '-' + param.name"
                  v-model="param.value"
                  type="text"
                  class="parameter-input"
                />
                
                <input 
                  v-else-if="param.type === 'integer' || param.type === 'number'" 
                  :id="tool.name + '-' + param.name"
                  v-model.number="param.value"
                  type="number"
                  class="parameter-input"
                />
                
                <input 
                  v-else-if="param.type === 'boolean'" 
                  :id="tool.name + '-' + param.name"
                  v-model="param.value"
                  type="checkbox"
                  class="parameter-checkbox"
                />
                
                <div class="parameter-description">{{ param.description }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="global-settings">
          <h3>Paramètres globaux</h3>
          
          <div class="option">
            <input 
              id="log_requests" 
              v-model="mcpConfig.settings.log_requests" 
              type="checkbox" 
            />
            <label for="log_requests">Journalisation des requêtes</label>
          </div>
          
          <div class="option">
            <input 
              id="log_responses" 
              v-model="mcpConfig.settings.log_responses" 
              type="checkbox" 
            />
            <label for="log_responses">Journalisation des réponses</label>
          </div>
          
          <div class="form-group">
            <label for="timeout">Timeout (secondes)</label>
            <input 
              id="timeout" 
              v-model.number="mcpConfig.settings.timeout_seconds" 
              type="number" 
              min="1" 
              max="60" 
              class="form-control-small"
            />
          </div>
          
          <div class="form-group">
            <label for="retry_count">Nombre de tentatives</label>
            <input 
              id="retry_count" 
              v-model.number="mcpConfig.settings.retry_count" 
              type="number" 
              min="0" 
              max="5" 
              class="form-control-small"
            />
          </div>
          
          <div class="form-group">
            <label for="retry_delay">Délai entre tentatives (secondes)</label>
            <input 
              id="retry_delay" 
              v-model.number="mcpConfig.settings.retry_delay_seconds" 
              type="number" 
              min="1" 
              max="10" 
              class="form-control-small"
            />
          </div>
        </div>
        
        <div class="form-actions">
          <button @click="saveMcpSettings" class="save-button" :disabled="!hasMcpChanges">
            Enregistrer les paramètres MCP
          </button>
        </div>
      </div>
    </div>
    
    <div class="settings-card">
      <h2>Paramètres de l'application</h2>
      
      <div class="form-group">
        <label for="theme">Thème</label>
        <select id="theme" v-model="appSettings.theme" class="form-control">
          <option value="light">Clair</option>
          <option value="dark">Sombre</option>
          <option value="system">Système</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="language">Langue</label>
        <select id="language" v-model="appSettings.language" class="form-control">
          <option value="fr">Français</option>
          <option value="en">English</option>
        </select>
      </div>
      
      <div class="form-divider"></div>
      
      <h3>À propos</h3>
      <div class="about-info">
        <p><strong>Version :</strong> 0.1.0</p>
        <p><strong>Licence :</strong> Usage personnel</p>
        <p><strong>Auteur :</strong> Florian Carriere</p>
        <p><a href="https://github.com/fcarriere427/claude-rasp" target="_blank">GitHub</a></p>
      </div>
      
      <div class="form-actions">
        <button @click="saveAppSettings" class="save-button" :disabled="!hasAppChanges">
          Enregistrer les préférences
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      userInfo: {
        username: '',
        isAdmin: false
      },
      
      // Paramètres utilisateur
      userSettings: {
        email: ''
      },
      
      // Changement de mot de passe
      passwordChange: {
        current: '',
        new: '',
        confirm: ''
      },
      
      // État initial pour comparer les changements
      initialUserSettings: {
        email: ''
      },
      
      // Paramètres MCP
      loadingMcpConfig: true,
      mcpConfig: {
        version: '',
        tools: [],
        settings: {
          log_requests: true,
          log_responses: true,
          timeout_seconds: 10,
          retry_count: 2,
          retry_delay_seconds: 1
        }
      },
      initialMcpConfig: null,
      
      // Paramètres de l'application
      appSettings: {
        theme: 'light',
        language: 'fr'
      },
      initialAppSettings: {
        theme: 'light',
        language: 'fr'
      }
    }
  },
  
  computed: {
    hasUserChanges() {
      return this.userSettings.email !== this.initialUserSettings.email ||
             (this.passwordChange.current && this.passwordChange.new && this.passwordChange.confirm)
    },
    
    hasMcpChanges() {
      // Les outils et leurs paramètres sont plus complexes à comparer,
      // donc nous utilisons JSON.stringify pour une comparaison simple
      return JSON.stringify(this.mcpConfig) !== JSON.stringify(this.initialMcpConfig)
    },
    
    hasAppChanges() {
      return this.appSettings.theme !== this.initialAppSettings.theme ||
             this.appSettings.language !== this.initialAppSettings.language
    }
  },
  
  mounted() {
    this.loadUserInfo()
    this.loadMcpConfig()
    this.loadAppSettings()
  },
  
  methods: {
    loadUserInfo() {
      // Dans une implémentation réelle, vous récupéreriez ces données depuis votre API
      // et stockage local
      const userStr = localStorage.getItem('user')
      if (userStr) {
        try {
          this.userInfo = JSON.parse(userStr)
          this.userSettings.email = this.userInfo.email || 'utilisateur@exemple.com'
          this.initialUserSettings.email = this.userSettings.email
        } catch (e) {
          console.error('Erreur lors de la récupération des infos utilisateur:', e)
        }
      }
    },
    
    loadMcpConfig() {
      // Dans une implémentation réelle, vous appelleriez votre API
      // Ici, nous utilisons des données de démonstration
      
      setTimeout(() => {
        this.mcpConfig = {
          version: '1.0',
          tools: [
            {
              name: 'brave_search',
              display_name: 'Recherche Web',
              description: 'Effectue une recherche sur le web via l\'API Brave Search',
              enabled: true,
              parameters: [
                {
                  name: 'query',
                  type: 'string',
                  required: true,
                  description: 'Requête de recherche',
                  value: ''
                },
                {
                  name: 'count',
                  type: 'integer',
                  required: false,
                  description: 'Nombre de résultats (max 20)',
                  value: 5
                },
                {
                  name: 'offset',
                  type: 'integer',
                  required: false,
                  description: 'Décalage pour la pagination',
                  value: 0
                }
              ]
            },
            {
              name: 'local_search',
              display_name: 'Recherche Locale',
              description: 'Recherche des lieux et commerces à proximité via l\'API Brave Search',
              enabled: true,
              parameters: [
                {
                  name: 'query',
                  type: 'string',
                  required: true,
                  description: 'Requête de recherche locale',
                  value: ''
                },
                {
                  name: 'count',
                  type: 'integer',
                  required: false,
                  description: 'Nombre de résultats (max 20)',
                  value: 5
                }
              ]
            },
            {
              name: 'image_analysis',
              display_name: 'Analyse d\'image',
              description: 'Analyse et description d\'images (disponible dans la V2)',
              enabled: false,
              parameters: []
            }
          ],
          settings: {
            log_requests: true,
            log_responses: true,
            timeout_seconds: 10,
            retry_count: 2,
            retry_delay_seconds: 1
          }
        }
        
        // Pour la comparaison des changements
        this.initialMcpConfig = JSON.parse(JSON.stringify(this.mcpConfig))
        
        this.loadingMcpConfig = false
      }, 1000)
    },
    
    loadAppSettings() {
      // Dans une implémentation réelle, vous récupéreriez ces paramètres
      // depuis le localStorage ou une API
      
      // Thème
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.appSettings.theme = savedTheme
      this.initialAppSettings.theme = savedTheme
      
      // Langue
      const savedLanguage = localStorage.getItem('language') || 'fr'
      this.appSettings.language = savedLanguage
      this.initialAppSettings.language = savedLanguage
    },
    
    saveUserSettings() {
      // Validation du mot de passe
      if (this.passwordChange.current) {
        if (!this.passwordChange.new) {
          alert('Veuillez entrer un nouveau mot de passe')
          return
        }
        
        if (this.passwordChange.new !== this.passwordChange.confirm) {
          alert('Les mots de passe ne correspondent pas')
          return
        }
        
        // Dans une implémentation réelle, vous appelleriez votre API pour changer le mot de passe
        console.log('Changing password:', {
          current: this.passwordChange.current,
          new: this.passwordChange.new
        })
        
        // Réinitialiser les champs de mot de passe
        this.passwordChange.current = ''
        this.passwordChange.new = ''
        this.passwordChange.confirm = ''
      }
      
      // Enregistrer les autres paramètres utilisateur
      // Dans une implémentation réelle, vous appelleriez votre API
      console.log('Saving user settings:', this.userSettings)
      
      // Mise à jour des informations utilisateur
      const userInfo = JSON.parse(localStorage.getItem('user') || '{}')
      userInfo.email = this.userSettings.email
      localStorage.setItem('user', JSON.stringify(userInfo))
      
      // Mettre à jour les valeurs initiales
      this.initialUserSettings.email = this.userSettings.email
      
      // Notification
      alert('Paramètres utilisateur enregistrés avec succès')
    },
    
    saveMcpSettings() {
      // Dans une implémentation réelle, vous appelleriez votre API
      console.log('Saving MCP settings:', this.mcpConfig)
      
      // Mettre à jour les valeurs initiales
      this.initialMcpConfig = JSON.parse(JSON.stringify(this.mcpConfig))
      
      // Notification
      alert('Paramètres MCP enregistrés avec succès')
    },
    
    saveAppSettings() {
      // Dans une implémentation réelle, vous pourriez appeler une API
      // ou simplement stocker dans localStorage comme ici
      
      localStorage.setItem('theme', this.appSettings.theme)
      localStorage.setItem('language', this.appSettings.language)
      
      // Application du thème
      document.documentElement.setAttribute('data-theme', this.appSettings.theme)
      
      // Mettre à jour les valeurs initiales
      this.initialAppSettings.theme = this.appSettings.theme
      this.initialAppSettings.language = this.appSettings.language
      
      // Notification
      alert('Préférences enregistrées avec succès')
    }
  }
}
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
}

.settings-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  color: #111827;
}

h3 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #374151;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4b5563;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-control-small {
  width: 100px;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-control-static {
  padding: 0.75rem;
  background-color: #f3f4f6;
  border-radius: 6px;
  color: #6b7280;
}

.form-divider {
  margin: 1.5rem 0;
  border-top: 1px solid #e5e7eb;
}

.form-actions {
  margin-top: 1.5rem;
  text-align: right;
}

.save-button {
  background-color: #6366f1;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
}

.save-button:hover {
  background-color: #4f46e5;
}

.save-button:disabled {
  background-color: #a5a6f6;
  cursor: not-allowed;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
  color: #6b7280;
}

/* MCP Tools Styles */
.tools-section {
  margin-bottom: 2rem;
}

.tool-card {
  background-color: #f9fafb;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.tool-title {
  flex: 1;
}

.tool-title h4 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: #111827;
}

.tool-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.tool-toggle {
  padding-left: 1rem;
}

.toggle-input {
  display: none;
}

.toggle-label {
  display: inline-block;
  width: 48px;
  height: 24px;
  background-color: #e5e7eb;
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-label::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  transition: all 0.3s;
}

.toggle-input:checked + .toggle-label {
  background-color: #6366f1;
}

.toggle-input:checked + .toggle-label::after {
  left: 26px;
}

.tool-parameters {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.tool-parameters h5 {
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.parameter {
  margin-bottom: 0.75rem;
}

.parameter label {
  display: block;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.parameter-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.875rem;
}

.parameter-description {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

/* Global Settings Styles */
.global-settings {
  background-color: #f9fafb;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.option {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.option input[type="checkbox"] {
  margin-right: 0.5rem;
}

/* About Info Styles */
.about-info {
  font-size: 0.875rem;
  color: #4b5563;
}

.about-info p {
  margin: 0.5rem 0;
}

.about-info a {
  color: #6366f1;
  text-decoration: none;
}

.about-info a:hover {
  text-decoration: underline;
}
</style>
