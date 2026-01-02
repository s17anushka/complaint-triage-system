<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
    <div class="bg-slate-800/80 backdrop-blur-xl p-10 rounded-2xl shadow-2xl w-full max-w-md border border-slate-700">
      
      <div class="flex justify-center mb-6">
        <div class="bg-blue-600 p-4 rounded-xl">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
      </div>

      <h2 class="text-3xl font-bold text-white text-center mb-2">
        Admin Login
      </h2>
      <p class="text-slate-400 text-sm text-center mb-8">
        Enter your credentials to access dashboard
      </p>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">
            Email
          </label>
          <input
            v-model="email"
            type="email"
            placeholder="admin@example.com"
            @keypress.enter="login"
            class="w-full px-4 py-3 rounded-xl bg-slate-900 text-white border border-slate-700 focus:ring-2 focus:ring-blue-600 outline-none transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            placeholder="Enter password"
            @keypress.enter="login"
            class="w-full px-4 py-3 rounded-xl bg-slate-900 text-white border border-slate-700 focus:ring-2 focus:ring-blue-600 outline-none transition"
          />
        </div>

        <button
          @click="login"
          :disabled="loading || !email || !password"
          class="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 transition font-semibold text-white shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>

        <p v-if="error" class="text-red-400 text-sm text-center">
          {{ error }}
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

const login = async () => {
  error.value = ''
  
  if (!email.value || !password.value) {
    error.value = 'Please enter both email and password'
    return
  }

  loading.value = true

  try {
    console.log('Attempting login...', email.value)
    
    const res = await api.adminLogin(email.value, password.value)

    console.log('Login response:', res.data)

    // Store token
    localStorage.setItem('adminToken', res.data.access_token)
    
    // Store user info
    localStorage.setItem('adminUser', JSON.stringify({
      email: res.data.email,
      role: res.data.role
    }))

    console.log('✅ Login successful, navigating to dashboard')

    // Navigate to dashboard
    router.push('/admin')

  } catch (err) {
    console.error('❌ Login failed:', err)
    console.error('Error response:', err.response?.data)
    error.value = err.response?.data?.detail || 'Invalid credentials'
  } finally {
    loading.value = false
  }
}
</script>