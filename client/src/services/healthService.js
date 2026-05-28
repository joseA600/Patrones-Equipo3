import { api } from './api'

export async function getServerStatus() {
  const response = await api.get('/health')

  return response.data
}
