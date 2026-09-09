from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UsuarioResponse, UsuarioUpdate
from models import Usuario

router = APIRouter()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obter dados de um usuário
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def atualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualizar dados do usuário
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if usuario_update.nome:
        usuario.nome = usuario_update.nome
    if usuario_update.email:
        usuario.email = usuario_update.email
    
    db.commit()
    db.refresh(usuario)
    return usuario
