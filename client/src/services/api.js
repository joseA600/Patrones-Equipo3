import axios from 'axios'

// Cliente HTTP centralizado para mantener las llamadas a la API en un solo lugar.
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

export function getErrorMessage(error) {
  const detail =
    error.response?.data?.detail ??
    error.message ??
    'Ocurrio un error inesperado'

  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg).join(', ')
  }

  return typeof detail === 'string' ? detail : 'Ocurrio un error inesperado'
}
