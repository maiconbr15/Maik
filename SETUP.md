# Setup Guide - Maik Sistema Despachante

## 🔧 Instalação Passo a Passo

### Pré-requisitos

1. **Python 3.10+**
   ```bash
   python --version
   ```

2. **PostgreSQL**
   - Download: https://www.postgresql.org/download/
   - Criar banco: `createdb maik_vistorias`

3. **Node.js 18+**
   ```bash
   node --version
   ```

4. **OpenAI API Key**
   - Acesse: https://platform.openai.com/api-keys
   - Gere uma nova chave

### Backend

#### 1. Clonar repositório

```bash
git clone https://github.com/maiconbr15/Maik.git
cd Maik/backend
```

#### 2. Criar ambiente virtual

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

#### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` com suas configurações:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/maik_vistorias
OPENAI_API_KEY=sua-chave-aqui
SECRET_KEY=sua-chave-secreta-super-segura-e-longa
```

#### 5. Criar tabelas no banco

```bash
# Python shell
python
>>> from app import app
>>> from database import create_tables
>>> create_tables()
>>> exit()
```

#### 6. Iniciar servidor

```bash
python app.py
```

✅ Backend estará em: `http://localhost:8000`

### Frontend

#### 1. Navegar até frontend

```bash
cd ../frontend
```

#### 2. Instalar dependências

```bash
npm install
```

#### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Verifique se `.env` contém:

```env
VITE_API_URL=http://localhost:8000/api
```

#### 4. Iniciar servidor de desenvolvimento

```bash
npm run dev
```

✅ Frontend estará em: `http://localhost:5173`

## ✅ Verificação

### Backend

- API: http://localhost:8000/
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Frontend

- App: http://localhost:5173/
- Login: http://localhost:5173/login
- Dashboard: http://localhost:5173/dashboard

## 🧪 Testar

### 1. Criar conta

```bash
POST /api/auth/registrar
{
  "email": "teste@exemplo.com",
  "nome": "Teste User",
  "senha": "senha123"
}
```

### 2. Fazer login

```bash
POST /api/auth/login
{
  "email": "teste@exemplo.com",
  "senha": "senha123"
}
```

### 3. Criar vistoria

```bash
POST /api/vistorias/
{
  "placa_veiculo": "ABC-1234",
  "marca_modelo": "Toyota Corolla",
  "ano_fabricacao": 2022,
  "numero_chassi": "1234567890123456",
  "localizacao": "São Paulo - SP"
}
```

### 4. Upload de foto

```bash
POST /api/vistorias/{vistoria_id}/fotos
Form-Data: file=image.jpg
```

### 5. Gerar relatório

```bash
POST /api/relatorios/{vistoria_id}/gerar
{
  "titulo": "Relatório - ABC-1234",
  "descricao": "Vistoria completa do veículo"
}
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

```bash
pip install fastapi uvicorn
```

### "connection refused" (PostgreSQL)

Verifique se PostgreSQL está rodando:

```bash
# Linux
sudo service postgresql status
sudo service postgresql start

# Mac
brew services start postgresql

# Windows
# Abra PostgreSQL via Services
```

### "CORS error"

Verifique se a URL do frontend está configurada corretamente em `app.py`:

```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

### "OpenAI API error"

Verifique sua chave de API:

```bash
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows
```

## 📚 Documentação Adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [OpenAI API](https://platform.openai.com/docs/)

## 🆘 Suporte

Se encontrar problemas, abra uma issue no GitHub com:
- Sistema operacional
- Versão do Python/Node
- Mensagem de erro completa
- Steps para reproduzir

---

**Happy coding! 🚀**
