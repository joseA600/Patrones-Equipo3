import { api } from './api'

export async function getBitacora() {
  const response = await api.get('/bitacora')
  return response.data
}
