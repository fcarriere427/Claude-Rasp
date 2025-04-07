<template>
  <div class="monitoring-container">
    <h1>Monitoring des coûts</h1>
    
    <div class="tabs">
      <button 
        :class="['tab-button', { active: activeTab === 'daily' }]" 
        @click="activeTab = 'daily'"
      >
        Utilisation quotidienne
      </button>
      <button 
        :class="['tab-button', { active: activeTab === 'monthly' }]" 
        @click="activeTab = 'monthly'"
      >
        Utilisation mensuelle
      </button>
      <button 
        :class="['tab-button', { active: activeTab === 'limits' }]" 
        @click="activeTab = 'limits'"
      >
        Limites
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      Chargement des données...
    </div>
    
    <div v-else>
      <!-- Onglet d'utilisation quotidienne -->
      <div v-if="activeTab === 'daily'" class="tab-content">
        <div class="chart-container">
          <canvas ref="dailyChart"></canvas>
        </div>
        <div class="stats-overview">
          <div class="stat-card">
            <h3>Utilisation aujourd'hui</h3>
            <div class="stat-value">{{ formatCost(dailyStats.today) }}€</div>
            <div class="stat-info">{{ dailyStats.todayTokens }} tokens</div>
          </div>
          <div class="stat-card">
            <h3>Moyenne 7 jours</h3>
            <div class="stat-value">{{ formatCost(dailyStats.average7d) }}€</div>
            <div class="stat-info">{{ dailyStats.average7dTokens }} tokens/jour</div>
          </div>
          <div class="stat-card">
            <h3>Maximum 30 jours</h3>
            <div class="stat-value">{{ formatCost(dailyStats.max30d) }}€</div>
            <div class="stat-info">{{ dailyStats.max30dDate }}</div>
          </div>
        </div>
      </div>
      
      <!-- Onglet d'utilisation mensuelle -->
      <div v-if="activeTab === 'monthly'" class="tab-content">
        <div class="chart-container">
          <canvas ref="monthlyChart"></canvas>
        </div>
        <div class="stats-overview">
          <div class="stat-card">
            <h3>Mois en cours</h3>
            <div class="stat-value">{{ formatCost(monthlyStats.currentMonth) }}€</div>
            <div class="stat-info">{{ monthlyStats.currentMonthTokens }} tokens</div>
          </div>
          <div class="stat-card">
            <h3>Mois précédent</h3>
            <div class="stat-value">{{ formatCost(monthlyStats.previousMonth) }}€</div>
            <div class="stat-info">{{ monthlyStats.previousMonthTokens }} tokens</div>
          </div>
          <div class="stat-card">
            <h3>Projection</h3>
            <div class="stat-value">{{ formatCost(monthlyStats.projection) }}€</div>
            <div class="stat-info">+{{ monthlyStats.projectionPercentage }}% vs mois précédent</div>
          </div>
        </div>
      </div>
      
      <!-- Onglet des limites -->
      <div v-if="activeTab === 'limits'" class="tab-content">
        <div class="limits-section">
          <h2>Limites actuelles</h2>
          
          <div class="limit-card">
            <div class="limit-header">
              <h3>Limite quotidienne</h3>
              <div class="limit-value">{{ formatCost(limits.daily.limit) }}€</div>
            </div>
            <div class="progress-container">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: `${limits.daily.percentage}%`, backgroundColor: getProgressColor(limits.daily.percentage) }"
                ></div>
              </div>
              <div class="progress-label">
                {{ formatCost(limits.daily.current) }}€ ({{ limits.daily.percentage }}%)
              </div>
            </div>
          </div>
          
          <div class="limit-card">
            <div class="limit-header">
              <h3>Limite mensuelle</h3>
              <div class="limit-value">{{ formatCost(limits.monthly.limit) }}€</div>
            </div>
            <div class="progress-container">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: `${limits.monthly.percentage}%`, backgroundColor: getProgressColor(limits.monthly.percentage) }"
                ></div>
              </div>
              <div class="progress-label">
                {{ formatCost(limits.monthly.current) }}€ ({{ limits.monthly.percentage }}%)
              </div>
            </div>
          </div>
          
          <div class="limit-options">
            <h3>Options de limite</h3>
            <div class="options-grid">
              <div class="option">
                <input type="checkbox" id="alert70" v-model="limits.options.alert70" />
                <label for="alert70">Alerte à 70%</label>
              </div>
              <div class="option">
                <input type="checkbox" id="alert90" v-model="limits.options.alert90" />
                <label for="alert90">Alerte à 90%</label>
              </div>
              <div class="option">
                <input type="checkbox" id="killSwitch" v-model="limits.options.killSwitch" />
                <label for="killSwitch">Kill switch activé</label>
              </div>
            </div>
          </div>
          
          <div class="limit-actions">
            <button @click="showLimitModal = true" class="edit-button">
              <i class="pi pi-pencil"></i> Modifier les limites
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal de modification des limites -->
    <div v-if="showLimitModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Modifier les limites</h2>
          <button @click="showLimitModal = false" class="close-button">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="dailyLimit">Limite quotidienne (€)</label>
            <input type="number" id="dailyLimit" v-model="editedLimits.daily" min="0" step="0.01" />
          </div>
          <div class="form-group">
            <label for="monthlyLimit">Limite mensuelle (€)</label>
            <input type="number" id="monthlyLimit" v-model="editedLimits.monthly" min="0" step="0.01" />
          </div>
          <div class="form-group">
            <label>Options</label>
            <div class="options-grid">
              <div class="option">
                <input type="checkbox" id="editAlert70" v-model="editedLimits.options.alert70" />
                <label for="editAlert70">Alerte à 70%</label>
              </div>
              <div class="option">
                <input type="checkbox" id="editAlert90" v-model="editedLimits.options.alert90" />
                <label for="editAlert90">Alerte à 90%</label>
              </div>
              <div class="option">
                <input type="checkbox" id="editKillSwitch" v-model="editedLimits.options.killSwitch" />
                <label for="editKillSwitch">Kill switch activé</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showLimitModal = false" class="cancel-button">Annuler</button>
          <button @click="saveLimits" class="save-button">Enregistrer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Note: Dans un projet réel, il faudrait importer Chart.js
// import Chart from 'chart.js/auto'

export default {
  name: 'Monitoring',
  data() {
    return {
      loading: true,
      activeTab: 'daily',
      showLimitModal: false,
      
      // Données quotidiennes
      dailyData: {
        labels: [],
        costs: [],
        tokens: []
      },
      dailyStats: {
        today: 0,
        todayTokens: 0,
        average7d: 0,
        average7dTokens: 0,
        max30d: 0,
        max30dDate: ''
      },
      
      // Données mensuelles
      monthlyData: {
        labels: [],
        costs: [],
        tokens: []
      },
      monthlyStats: {
        currentMonth: 0,
        currentMonthTokens: 0,
        previousMonth: 0,
        previousMonthTokens: 0,
        projection: 0,
        projectionPercentage: 0
      },
      
      // Limites
      limits: {
        daily: {
          limit: 5.0,
          current: 2.5,
          percentage: 50
        },
        monthly: {
          limit: 50.0,
          current: 18.7,
          percentage: 37
        },
        options: {
          alert70: true,
          alert90: true,
          killSwitch: true
        }
      },
      
      // Limites en édition
      editedLimits: {
        daily: 5.0,
        monthly: 50.0,
        options: {
          alert70: true,
          alert90: true,
          killSwitch: true
        }
      },
      
      // Références aux charts
      dailyChart: null,
      monthlyChart: null
    }
  },
  mounted() {
    setTimeout(() => {
      this.fetchData()
    }, 1000)
  },
  methods: {
    fetchData() {
      // Dans une implémentation réelle, vous appelleriez votre API
      // Ici, nous générons des données de démonstration
      
      // Données quotidiennes
      const days = 30
      const today = new Date()
      this.dailyData.labels = []
      this.dailyData.costs = []
      this.dailyData.tokens = []
      
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today)
        date.setDate(date.getDate() - i)
        
        const formattedDate = date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })
        this.dailyData.labels.push(formattedDate)
        
        // Générer des données aléatoires mais réalistes
        // Plus de consommation les jours de semaine
        const isWeekend = date.getDay() === 0 || date.getDay() === 6
        const baseCost = isWeekend ? 0.5 : 2.0
        const randomFactor = Math.random() * 2.0
        const cost = Math.round((baseCost + randomFactor) * 100) / 100
        
        this.dailyData.costs.push(cost)
        
        // Environ 5000 tokens par euro
        const tokens = Math.round(cost * 5000)
        this.dailyData.tokens.push(tokens)
      }
      
      // Générer des statistiques quotidiennes
      this.dailyStats.today = this.dailyData.costs[this.dailyData.costs.length - 1]
      this.dailyStats.todayTokens = this.dailyData.tokens[this.dailyData.tokens.length - 1]
      
      const last7Days = this.dailyData.costs.slice(-7)
      this.dailyStats.average7d = Math.round(last7Days.reduce((a, b) => a + b, 0) / 7 * 100) / 100
      
      const last7DaysTokens = this.dailyData.tokens.slice(-7)
      this.dailyStats.average7dTokens = Math.round(last7DaysTokens.reduce((a, b) => a + b, 0) / 7)
      
      const maxCost = Math.max(...this.dailyData.costs)
      this.dailyStats.max30d = maxCost
      const maxIndex = this.dailyData.costs.indexOf(maxCost)
      this.dailyStats.max30dDate = this.dailyData.labels[maxIndex]
      
      // Données mensuelles
      const months = 12
      const currentMonth = today.getMonth()
      const currentYear = today.getFullYear()
      this.monthlyData.labels = []
      this.monthlyData.costs = []
      this.monthlyData.tokens = []
      
      for (let i = months - 1; i >= 0; i--) {
        let monthIndex = currentMonth - i
        let year = currentYear
        
        if (monthIndex < 0) {
          monthIndex += 12
          year--
        }
        
        const monthName = new Date(year, monthIndex, 1).toLocaleDateString('fr-FR', { month: 'long' })
        this.monthlyData.labels.push(monthName)
        
        // Générer des données aléatoires mais avec une tendance à la hausse
        const baseCost = 20 + i * 2 // Tendance à la hausse
        const randomFactor = Math.random() * 10.0 - 5.0 // Variation aléatoire
        const cost = Math.round((baseCost + randomFactor) * 100) / 100
        
        this.monthlyData.costs.push(cost)
        
        // Environ 5000 tokens par euro
        const tokens = Math.round(cost * 5000)
        this.monthlyData.tokens.push(tokens)
      }
      
      // Générer des statistiques mensuelles
      this.monthlyStats.currentMonth = this.monthlyData.costs[this.monthlyData.costs.length - 1]
      this.monthlyStats.currentMonthTokens = this.monthlyData.tokens[this.monthlyData.tokens.length - 1]
      
      this.monthlyStats.previousMonth = this.monthlyData.costs[this.monthlyData.costs.length - 2]
      this.monthlyStats.previousMonthTokens = this.monthlyData.tokens[this.monthlyData.tokens.length - 2]
      
      // Projection basée sur la consommation actuelle
      const dayOfMonth = today.getDate()
      const daysInMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate()
      this.monthlyStats.projection = Math.round((this.monthlyStats.currentMonth / dayOfMonth * daysInMonth) * 100) / 100
      
      // Pourcentage de variation
      this.monthlyStats.projectionPercentage = Math.round((this.monthlyStats.projection / this.monthlyStats.previousMonth - 1) * 100)
      
      // Mise à jour des limites
      this.limits.daily.current = this.dailyStats.today
      this.limits.daily.percentage = Math.round((this.limits.daily.current / this.limits.daily.limit) * 100)
      
      this.limits.monthly.current = this.monthlyStats.currentMonth
      this.limits.monthly.percentage = Math.round((this.limits.monthly.current / this.limits.monthly.limit) * 100)
      
      // Initialiser les valeurs d'édition
      this.editedLimits.daily = this.limits.daily.limit
      this.editedLimits.monthly = this.limits.monthly.limit
      this.editedLimits.options = { ...this.limits.options }
      
      this.loading = false
      
      // Créer les charts une fois les données chargées
      this.$nextTick(() => {
        this.createCharts()
      })
    },
    
    createCharts() {
      /* Note: Cette fonction utiliserait normalement Chart.js
       * Comme nous ne pouvons pas l'importer ici, ce code est commenté
       * et servirait de référence pour l'implémentation réelle
       */
      /*
      // Graphique d'utilisation quotidienne
      const dailyCtx = this.$refs.dailyChart.getContext('2d')
      this.dailyChart = new Chart(dailyCtx, {
        type: 'bar',
        data: {
          labels: this.dailyData.labels,
          datasets: [
            {
              label: 'Coût (€)',
              backgroundColor: '#6366F1',
              data: this.dailyData.costs
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const cost = context.raw.toFixed(2) + '€'
                  const tokens = Math.round(context.raw * 5000) + ' tokens'
                  return [cost, tokens]
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value.toFixed(2) + '€'
                }
              }
            }
          }
        }
      })
      
      // Graphique d'utilisation mensuelle
      const monthlyCtx = this.$refs.monthlyChart.getContext('2d')
      this.monthlyChart = new Chart(monthlyCtx, {
        type: 'bar',
        data: {
          labels: this.monthlyData.labels,
          datasets: [
            {
              label: 'Coût (€)',
              backgroundColor: '#3B82F6',
              data: this.monthlyData.costs
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const cost = context.raw.toFixed(2) + '€'
                  const tokens = Math.round(context.raw * 5000) + ' tokens'
                  return [cost, tokens]
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value.toFixed(2) + '€'
                }
              }
            }
          }
        }
      })
      */
      
      console.log('Charts would be created here in a real implementation')
    },
    
    formatCost(cost) {
      return cost.toFixed(2)
    },
    
    getProgressColor(percentage) {
      if (percentage < 70) {
        return '#10B981' // Vert
      } else if (percentage < 90) {
        return '#F59E0B' // Orange
      } else {
        return '#EF4444' // Rouge
      }
    },
    
    saveLimits() {
      // Dans une implémentation réelle, vous appelleriez votre API
      this.limits.daily.limit = parseFloat(this.editedLimits.daily)
      this.limits.monthly.limit = parseFloat(this.editedLimits.monthly)
      this.limits.options = { ...this.editedLimits.options }
      
      // Recalculer les pourcentages
      this.limits.daily.percentage = Math.round((this.limits.daily.current / this.limits.daily.limit) * 100)
      this.limits.monthly.percentage = Math.round((this.limits.monthly.current / this.limits.monthly.limit) * 100)
      
      this.showLimitModal = false
      
      // Simuler une notification de succès
      alert('Limites mises à jour avec succès')
    }
  }
}
</script>

<style scoped>
.monitoring-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 1.5rem;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 1.5rem;
}

.tab-button {
  background: none;
  border: none;
  padding: 1rem 1.5rem;
  margin-right: 0.5rem;
  font-size: 1rem;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tab-button.active {
  color: #6366f1;
  border-bottom-color: #6366f1;
}

.tab-button:hover {
  color: #4f46e5;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  color: #6b7280;
}

.tab-content {
  margin-bottom: 2rem;
}

.chart-container {
  height: 300px;
  position: relative;
  margin-bottom: 2rem;
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 1rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: #6b7280;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #111827;
  margin-bottom: 0.25rem;
}

.stat-info {
  font-size: 0.875rem;
  color: #6b7280;
}

.limits-section {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.limit-card {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 6px;
}

.limit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.limit-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #374151;
}

.limit-value {
  font-weight: bold;
  color: #111827;
}

.progress-container {
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 12px;
  background-color: #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  transition: width 0.5s, background-color 0.5s;
}

.progress-label {
  font-size: 0.875rem;
  color: #6b7280;
  text-align: right;
}

.limit-options {
  margin-top: 2rem;
  margin-bottom: 1.5rem;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 0.5rem;
}

.option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.limit-actions {
  margin-top: 1.5rem;
  text-align: right;
}

.edit-button {
  background-color: #6366f1;
  color: white;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.edit-button:hover {
  background-color: #4f46e5;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  color: #6b7280;
}

.modal-body {
  padding: 1.25rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input[type="number"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.25rem;
  border-top: 1px solid #e5e7eb;
}

.cancel-button, .save-button {
  padding: 0.75rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
}

.cancel-button {
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  color: #374151;
}

.save-button {
  background-color: #6366f1;
  border: none;
  color: white;
}

.cancel-button:hover {
  background-color: #e5e7eb;
}

.save-button:hover {
  background-color: #4f46e5;
}
</style>
