# Maik - Sistema Despachante Administrador

## 🎯 Descrição

Sistema web completo para gerenciamento de vistorias veiculares com:
- ✅ **Painel Administrativo** moderno e intuitivo
- ✅ **Análise de IA** automática de danos veiculares (GPT-4 Vision)
- ✅ **Upload de Fotos** com processamento inteligente
- ✅ **Geração de PDF** com relatórios profissionais
- ✅ **Autenticação JWT** segura
- ✅ **Banco de Dados** PostgreSQL com SQLAlchemy ORM

## 📋 Pré-requisitos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- OpenAI API Key (para análise com GPT-4 Vision)

## 🚀 Instalação

### 1. Backend (FastAPI)

```bash
# Navegar até o diretório backend
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Rodar migrations (se houver)
alembic upgrade head

# Iniciar servidor
python app.py
# ou
uvicorn app:app --reload
```

### 2. Frontend (React)

```bash
# Navegar até o diretório frontend
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: **http://localhost:5173**

## 📚 Documentação da API

Acesse a documentação interativa em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuração

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/maik_vistorias

# OpenAI API
OPENAI_API_KEY=sk-...

# JWT
SECRET_KEY=sua-chave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Upload
MAX_UPLOAD_SIZE=52428800  # 50MB
UPLOAD_DIRECTORY=./uploads/vistorias
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api
```

## 📁 Estrutura do Projeto

```
maik/
├── backend/
│   ├── app.py                 # Aplicação FastAPI principal
│   ├── database.py            # Configuração de BD
│   ├── requirements.txt       # Dependências Python
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── vistoria.py
│   │   ├── foto.py
│   │   ├── analise.py
│   │   └── relatorio.py
│   ├── schemas/               # Schemas Pydantic
│   │   ├── usuario.py
│   │   ├── vistoria.py
│   │   └── relatorio.py
│   ├── services/              # Lógica de negócio
│   │   ├── auth.py
│   │   ├── ia_analysis.py
│   │   └── pdf_generator.py
│   └── routes/                # Rotas API
│       ├── auth.py
│       ├── usuarios.py
│       ├── vistorias.py
│       └── relatorios.py
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Componente raiz
│   │   ├── main.tsx           # Entry point
│   │   ├── index.css          # Estilos globais
│   │   ├── components/        # Componentes reutilizáveis
│   │   │   ├── Navbar.tsx
│   │   │   ├── VistoriaForm.tsx
│   │   │   └── PhotoUpload.tsx
│   │   ├── pages/             # Páginas
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── services/          # Serviços API
│   │   │   └── api.ts
│   │   └── store/             # Estado global (Zustand)
│   │       └── authStore.ts
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
└── README.md
```

## 🔐 Autenticação

O sistema usa JWT (JSON Web Token) para autenticação:

1. **Registrar**: POST `/api/auth/registrar`
   ```json
   {
     "email": "usuario@exemplo.com",
     "nome": "João Silva",
     "senha": "senha123"
   }
   ```

2. **Login**: POST `/api/auth/login`
   ```json
   {
     "email": "usuario@exemplo.com",
     "senha": "senha123"
   }
   ```

3. **Resposta**:
   ```json
   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "token_type": "bearer",
     "usuario": {
       "id": 1,
       "email": "usuario@exemplo.com",
       "nome": "João Silva",
       "administrador": false
     }
   }
   ```

## 📸 Fluxo de Vistoria

1. **Criar Vistoria**: Adicione dados básicos do veículo
2. **Upload de Fotos**: Envie fotos do veículo (JPEG/PNG)
3. **Análise IA**: Sistema analisa automaticamente com GPT-4 Vision
4. **Revisão**: Analise os resultados da IA
5. **Gerar PDF**: Crie relatório profissional com fotos e análises

## 🤖 Análise de IA

O sistema utiliza **GPT-4 Vision** para:
- Detectar danos veiculares
- Avaliar condição geral
- Identificar áreas de preocupação
- Gerar recomendações de reparo
- Calcular confiança da análise

## 📄 Geração de PDF

Os relatórios incluem:
- ✅ Informações do veículo
- ✅ Fotos anexadas
- ✅ Análises de IA
- ✅ Resumo executivo
- ✅ Recomendações
- ✅ Data e hora da vistoria

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **OpenAI API** - Análise com IA
- **ReportLab** - Geração de PDF
- **Python-Jose** - JWT
- **Passlib** - Hash de senhas

### Frontend
- **React 18** - Biblioteca UI
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool moderno
- **TailwindCSS** - Framework CSS
- **Zustand** - Gerenciamento de estado
- **Formik + Yup** - Gerenciamento de formulários
- **Axios** - Cliente HTTP
- **React Router** - Roteamento

## 📊 Banco de Dados

### Tabelas

- **usuarios**: Usuários do sistema
- **vistorias**: Registro de vistorias
- **fotos**: Fotos anexadas às vistorias
- **analises**: Resultados das análises de IA
- **relatorios**: Relatórios gerados em PDF

## 🚀 Deploy

### Backend (Heroku/Railway)

```bash
# Railway
railway link
railway up

# Ou Heroku
heroku create seu-app
git push heroku main
```

### Frontend (Vercel/Netlify)

```bash
# Vercel
vercel

# Ou Netlify
netlify deploy --prod --dir dist
```

## 📝 Licença

MIT License - veja LICENSE.md

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 💬 Suporte

Para dúvidas ou problemas, entre em contato ou abra uma issue no GitHub.

---

**Desenvolvido com ❤️ por Maicon**
