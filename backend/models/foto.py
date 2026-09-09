from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Foto(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, index=True)
    vistoria_id = Column(Integer, ForeignKey("vistorias.id"))
    
    # Informações da foto
    caminho_arquivo = Column(String)
    nome_original = Column(String)
    descricao = Column(String, nullable=True)
    tamanho_bytes = Column(Integer)
    tipo_mime = Column(String)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    vistoria = relationship("Vistoria", back_populates="fotos")
    analises = relationship("Analise", back_populates="foto", cascade="all, delete-orphan")

    class Config:
        from_attributes = True
