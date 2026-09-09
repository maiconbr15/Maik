from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class StatusRelatorio(str, enum.Enum):
    RASCUNHO = "rascunho"
    PROCESSANDO = "processando"
    PRONTO = "pronto"
    ERRO = "erro"

class Relatorio(Base):
    __tablename__ = "relatorios"

    id = Column(Integer, primary_key=True, index=True)
    vistoria_id = Column(Integer, ForeignKey("vistorias.id"))
    
    # Dados do relatório
    titulo = Column(String)
    descricao = Column(Text, nullable=True)
    caminho_pdf = Column(String, nullable=True)
    status = Column(Enum(StatusRelatorio), default=StatusRelatorio.RASCUNHO)
    
    # Conteúdo
    conteudo_html = Column(Text, nullable=True)
    resumo_executivo = Column(Text, nullable=True)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    gerado_em = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    vistoria = relationship("Vistoria", back_populates="relatorios")

    class Config:
        from_attributes = True
