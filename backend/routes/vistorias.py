from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from schemas import VistoriaCreate, VistoriaResponse, VistoriaUpdate
from models import Vistoria, Foto, Analise
from services import IAAnalysisService
import os
import uuid
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIRECTORY", "./uploads/vistorias")

@router.post("/", response_model=VistoriaResponse)
async def criar_vistoria(vistoria: VistoriaCreate, db: Session = Depends(get_db)):
    """
    Criar nova vistoria
    """
    # Gerar número de protocolo único
    numero_protocolo = f"VISO-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    
    nova_vistoria = Vistoria(
        numero_protocolo=numero_protocolo,
        placa_veiculo=vistoria.placa_veiculo,
        marca_modelo=vistoria.marca_modelo,
        ano_fabricacao=vistoria.ano_fabricacao,
        numero_chassi=vistoria.numero_chassi,
        localizacao=vistoria.localizacao,
        observacoes=vistoria.observacoes
    )
    
    db.add(nova_vistoria)
    db.commit()
    db.refresh(nova_vistoria)
    
    return nova_vistoria

@router.get("/{vistoria_id}", response_model=VistoriaResponse)
async def obter_vistoria(vistoria_id: int, db: Session = Depends(get_db)):
    """
    Obter dados de uma vistoria
    """
    vistoria = db.query(Vistoria).filter(Vistoria.id == vistoria_id).first()
    if not vistoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vistoria não encontrada"
        )
    return vistoria

@router.post("/{vistoria_id}/fotos")
async def upload_foto(
    vistoria_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload de foto para uma vistoria
    """
    vistoria = db.query(Vistoria).filter(Vistoria.id == vistoria_id).first()
    if not vistoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vistoria não encontrada"
        )
    
    # Criar diretório se não existir
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Gerar nome único para arquivo
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    # Salvar arquivo
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Criar registro de foto no banco
    foto = Foto(
        vistoria_id=vistoria_id,
        caminho_arquivo=file_path,
        nome_original=file.filename,
        tamanho_bytes=os.path.getsize(file_path),
        tipo_mime=file.content_type
    )
    
    db.add(foto)
    db.commit()
    db.refresh(foto)
    
    # Executar análise de IA
    resultado_ia = IAAnalysisService.analyze_vehicle_damage(file_path)
    
    if resultado_ia.get("sucesso"):
        analise = Analise(
            vistoria_id=vistoria_id,
            foto_id=foto.id,
            modelo_ia="gpt-4-vision",
            descricao=str(resultado_ia.get("dados", {})),
            danos_detectados=str(resultado_ia.get("dados", {}).get("danos_detectados", [])),
            confianca_percentual=resultado_ia.get("dados", {}).get("confianca", 0)
        )
        db.add(analise)
        db.commit()
    
    return {
        "foto_id": foto.id,
        "arquivo": file_name,
        "analise": resultado_ia
    }
