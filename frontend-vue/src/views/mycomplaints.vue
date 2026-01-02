<template>
  <div class="min-h-screen bg-slate-950 text-white px-8 py-10">
    <h1 class="text-3xl font-bold text-blue-400 mb-8">
      My Complaints
    </h1>

    <div v-if="complaints.length === 0" class="text-slate-400">
      No complaints found.
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="c in complaints"
        :key="c.id"
        class="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-blue-600 transition shadow-lg"
      >
        <div class="flex justify-between mb-3">
          <span class="text-sm text-slate-400">
            {{ formatDate(c.created_at) }}
          </span>
          <span
            :class="statusColor(c.status)"
            class="text-xs px-3 py-1 rounded-full font-bold"
          >
            {{ c.status }}
          </span>
        </div>

        <p class="text-slate-300 leading-relaxed">
          {{ c.text }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const complaints = ref([])

onMounted(async () => {
  const email = localStorage.getItem('user_email')
  if (!email) return

  const res = await api.getUserComplaints(email)
  complaints.value = res.data
})

const formatDate = (d) =>
  new Date(d).toLocaleDateString()

const statusColor = (s) => {
  if (s === 'open') return 'bg-yellow-500'
  if (s === 'resolved') return 'bg-green-600'
  return 'bg-blue-600'
}
</script>
