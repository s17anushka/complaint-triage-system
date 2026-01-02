// frontend-vue/src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('adminToken') || null)
  const user = ref(JSON.parse(localStorage.getItem('adminUser') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('adminToken', newToken)
  }

  function setUser(userData) {
    user.value = userData
    localStorage.setItem('adminUser', JSON.stringify(userData))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('adminToken')
    localStorage.removeItem('adminUser')
    
    localStorage.removeItem('adminEmail')
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    setUser,
    logout
  }
})