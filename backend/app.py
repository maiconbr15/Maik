from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Importar rotas
from routes import vistorias, usuarios, relatorios, auth

# Carregar variáveis de ambiente
load_dotenv()

# Criar diretório de uploads se não existir
os.makedirs(os.getenv("UPLOAD_DIRECTORY", "./uploads/vistorias"), exist_ok=True)

# Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Aplicação iniciada")
    yield
    print("🛑 Aplicação encerrada")

# Criar aplicação
app = FastAPI(
    title="Maik - Sistema Despachante Administrador",
    description="API para gerenciamento de vistorias veiculares com análise de IA",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuários"])
app.include_router(vistorias.router, prefix="/api/vistorias", tags=["Vistorias"])
app.include_router(relatorios.router, prefix="/api/relatorios", tags=["Relatórios"])

# Rota de health check
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao Maik - Sistema Despachante Administrador",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    )
