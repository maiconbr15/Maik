from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RelatorioCreate(BaseModel):
    vistoria_id: int
    titulo: str
    descricao: Optional[str] = None

class RelatorioResponse(BaseModel):
    id: int
    vistoria_id: int
    titulo: str
    descricao: Optional[str]
    status: str
    caminho_pdf: Optional[str]
    criado_em: datetime
    gerado_em: Optional[datetime]

    class Config:
        from_attributes = True
