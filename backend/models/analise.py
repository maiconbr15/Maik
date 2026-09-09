from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)
    vistoria_id = Column(Integer, ForeignKey("vistorias.id"))
    foto_id = Column(Integer, ForeignKey("fotos.id"))
    
    # Resultados da análise
    modelo_ia = Column(String)  # Ex: gpt-4-vision, google-vision
    descricao = Column(Text)  # Análise em texto
    danos_detectados = Column(Text)  # JSON com lista de danos
    confianca_percentual = Column(Float)  # 0-100
    tags = Column(Text)  # JSON com tags/categorias
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    vistoria = relationship("Vistoria", back_populates="analises")
    foto = relationship("Foto", back_populates="analises")

    class Config:
        from_attributes = True
