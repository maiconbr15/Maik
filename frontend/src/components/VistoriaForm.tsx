import React from 'react'
import { useFormik } from 'formik'
import * as Yup from 'yup'
import toast from 'react-hot-toast'
import { vistoriasService } from '../services/api'

const validationSchema = Yup.object({
  placa_veiculo: Yup.string().required('Placa obrigatória'),
  marca_modelo: Yup.string().required('Marca/Modelo obrigatório'),
  ano_fabricacao: Yup.number().required('Ano obrigatório'),
  numero_chassi: Yup.string().required('Número do chassi obrigatório'),
  localizacao: Yup.string().required('Localização obrigatória'),
})

interface VistoriaFormProps {
  onSuccess: (vistoria: any) => void
}

export const VistoriaForm: React.FC<VistoriaFormProps> = ({ onSuccess }) => {
  const formik = useFormik({
    initialValues: {
      placa_veiculo: '',
      marca_modelo: '',
      ano_fabricacao: new Date().getFullYear(),
      numero_chassi: '',
      localizacao: '',
      observacoes: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      try {
        const response = await vistoriasService.criar(values)
        toast.success('Vistoria criada com sucesso!')
        onSuccess(response.data)
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Erro ao criar vistoria')
      }
    },
  })

  const inputField = (name: keyof typeof formik.values) => ({
    value: formik.values[name],
    onChange: formik.handleChange,
    onBlur: formik.handleBlur,
    className: `input-field ${formik.touched[name] && formik.errors[name] ? 'border-red-500' : ''}`,
  })

  return (
    <form onSubmit={formik.handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Placa</label>
          <input {...inputField('placa_veiculo')} type="text" placeholder="ABC-1234" />
          {formik.touched.placa_veiculo && formik.errors.placa_veiculo && (
            <p className="text-red-500 text-sm mt-1">{formik.errors.placa_veiculo}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Marca/Modelo</label>
          <input {...inputField('marca_modelo')} type="text" placeholder="Toyota Corolla" />
          {formik.touched.marca_modelo && formik.errors.marca_modelo && (
            <p className="text-red-500 text-sm mt-1">{formik.errors.marca_modelo}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Ano</label>
          <input {...inputField('ano_fabricacao')} type="number" />
          {formik.touched.ano_fabricacao && formik.errors.ano_fabricacao && (
            <p className="text-red-500 text-sm mt-1">{formik.errors.ano_fabricacao}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Chassi</label>
          <input {...inputField('numero_chassi')} type="text" />
          {formik.touched.numero_chassi && formik.errors.numero_chassi && (
            <p className="text-red-500 text-sm mt-1">{formik.errors.numero_chassi}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Localização</label>
          <input {...inputField('localizacao')} type="text" />
          {formik.touched.localizacao && formik.errors.localizacao && (
            <p className="text-red-500 text-sm mt-1">{formik.errors.localizacao}</p>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Observações</label>
        <textarea
          {...inputField('observacoes')}
          rows={4}
          placeholder="Adicione observações sobre a vistoria..."
          className="input-field"
        />
      </div>

      <button
        type="submit"
        disabled={formik.isSubmitting}
        className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {formik.isSubmitting ? 'Criando...' : 'Criar Vistoria'}
      </button>
    </form>
  )
}
