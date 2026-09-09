from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VistoriaCreate(BaseModel):
    placa_veiculo: str
    marca_modelo: str
    ano_fabricacao: int
    numero_chassi: str
    localizacao: str
    observacoes: Optional[str] = None

class VistoriaUpdate(BaseModel):
    localizacao: Optional[str] = None
    observacoes: Optional[str] = None

class VistoriaResponse(BaseModel):
    id: int
    numero_protocolo: str
    placa_veiculo: str
    marca_modelo: str
    ano_fabricacao: int
    numero_chassi: str
    localizacao: str
    observacoes: Optional[str]
    status: str
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
