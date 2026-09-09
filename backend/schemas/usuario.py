from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioCreate(BaseModel):
    email: EmailStr
    nome: str
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

class UsuarioResponse(BaseModel):
    id: int
    email: str
    nome: str
    ativo: bool
    administrador: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
