import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Serviços de Autenticação
export const authService = {
  registrar: (email: string, nome: string, senha: string) =>
    api.post('/auth/registrar', { email, nome, senha }),
  
  login: (email: string, senha: string) =>
    api.post('/auth/login', { email, senha }),
}

// Serviços de Vistorias
export const vistoriasService = {
  criar: (data: any) =>
    api.post('/vistorias/', data),
  
  obter: (id: number) =>
    api.get(`/vistorias/${id}`),
  
  uploadFoto: (vistoriaId: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/vistorias/${vistoriaId}/fotos`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Serviços de Relatórios
export const relatoriosService = {
  gerar: (vistoriaId: number, data: any) =>
    api.post(`/relatorios/${vistoriaId}/gerar`, data),
  
  download: (relatorioId: number) =>
    api.get(`/relatorios/${relatorioId}/download`, { responseType: 'blob' }),
}

export default api
