import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface Usuario {
  id: number
  email: string
  nome: string
  administrador: boolean
}

interface AuthStore {
  usuario: Usuario | null
  token: string | null
  setUsuario: (usuario: Usuario) => void
  setToken: (token: string) => void
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthStore>(
  persist(
    (set, get) => ({
      usuario: null,
      token: null,
      setUsuario: (usuario) => set({ usuario }),
      setToken: (token) => set({ token }),
      logout: () => set({ usuario: null, token: null }),
      isAuthenticated: () => !!get().token,
    }),
    {
      name: 'auth-storage',
    }
  )
)
