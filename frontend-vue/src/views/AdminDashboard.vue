<template>
  <div class="min-h-screen bg-slate-950 text-white px-8 py-6">
    <header class="mb-10">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-blue-400">Admin Dashboard</h1>
        <button 
          @click="logout" 
          class="text-sm bg-slate-800 px-4 py-2 rounded-lg hover:bg-red-600 hover:scale-105 active:scale-95 transition-all duration-200"
        >
          Logout
        </button>
      </div>

      <!-- Filter Bar -->
      <div class="bg-slate-900/50 border border-slate-800 rounded-xl p-4 backdrop-blur-sm">
        <div class="flex gap-4 items-end flex-wrap">
          <div class="flex-1 min-w-[200px]">
            <label class="text-xs text-slate-400 mb-1.5 block font-medium">SEVERITY</label>
            <select 
              v-model="filters.severity"
              class="w-full bg-slate-800 text-white px-3 py-2.5 rounded-lg border border-slate-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition cursor-pointer text-sm hover:border-slate-600"
            >
              <option value="all">All Severities</option>
              <option value="high">🔴 High Priority</option>
              <option value="medium">🟡 Medium Priority</option>
              <option value="low">🟢 Low Priority</option>
            </select>
          </div>

          <div class="flex-1 min-w-[200px]">
            <label class="text-xs text-slate-400 mb-1.5 block font-medium">STATUS</label>
            <select 
              v-model="filters.status"
              class="w-full bg-slate-800 text-white px-3 py-2.5 rounded-lg border border-slate-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition cursor-pointer text-sm hover:border-slate-600"
            >
              <option value="all">All Status</option>
              <option value="open">📂 Open</option>
              <option value="resolved">✅ Resolved</option>
          
            </select>
          </div>

          <button
            @click="resetFilters"
            class="bg-slate-700 text-white px-4 py-2.5 rounded-lg hover:bg-slate-600 hover:scale-105 active:scale-95 transition-all text-sm font-medium flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Reset
          </button>

          <div class="ml-auto bg-blue-500/10 border border-blue-500/30 px-4 py-2.5 rounded-lg">
            <span class="text-slate-400 text-xs font-medium mr-2">SHOWING:</span>
            <span class="text-blue-400 font-bold text-lg">{{ filteredComplaints.length }}</span>
            <span class="text-slate-500 text-xs ml-1">/ {{ complaints.length }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-slate-400 text-lg">Loading complaints...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="loadError" class="text-center text-red-400">
      <p class="text-xl mb-4">{{ loadError }}</p>
      <button 
        @click="loadComplaints" 
        class="bg-blue-600 px-6 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        Retry
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="complaints.length === 0" class="text-center text-slate-400 mt-20">
      <svg class="w-20 h-20 mx-auto mb-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
      <p class="text-xl">No complaints yet</p>
    </div>

    <!-- Complaints Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div
        v-for="c in filteredComplaints"
        :key="c.id"
        class="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 hover:scale-[1.03] hover:shadow-2xl hover:shadow-blue-500/20 hover:border-blue-500 hover:-translate-y-1 transition-all duration-300 shadow-lg cursor-pointer group"
      >
        <!-- Header -->
        <div class="flex justify-between items-start mb-3">
          <div>
            <h3 class="font-semibold text-lg text-white group-hover:text-blue-400 transition-colors">{{ c.customer_name }}</h3>
            <p class="text-slate-400 text-xs group-hover:text-slate-300 transition-colors">{{ c.email }}</p>
          </div>
          <div class="flex flex-col gap-2 items-end">
            <span
              :class="statusColor(c.status)"
              class="text-xs px-3 py-1 rounded-full font-bold uppercase"
            >
              {{ c.status }}
            </span>
            <span
              v-if="c.severity"
              :class="severityColor(c.severity)"
              class="text-xs px-3 py-1 rounded-full font-bold uppercase"
            >
              {{ c.severity }}
            </span>
          </div>
        </div>

        <!-- Complaint Text -->
        <p class="text-slate-300 text-sm mb-2 line-clamp-3">
          {{ c.text }}
        </p>

        <!-- Category & Notes -->
        <div class="mb-4 space-y-1">
          <p v-if="c.category" class="text-xs text-blue-400">
            📂 {{ c.category }}
          </p>
          <p v-if="c.notes" class="text-xs text-slate-500 italic">
            {{ c.notes }}
          </p>
          <p v-if="c.created_at" class="text-xs text-slate-600">
            📅 {{ formatDate(c.created_at) }}
          </p>
        </div>

        <!-- Actions -->
        <div class="flex flex-col gap-2">
          <div class="flex gap-2">
            <button
              @click="markResolved(c.id)"
              :disabled="c.status === 'resolved'"
              class="flex-1 text-sm bg-green-600 px-4 py-2 rounded-lg hover:bg-green-700 hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 font-medium"
            >
              {{ c.status === 'resolved' ? 'Resolved' : 'Resolve' }}
            </button>

            <button
              @click="remove(c.id)"
              class="text-sm bg-red-600 px-4 py-2 rounded-lg hover:bg-red-700 hover:scale-105 active:scale-95 transition-all font-medium"
            >
              Delete
            </button>
          </div>

          <button
            @click="generateReply(c)"
            class="w-full text-sm bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-2 rounded-lg hover:from-purple-700 hover:to-blue-700 hover:scale-105 active:scale-95 transition-all font-medium flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Generate AI Reply
          </button>
        </div>
      </div>
    </div>

    <!-- AI Reply Modal -->
    <div 
      v-if="showReplyModal" 
      class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6 z-50 animate-fadeIn"
      @click.self="closeReplyModal"
    >
      <div class="bg-gradient-to-br from-slate-900 to-slate-950 border-2 border-blue-500/50 rounded-2xl p-8 max-w-3xl w-full shadow-2xl shadow-blue-500/20 animate-slideUp">
        <!-- Header -->
        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="text-2xl font-bold text-white mb-1 flex items-center gap-2">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              AI Generated Reply
            </h2>
            <p class="text-slate-400 text-sm">For: {{ selectedComplaint?.customer_name }}</p>
          </div>
          <button 
            @click="closeReplyModal"
            class="text-slate-400 hover:text-white transition p-2 hover:bg-slate-800 rounded-lg"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Complaint Preview -->
        <div class="bg-slate-800/50 border border-slate-700 rounded-lg p-4 mb-4">
          <p class="text-xs text-slate-400 mb-1">Original Complaint:</p>
          <p class="text-slate-200 text-sm">{{ selectedComplaint?.text }}</p>
        </div>

        <!-- Loading State -->
        <div v-if="generatingReply" class="flex flex-col items-center justify-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mb-4"></div>
          <p class="text-slate-400">Generating intelligent reply...</p>
        </div>

        <!-- Reply Editor -->
        <div v-else>
          <label class="text-sm text-slate-400 mb-2 block font-medium">Edit & Send Reply:</label>
          <textarea
            v-model="aiReply"
            class="w-full bg-slate-800 text-white px-4 py-3 rounded-lg border-2 border-slate-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition resize-none mb-4"
            rows="10"
            placeholder="AI generated reply will appear here..."
          ></textarea>

          <!-- Action Buttons -->
          <div class="flex gap-3">
            <button
              @click="sendReply"
              :disabled="!aiReply.trim() || sendingReply"
              class="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white px-6 py-3 rounded-lg hover:from-green-700 hover:to-emerald-700 hover:scale-105 active:scale-95 transition-all font-medium flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              {{ sendingReply ? 'Sending...' : 'Send Reply' }}
            </button>

            <button
              @click="copyReply"
              class="bg-slate-700 text-white px-6 py-3 rounded-lg hover:bg-slate-600 hover:scale-105 active:scale-95 transition-all font-medium flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy
            </button>

            <button
              @click="regenerateReply"
              class="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 hover:scale-105 active:scale-95 transition-all font-medium flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Regenerate
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

const complaints = ref([])
const loading = ref(true)
const loadError = ref('')
const router = useRouter()

const filters = ref({
  severity: 'all',
  status: 'all'
})

// AI Reply Modal States
const showReplyModal = ref(false)
const selectedComplaint = ref(null)
const aiReply = ref('')
const generatingReply = ref(false)
const sendingReply = ref(false)

const filteredComplaints = computed(() => {
  return complaints.value.filter(c => {
    const severityMatch = filters.value.severity === 'all' || c.severity === filters.value.severity
    const statusMatch = filters.value.status === 'all' || c.status === filters.value.status
    return severityMatch && statusMatch
  })
})

const resetFilters = () => {
  filters.value = {
    severity: 'all',
    status: 'all'
  }
}

const loadComplaints = async () => {
  loading.value = true
  loadError.value = ''

  try {
    const res = await api.getComplaints()
    complaints.value = res.data
    console.log('✅ Complaints loaded:', res.data.length)
  } catch (err) {
    console.error('❌ Failed to load complaints:', err)
    
    if (err.response?.status === 401 || err.response?.status === 403) {
      localStorage.removeItem('adminToken')
      localStorage.removeItem('adminUser')
      router.push('/admin-login')
    } else {
      loadError.value = 'Failed to load complaints. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadComplaints()
})

const markResolved = async (id) => {
  try {
    await api.updateStatus(id, 'resolved')
    
    // Update local state
    const complaint = complaints.value.find(c => c.id === id)
    if (complaint) {
      complaint.status = 'resolved'
    }
    
    console.log('✅ Status updated to resolved')
  } catch (err) {
    console.error('❌ Failed to update status:', err)
    alert('Failed to update status: ' + (err.response?.data?.detail || err.message))
  }
}

const remove = async (id) => {
  if (!confirm('Are you sure you want to delete this complaint?')) {
    return
  }

  try {
    await api.deleteComplaint(id)
    complaints.value = complaints.value.filter(c => c.id !== id)
    console.log('✅ Complaint deleted')
  } catch (err) {
    console.error('❌ Failed to delete complaint:', err)
    alert('Failed to delete: ' + (err.response?.data?.detail || err.message))
  }
}

const logout = () => {
  localStorage.removeItem('adminToken')
  localStorage.removeItem('adminUser')
  router.push('/admin-login')
}

const statusColor = (s) => {
  const colors = {
    open: 'bg-yellow-500 text-black',
    resolved: 'bg-green-500 text-white',
    closed: 'bg-gray-500 text-white'
  }
  return colors[s] || 'bg-blue-500 text-white'
}

const severityColor = (s) => {
  const colors = {
    high: 'bg-red-500 text-white',
    medium: 'bg-orange-500 text-white',
    low: 'bg-green-500 text-white'
  }
  return colors[s] || 'bg-gray-500 text-white'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// AI Reply Functions
const generateReply = async (complaint) => {
  selectedComplaint.value = complaint
  showReplyModal.value = true
  generatingReply.value = true
  aiReply.value = ''
  
  try {
    const res = await api.generateReply(complaint.id)
    aiReply.value =  res.data.draft_reply || res.data.reply || res.data.ai_reply || res.data?.data?.draft_reply 
  } catch (err) {
    console.error('❌ Failed to generate AI reply:', err)
    alert('Failed to generate AI reply. Please try again.')
    closeReplyModal()
  } finally {
    generatingReply.value = false
  }
}

const closeReplyModal = () => {
  showReplyModal.value = false
  selectedComplaint.value = null
  aiReply.value = ''
  generatingReply.value = false
  sendingReply.value = false
}

const sendReply = async () => {
  if (!aiReply.value.trim() || !selectedComplaint.value) return

  sendingReply.value = true

  try {
    // 🔥 REAL BACKEND CALL
    await api.sendReply(selectedComplaint.value.id, aiReply.value)

    console.log('✅ Email sent to:', selectedComplaint.value.email)
    alert(`Reply sent successfully to ${selectedComplaint.value.customer_name}!`)

    closeReplyModal()
    loadComplaints()
  } catch (err) {
    console.error('❌ Failed to send email:', err)
    alert('Failed to send reply. Please try again.')
  } finally {
    sendingReply.value = false
  }
}

const copyReply = () => {
  navigator.clipboard.writeText(aiReply.value)
  alert('Reply copied to clipboard!')
}

const regenerateReply = () => {
  generateReply(selectedComplaint.value)
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>