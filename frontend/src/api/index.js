import axios from 'axios'
import { store } from '../store'
import { logout } from '../store/authSlice'

// Make sure the baseURL ends with /api and doesn't have trailing slash
const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:5000/api').replace(/\/$/, ''),
})

api.interceptors.request.use((config) => {
  const token = store.getState().auth.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      store.dispatch(logout())
    }
    return Promise.reject(err)
  }
)

export default api