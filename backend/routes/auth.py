from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UsuarioCreate
from models import Usuario
from services import AuthService
from datetime import timedelta

router = APIRouter()

@router.post("/registrar")
async def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar novo usuário
    """
    # Verificar se usuário já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar novo usuário
    novo_usuario = Usuario(
        email=usuario.email,
        nome=usuario.nome,
        senha_hash=AuthService.hash_password(usuario.senha)
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {"id": novo_usuario.id, "email": novo_usuario.email, "nome": novo_usuario.nome}

@router.post("/login")
async def login(email: str, senha: str, db: Session = Depends(get_db)):
    """
    Fazer login
    """
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario or not AuthService.verify_password(senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Criar token
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={"sub": usuario.email, "user_id": usuario.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "nome": usuario.nome,
            "administrador": usuario.administrador
        }
    }
