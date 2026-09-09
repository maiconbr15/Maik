import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { LogOut, Home, FileText, User } from 'lucide-react'
import { useAuthStore } from '../store/authStore'

export const Navbar: React.FC = () => {
  const navigate = useNavigate()
  const { usuario, logout, isAuthenticated } = useAuthStore()

  const handleLogout = () => {
    logout()
    localStorage.removeItem('access_token')
    navigate('/login')
  }

  if (!isAuthenticated()) {
    return null
  }

  return (
    <nav className="bg-primary text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold flex items-center gap-2">
          <Home size={28} />
          Maik
        </Link>

        <div className="flex items-center gap-6">
          <Link
            to="/dashboard"
            className="flex items-center gap-2 hover:text-accent transition-colors"
          >
            <FileText size={20} />
            Dashboard
          </Link>

          <div className="flex items-center gap-2">
            <User size={20} />
            <span>{usuario?.nome}</span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
          >
            <LogOut size={20} />
            Sair
          </button>
        </div>
      </div>
    </nav>
  )
}
