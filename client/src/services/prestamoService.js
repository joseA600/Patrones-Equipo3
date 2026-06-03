import { api } from './api'

export async function getPrestamos() {
  const response = await api.get('/prestamos')
  return response.data
}

export async function createPrestamo(payload) {
  const response = await api.post('/prestamos', payload)
  return response.data
}

export async function devolverPrestamo(prestamoId) {
  const response = await api.put(`/prestamos/${prestamoId}/devolver`)
  return response.data
}
