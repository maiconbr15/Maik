import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useFormik } from 'formik'
import * as Yup from 'yup'
import toast from 'react-hot-toast'
import { authService } from '../services/api'
import { useAuthStore } from '../store/authStore'

const validationSchema = Yup.object({
  email: Yup.string().email('Email inválido').required('Email obrigatório'),
  senha: Yup.string().min(6, 'Senha com no mínimo 6 caracteres').required('Senha obrigatória'),
})

export const Login: React.FC = () => {
  const navigate = useNavigate()
  const { setUsuario, setToken } = useAuthStore()

  const formik = useFormik({
    initialValues: {
      email: '',
      senha: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      try {
        const response = await authService.login(values.email, values.senha)
        setToken(response.data.access_token)
        setUsuario(response.data.usuario)
        localStorage.setItem('access_token', response.data.access_token)
        toast.success('Login realizado com sucesso!')
        navigate('/dashboard')
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Erro ao fazer login')
      }
    },
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-primary mb-8">Maik</h1>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Login</h2>

        <form onSubmit={formik.handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              {...formik.getFieldProps('email')}
              className="input-field"
              placeholder="seu@email.com"
            />
            {formik.touched.email && formik.errors.email && (
              <p className="text-red-500 text-sm mt-1">{formik.errors.email}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Senha</label>
            <input
              type="password"
              {...formik.getFieldProps('senha')}
              className="input-field"
              placeholder="••••••••"
            />
            {formik.touched.senha && formik.errors.senha && (
              <p className="text-red-500 text-sm mt-1">{formik.errors.senha}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={formik.isSubmitting}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {formik.isSubmitting ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <p className="text-center text-gray-600 mt-6">
          Não tem conta?{' '}
          <Link to="/register" className="text-primary font-semibold hover:underline">
            Registre-se
          </Link>
        </p>
      </div>
    </div>
  )
}
