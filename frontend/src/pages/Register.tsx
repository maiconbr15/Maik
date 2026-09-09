import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useFormik } from 'formik'
import * as Yup from 'yup'
import toast from 'react-hot-toast'
import { authService } from '../services/api'

const validationSchema = Yup.object({
  nome: Yup.string().required('Nome obrigatório'),
  email: Yup.string().email('Email inválido').required('Email obrigatório'),
  senha: Yup.string().min(6, 'Senha com no mínimo 6 caracteres').required('Senha obrigatória'),
  confirmaSenha: Yup.string()
    .oneOf([Yup.ref('senha')], 'Senhas devem ser iguais')
    .required('Confirmação de senha obrigatória'),
})

export const Register: React.FC = () => {
  const navigate = useNavigate()

  const formik = useFormik({
    initialValues: {
      nome: '',
      email: '',
      senha: '',
      confirmaSenha: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      try {
        await authService.registrar(values.email, values.nome, values.senha)
        toast.success('Registro realizado! Faça login.')
        navigate('/login')
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Erro ao registrar')
      }
    },
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-primary mb-8">Maik</h1>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Registre-se</h2>

        <form onSubmit={formik.handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Nome</label>
            <input
              type="text"
              {...formik.getFieldProps('nome')}
              className="input-field"
              placeholder="Seu nome"
            />
            {formik.touched.nome && formik.errors.nome && (
              <p className="text-red-500 text-sm mt-1">{formik.errors.nome}</p>
            )}
          </div>

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

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Confirmar Senha</label>
            <input
              type="password"
              {...formik.getFieldProps('confirmaSenha')}
              className="input-field"
              placeholder="••••••••"
            />
            {formik.touched.confirmaSenha && formik.errors.confirmaSenha && (
              <p className="text-red-500 text-sm mt-1">{formik.errors.confirmaSenha}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={formik.isSubmitting}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {formik.isSubmitting ? 'Registrando...' : 'Registrar'}
          </button>
        </form>

        <p className="text-center text-gray-600 mt-6">
          Já tem conta?{' '}
          <Link to="/login" className="text-primary font-semibold hover:underline">
            Faça login
          </Link>
        </p>
      </div>
    </div>
  )
}
