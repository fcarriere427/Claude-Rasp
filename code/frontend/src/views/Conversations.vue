<template>
  <div class="conversations-container">
    <h1>Mes conversations</h1>
    
    <div class="actions">
      <button @click="createNewConversation" class="create-button">
        <i class="pi pi-plus"></i> Nouvelle conversation
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      Chargement des conversations...
    </div>
    
    <div v-else-if="conversations.length === 0" class="empty-state">
      <p>Vous n'avez pas encore de conversations.</p>
      <p>Commencez par créer une nouvelle conversation!</p>
    </div>
    
    <div v-else class="conversations-list">
      <div 
        v-for="conversation in conversations" 
        :key="conversation.id"
        class="conversation-card"
        @click="openConversation(conversation.id)"
      >
        <div class="conversation-header">
          <h3>{{ conversation.title }}</h3>
          <span class="date">{{ formatDate(conversation.updated_at) }}</span>
        </div>
        <p class="preview">{{ conversation.last_message_preview || 'Aucun message' }}</p>
        <div class="conversation-footer">
          <span class="message-count">{{ conversation.message_count }} message(s)</span>
          <button @click.stop="deleteConversation(conversation.id)" class="delete-button">
            <i class="pi pi-trash"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Conversations',
  data() {
    return {
      loading: true,
      conversations: []
    }
  },
  mounted() {
    // Simuler le chargement des données
    setTimeout(() => {
      this.fetchConversations()
    }, 1000)
  },
  methods: {
    fetchConversations() {
      // Pour le prototype, nous utilisons des données statiques
      // Dans une implémentation réelle, vous appelleriez votre API
      this.conversations = [
        {
          id: 1,
          title: 'Introduction à Claude',
          updated_at: new Date(Date.now() - 3600000), // 1 heure avant
          last_message_preview: 'Bonjour! Je suis Claude, un assistant intelligent. Comment puis-je vous aider aujourd\'hui?',
          message_count: 3
        },
        {
          id: 2,
          title: 'Projet document technique',
          updated_at: new Date(Date.now() - 86400000), // 1 jour avant
          last_message_preview: 'Voici la dernière version du document avec les modifications que vous avez demandées.',
          message_count: 12
        },
        {
          id: 3,
          title: 'Questions sur l\'API',
          updated_at: new Date(Date.now() - 259200000), // 3 jours avant
          last_message_preview: 'L\'API REST est accessible via le endpoint /api/v1/',
          message_count: 8
        }
      ]
      this.loading = false
    },
    
    formatDate(date) {
      // Formater la date pour l'affichage
      return new Date(date).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    createNewConversation() {
      // Dans une implémentation réelle, vous appelleriez votre API pour créer une nouvelle conversation
      const newId = this.conversations.length > 0 
        ? Math.max(...this.conversations.map(c => c.id)) + 1 
        : 1
        
      const newConversation = {
        id: newId,
        title: `Nouvelle conversation ${newId}`,
        updated_at: new Date(),
        last_message_preview: '',
        message_count: 0
      }
      
      this.conversations.unshift(newConversation)
      this.openConversation(newId)
    },
    
    openConversation(id) {
      this.$router.push(`/conversation/${id}`)
    },
    
    deleteConversation(id) {
      // Dans une implémentation réelle, vous appelleriez votre API pour supprimer la conversation
      if (confirm('Êtes-vous sûr de vouloir supprimer cette conversation?')) {
        this.conversations = this.conversations.filter(c => c.id !== id)
      }
    }
  }
}
</script>

<style scoped>
.conversations-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.actions {
  margin-bottom: 1.5rem;
}

.create-button {
  background-color: #6366f1;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.create-button:hover {
  background-color: #4f46e5;
}

.loading, .empty-state {
  text-align: center;
  margin: 3rem 0;
  color: #6b7280;
}

.conversations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.conversation-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.conversation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.conversation-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #111827;
}

.date {
  font-size: 0.875rem;
  color: #6b7280;
}

.preview {
  margin: 0 0 1rem;
  color: #4b5563;
  font-size: 0.95rem;
  line-height: 1.5;
  /* Limiter à 2 lignes et ajouter les points de suspension */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.conversation-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-count {
  font-size: 0.875rem;
  color: #6b7280;
}

.delete-button {
  background-color: transparent;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
}

.delete-button:hover {
  background-color: rgba(239, 68, 68, 0.1);
}
</style>
