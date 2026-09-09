# Sistema Despachante Administrador - Maik Vistorias

## 📋 Visão Geral
Sistema web para gerenciamento de vistorias veiculares com análise de IA, geração de PDFs e painel administrativo.

## 🏗️ Arquitetura

```
maik-vistorias/
├── backend/
│   ├── app.py / server.js
│   ├── routes/
│   │   ├── vistorias.py
│   │   ├── usuarios.py
│   │   └── relatorios.py
│   ├── services/
│   │   ├── ia_analysis.py
│   │   ├── pdf_generator.py
│   │   └── database.py
│   ├── models/
│   │   ├── vistoria.py
│   │   ├── usuario.py
│   │   └── relatorio.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   ├── VistoriaForm/
│   │   │   ├── PhotoUpload/
│   │   │   ├── AnalysisResult/
│   │   │   └── PDFPreview/
│   │   ├── pages/
│   │   │   ├── AdminPanel.jsx
│   │   │   ├── NewVistoria.jsx
│   │   │   └── RelatorioDetails.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   └── package.json
├── database/
│   └── schema.sql
└── README.md
```

## 🔧 Tecnologias

### Backend
- **Python/FastAPI** ou **Node.js/Express**
- **PostgreSQL** ou **MongoDB**
- **OpenAI Vision API** para análise de imagens
- **ReportLab** ou **PDFKit** para geração de PDFs

### Frontend
- **React** + **Vite**
- **TailwindCSS** para styling
- **React Query** para gerenciamento de estado
- **Formik** para formulários

### IA
- OpenAI Vision API
- Google Cloud Vision API (alternativa)

## 📝 Features

1. ✅ Painel Administrativo
2. ✅ Criar nova vistoria
3. ✅ Upload de fotos
4. ✅ Análise de IA automática
5. ✅ Geração de PDF
6. ✅ Histórico de vistorias
7. ✅ Exportação de relatórios

## 🚀 Próximos Passos
1. Implementar backend API
2. Criar interface frontend
3. Integrar IA para análise
4. Sistema de geração PDF
5. Autenticação e autorização
