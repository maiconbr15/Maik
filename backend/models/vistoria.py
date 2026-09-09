from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class StatusVistoria(str, enum.Enum):
    PENDENTE = "pendente"
    ANALISE = "analise"
    CONCLUIDA = "concluida"
    REJEITADA = "rejeitada"

class Vistoria(Base):
    __tablename__ = "vistorias"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Informações da vistoria
    numero_protocolo = Column(String, unique=True, index=True)
    placa_veiculo = Column(String)
    marca_modelo = Column(String)
    ano_fabricacao = Column(Integer)
    numero_chassi = Column(String)
    
    # Localização e dados
    localizacao = Column(String)
    observacoes = Column(Text)
    status = Column(Enum(StatusVistoria), default=StatusVistoria.PENDENTE)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    fotos = relationship("Foto", back_populates="vistoria", cascade="all, delete-orphan")
    analises = relationship("Analise", back_populates="vistoria", cascade="all, delete-orphan")
    relatorios = relationship("Relatorio", back_populates="vistoria", cascade="all, delete-orphan")

    class Config:
        from_attributes = True
