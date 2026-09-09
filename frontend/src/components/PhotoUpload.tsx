import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Image, Loader } from 'lucide-react'
import toast from 'react-hot-toast'
import { vistoriasService } from '../services/api'

interface PhotoUploadProps {
  vistoriaId: number
  onUploadSuccess: (data: any) => void
}

export const PhotoUpload: React.FC<PhotoUploadProps> = ({ vistoriaId, onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return

      const file = acceptedFiles[0]
      setUploading(true)

      // Preview
      const reader = new FileReader()
      reader.onload = () => setPreview(reader.result as string)
      reader.readAsDataURL(file)

      try {
        const response = await vistoriasService.uploadFoto(vistoriaId, file)
        toast.success('Foto enviada e analisada com sucesso!')
        onUploadSuccess(response.data)
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Erro ao enviar foto')
      } finally {
        setUploading(false)
      }
    },
    [vistoriaId, onUploadSuccess]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png'] },
  })

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-2">
          <Upload size={32} className="text-gray-400" />
          <p className="text-gray-600">
            {isDragActive ? 'Solte a foto aqui' : 'Arraste fotos ou clique para selecionar'}
          </p>
          <p className="text-sm text-gray-500">PNG, JPG até 50MB</p>
        </div>
      </div>

      {preview && (
        <div className="space-y-2">
          <img src={preview} alt="Preview" className="w-full h-64 object-cover rounded-lg" />
          {uploading && (
            <div className="flex items-center gap-2 text-blue-600">
              <Loader size={20} className="animate-spin" />
              <span>Analisando foto com IA...</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
