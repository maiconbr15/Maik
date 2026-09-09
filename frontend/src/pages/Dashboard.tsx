import React, { useState } from 'react'
import { VistoriaForm } from '../components/VistoriaForm'
import { PhotoUpload } from '../components/PhotoUpload'
import { FileDown, Plus } from 'lucide-react'
import toast from 'react-hot-toast'
import { relatoriosService } from '../services/api'

interface Vistoria {
  id: number
  numero_protocolo: string
  placa_veiculo: string
  marca_modelo: string
}

export const Dashboard: React.FC = () => {
  const [vistoriaAtiva, setVistoriaAtiva] = useState<Vistoria | null>(null)
  const [showNewForm, setShowNewForm] = useState(false)
  const [vistorias, setVistorias] = useState<Vistoria[]>([])
  const [fotoAnalise, setFotoAnalise] = useState<any>(null)

  const handleVistoriaCreated = (vistoria: Vistoria) => {
    setVistorias([...vistorias, vistoria])
    setVistoriaAtiva(vistoria)
    setShowNewForm(false)
  }

  const handlePhotoUploaded = (data: any) => {
    setFotoAnalise(data)
  }

  const handleGerarRelatorio = async () => {
    if (!vistoriaAtiva) {
      toast.error('Selecione uma vistoria')
      return
    }

    try {
      const response = await relatoriosService.gerar(vistoriaAtiva.id, {
        titulo: `Relatório - ${vistoriaAtiva.placa_veiculo}`,
        descricao: 'Relatório automático gerado pelo sistema',
      })
      toast.success('Relatório gerado com sucesso!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao gerar relatório')
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-primary mb-8">Dashboard - Vistorias</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Seção de Vistorias */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-primary mb-4">Minhas Vistorias</h2>

            {vistorias.length === 0 ? (
              <p className="text-gray-500 mb-6">Nenhuma vistoria criada</p>
            ) : (
              <div className="space-y-2 mb-6">
                {vistorias.map((v) => (
                  <button
                    key={v.id}
                    onClick={() => setVistoriaAtiva(v)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      vistoriaAtiva?.id === v.id
                        ? 'bg-primary text-white'
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    <p className="font-semibold">{v.placa_veiculo}</p>
                    <p className="text-sm opacity-75">{v.numero_protocolo}</p>
                  </button>
                ))}
              </div>
            )}

            <button
              onClick={() => setShowNewForm(!showNewForm)}
              className="w-full btn-primary flex items-center justify-center gap-2"
            >
              <Plus size={20} />
              Nova Vistoria
            </button>
          </div>
        </div>

        {/* Seção Principal */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
            {showNewForm ? (
              <div>
                <h2 className="text-2xl font-bold text-primary mb-4">Nova Vistoria</h2>
                <VistoriaForm onSuccess={handleVistoriaCreated} />
              </div>
            ) : vistoriaAtiva ? (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-primary mb-4">{vistoriaAtiva.placa_veiculo}</h2>
                  <div className="grid grid-cols-2 gap-4 text-gray-600">
                    <p>
                      <span className="font-semibold">Protocolo:</span> {vistoriaAtiva.numero_protocolo}
                    </p>
                    <p>
                      <span className="font-semibold">Modelo:</span> {vistoriaAtiva.marca_modelo}
                    </p>
                  </div>
                </div>

                <div className="border-t pt-6">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Upload de Fotos</h3>
                  <PhotoUpload
                    vistoriaId={vistoriaAtiva.id}
                    onUploadSuccess={handlePhotoUploaded}
                  />
                </div>

                {fotoAnalise && (
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4">Análise IA</h3>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <pre className="text-sm overflow-auto">
                        {JSON.stringify(fotoAnalise, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}

                <button
                  onClick={handleGerarRelatorio}
                  className="w-full btn-primary flex items-center justify-center gap-2"
                >
                  <FileDown size={20} />
                  Gerar Relatório PDF
                </button>
              </div>
            ) : (
              <div className="text-center text-gray-500">
                <p>Selecione uma vistoria ou crie uma nova</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
