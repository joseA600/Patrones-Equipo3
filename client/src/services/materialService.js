import { api } from './api'

export async function getMateriales() {
  const response = await api.get('/materiales')
  return response.data
}

export async function getMaterialesDisponibles() {
  const response = await api.get('/materiales/disponibles')
  return response.data
}

export async function createMaterial(payload) {
  const response = await api.post('/materiales', payload)
  return response.data
}

export async function sendMaterialToMantenimiento(materialId) {
  const response = await api.put(`/materiales/${materialId}/mantenimiento`)
  return response.data
}
