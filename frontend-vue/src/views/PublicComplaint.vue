<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-6 py-12">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Submit Complaint</h1>
        <p class="text-gray-600">We're here to help resolve your concerns quickly</p>
      </div>

      <div class="bg-white rounded-lg shadow-lg p-8 border border-gray-200">
        <div class="space-y-6">
          <div>
            <label class="flex items-center text-sm font-semibold text-gray-900 mb-2 uppercase tracking-wide">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
              FULL NAME
            </label>
            <input
              v-model="formData.name"
              type="text"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
              placeholder="Enter your full name"
            />
          </div>

          <div>
            <label class="flex items-center text-sm font-semibold text-gray-900 mb-2 uppercase tracking-wide">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
              </svg>
              EMAIL ADDRESS <span class="text-red-600">*</span>
            </label>
            <input
              v-model="formData.email"
              type="email"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
              placeholder="your.email@example.com"
            />
          </div>

          <div>
            <label class="flex items-center text-sm font-semibold text-gray-900 mb-2 uppercase tracking-wide">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
              </svg>
              YOUR COMPLAINT <span class="text-red-600">*</span>
            </label>
            <textarea
              v-model="formData.complaint"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-none"
              rows="6"
              placeholder="Please describe your issue in detail..."
            ></textarea>
          </div>

          <button
            @click="handleSubmit"
            :disabled="loading"
            class="w-full bg-gray-900 text-white py-4 rounded-lg font-bold text-base hover:bg-gray-800 transition flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <span>{{ loading ? 'Submitting...' : 'Submit Complaint' }}</span>
          </button>

          <p v-if="error" class="text-red-600 text-sm text-center">
            {{ error }}
          </p>

          <p v-if="success" class="text-green-600 text-sm text-center">
            {{ success }}
          </p>
        </div>
      </div>

      <div class="mt-6 text-center">
        <div class="inline-flex items-center bg-amber-50 border border-amber-200 px-4 py-2 rounded-full">
          <svg class="w-4 h-4 text-amber-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
          </svg>
          <span class="text-sm text-amber-800 font-medium">Average response time: 24-48 hours</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const formData = ref({
  name: '',
  email: '',
  complaint: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const handleSubmit = async () => {
  error.value = ''
  success.value = ''

  // Validation
  if (!formData.value.name || !formData.value.email || !formData.value.complaint) {
    error.value = 'Please fill in all required fields'
    return
  }

  loading.value = true

  try {
    const res = await api.submitComplaint(formData.value)
    
    success.value = 'Complaint submitted successfully! We will get back to you soon.'
    
    // Reset form
    formData.value = {
      name: '',
      email: '',
      complaint: ''
    }

    console.log('✅ Complaint submitted:', res.data)
  } catch (err) {
    console.error('❌ Failed to submit complaint:', err)
    error.value = err.response?.data?.detail || 'Failed to submit complaint. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>