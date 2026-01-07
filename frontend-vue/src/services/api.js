// frontend-vue/src/services/api.js
import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000'

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default {
  submitComplaint(data) {
    return apiClient.post('/complaints/submit', {
      customer_name: data.name,
      email: data.email,
      text: data.complaint
    })
  },

  adminLogin(email, password) {
    return apiClient.post('/auth/admin/login', { email, password })
  },

  getMe() {
    return apiClient.get('/auth/me')
  },

  getComplaints() {
    return apiClient.get('/complaints/')
  },

  updateStatus(id, status) {
    return apiClient.patch(`/complaints/${id}/status?status=${status}`)
  },

  deleteComplaint(id) {
    return apiClient.delete(`/complaints/${id}`)
  },

  getStats() {
    return apiClient.get('/complaints/stats/summary')
  },

  generateReply(id) {
    return apiClient.post(`/complaints/${id}/reply`).then(res => {
      console.log("API /reply response:", res.data)
      return res
    })
    
  },
  sendReply(id,replyText) {
    return apiClient.post(`/complaints/${id}/send_reply`,
      { reply_text: replyText }
    )
  },
}