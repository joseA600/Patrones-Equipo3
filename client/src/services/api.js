import axios from 'axios'

// Cliente HTTP centralizado para mantener las llamadas a la API en un solo lugar.
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})
