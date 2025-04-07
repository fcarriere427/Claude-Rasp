<template>
  <div class="conversation-container">
    <div class="conversation-header">
      <button @click="goBack" class="back-button">
        <i class="pi pi-arrow-left"></i>
        Retour
      </button>
      <h1>{{ conversation.title }}</h1>
      <div class="conversation-actions">
        <button @click="exportConversation" class="action-button">
          <i class="pi pi-download"></i>
        </button>
        <button @click="toggleEditTitle" class="action-button">
          <i class="pi pi-pencil"></i>
        </button>
      </div>
    </div>
    
    <div v-if="editingTitle" class="edit-title">
      <input 
        v-model="newTitle" 
        type="text" 
        class="title-input"
        @keyup.enter="saveTitle"
      />
      <button @click="saveTitle" class="save-button">
        <i class="pi pi-check"></i>
      </button>
      <button @click="cancelEditTitle" class="cancel-button">
        <i class="pi pi-times"></i>
      </button>
    </div>
    
    <div class="messages-container">
      <div v-if="loading" class="loading">
        Chargement de la conversation...
      </div>
      
      <div v-else-if="messages.length === 0" class="empty-state">
        <p>Aucun message dans cette conversation.</p>
        <p>Commencez à discuter avec Claude!</p>
      </div>
      
      <div v-else class="messages">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']"
        >
          <div class="message-content">
            {{ message.content }}
          </div>
          <div class="message-meta">
            <span class="message-time">{{ formatTime(message.created_at) }}</span>
            <span v-if="message.role === 'assistant'" class="message-cost">
              {{ formatCost(message.cost) }} € ({{ message.input_tokens + message.output_tokens }} tokens)
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="message-input-container">
      <textarea 
        v-model="newMessage" 
        class="message-input"
        placeholder="Écrivez votre message ici..."
        @keyup.ctrl.enter="sendMessage"
        @keyup.meta.enter="sendMessage"
      ></textarea>
      <button @click="sendMessage" class="send-button" :disabled="!newMessage.trim()">
        <i class="pi pi-send"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Conversation',
  data() {
    return {
      loading: true,
      conversation: {
        id: null,
        title: ''
      },
      messages: [],
      newMessage: '',
      editingTitle: false,
      newTitle: '',
      typing: false
    }
  },
  computed: {
    conversationId() {
      return parseInt(this.$route.params.id)
    }
  },
  mounted() {
    this.fetchConversation()
  },
  methods: {
    fetchConversation() {
      // Pour le prototype, nous utilisons des données statiques
      // Dans une implémentation réelle, vous appelleriez votre API
      
      setTimeout(() => {
        this.conversation = {
          id: this.conversationId,
          title: `Conversation ${this.conversationId}`,
          created_at: new Date(Date.now() - 3600000),
          updated_at: new Date()
        }
        
        if (this.conversationId === 1) {
          // Conversation d'exemple
          this.messages = [
            {
              id: 1,
              role: 'assistant',
              content: 'Bonjour! Je suis Claude, un assistant intelligent. Comment puis-je vous aider aujourd\'hui?',
              created_at: new Date(Date.now() - 3600000),
              input_tokens: 0,
              output_tokens: 23,
              cost: 0.0046
            },
            {
              id: 2,
              role: 'user',
              content: 'Bonjour Claude! Pouvez-vous m\'expliquer comment fonctionne l\'API?',
              created_at: new Date(Date.now() - 3540000)
            },
            {
              id: 3,
              role: 'assistant',
              content: 'Bien sûr! L\'API Claude est une interface programmatique qui vous permet d\'interagir avec moi via des requêtes HTTP. Vous pouvez envoyer des messages textuels et recevoir des réponses. L\'API utilise un système de tokens pour facturer l\'utilisation, avec un coût différent pour les tokens d\'entrée et de sortie. Vous avez besoin d\'une clé API pour authentifier vos requêtes. Que souhaitez-vous savoir de plus précisément?',
              created_at: new Date(Date.now() - 3520000),
              input_tokens: 15,
              output_tokens: 78,
              cost: 0.0159
            }
          ]
        } else {
          // Conversations vides
          this.messages = []
        }
        
        this.loading = false
      }, 1000)
    },
    
    formatTime(date) {
      return new Date(date).toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatCost(cost) {
      return cost.toFixed(4)
    },
    
    sendMessage() {
      if (!this.newMessage.trim() || this.typing) return
      
      // Ajouter le message de l'utilisateur
      const userMessage = {
        id: this.messages.length + 1,
        role: 'user',
        content: this.newMessage,
        created_at: new Date()
      }
      
      this.messages.push(userMessage)
      const userMessageContent = this.newMessage
      this.newMessage = ''
      
      // Simuler la réponse de Claude
      this.typing = true
      setTimeout(() => {
        // Ajouter la réponse de Claude
        const assistantMessage = {
          id: this.messages.length + 1,
          role: 'assistant',
          content: this.generateResponse(userMessageContent),
          created_at: new Date(),
          input_tokens: Math.floor(userMessageContent.length / 4),
          output_tokens: Math.floor(Math.random() * 50) + 30,
          cost: Math.random() * 0.02 + 0.01
        }
        
        this.messages.push(assistantMessage)
        this.typing = false
      }, 2000)
    },
    
    generateResponse(userMessage) {
      // Fonction simpliste pour générer une réponse
      // Dans une implémentation réelle, ce serait un appel à l'API Claude
      
      const responses = [
        `J'ai bien compris votre message concernant "${userMessage.substring(0, 20)}...". Que puis-je faire d'autre pour vous aider?`,
        `Merci pour votre question. Pour répondre à "${userMessage.substring(0, 20)}...", je dirais que cela dépend du contexte spécifique. Pourriez-vous me donner plus de détails?`,
        `C'est une excellente question. En ce qui concerne "${userMessage.substring(0, 20)}...", il y a plusieurs approches possibles. Voulez-vous que j'explore une direction particulière?`,
        `J'ai analysé votre demande sur "${userMessage.substring(0, 20)}...". Voici quelques éléments de réponse, mais n'hésitez pas à me demander des précisions si nécessaire.`
      ]
      
      return responses[Math.floor(Math.random() * responses.length)]
    },
    
    toggleEditTitle() {
      this.editingTitle = !this.editingTitle
      this.newTitle = this.conversation.title
    },
    
    saveTitle() {
      if (this.newTitle.trim()) {
        this.conversation.title = this.newTitle
      }
      this.editingTitle = false
    },
    
    cancelEditTitle() {
      this.editingTitle = false
    },
    
    exportConversation() {
      // Dans une implémentation réelle, cela déclencherait un téléchargement
      alert('Export de la conversation au format Markdown (fonctionnalité à implémenter)')
    },
    
    goBack() {
      this.$router.push('/conversations')
    }
  }
}
</script>

<style scoped>
.conversation-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

.conversation-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #6366f1;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem;
  margin-right: 1rem;
}

.conversation-header h1 {
  flex: 1;
  margin: 0;
  font-size: 1.5rem;
}

.conversation-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
}

.action-button:hover {
  background-color: #f3f4f6;
  color: #6366f1;
}

.edit-title {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.title-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.save-button, .cancel-button {
  background: none;
  border: none;
  padding: 0.5rem;
  margin-left: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.save-button {
  color: #10b981;
}

.cancel-button {
  color: #ef4444;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.loading, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  text-align: center;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  max-width: 80%;
  padding: 1rem;
  border-radius: 8px;
}

.user-message {
  align-self: flex-end;
  background-color: #6366f1;
  color: white;
}

.assistant-message {
  align-self: flex-start;
  background-color: #f3f4f6;
  color: #1f2937;
}

.message-content {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  opacity: 0.7;
}

.message-input-container {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background-color: white;
}

.message-input {
  flex: 1;
  min-height: 3rem;
  max-height: 10rem;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
}

.send-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  width: 3rem;
  height: 3rem;
  margin-left: 0.75rem;
  cursor: pointer;
}

.send-button:disabled {
  background-color: #a5a6f6;
  cursor: not-allowed;
}
</style>
