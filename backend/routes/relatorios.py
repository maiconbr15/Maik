from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas import RelatorioCreate, RelatorioResponse
from models import Relatorio, Vistoria, Foto, Analise
from services import IAAnalysisService, PDFGeneratorService
import os
import json
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIRECTORY", "./uploads/vistorias")
PDF_DIR = os.path.join(UPLOAD_DIR, "pdfs")

@router.post("/{vistoria_id}/gerar", response_model=RelatorioResponse)
async def gerar_relatorio(
    vistoria_id: int,
    relatorio_data: RelatorioCreate,
    db: Session = Depends(get_db)
):
    """
    Gerar PDF de relatório de vistoria
    """
    # Obter vistoria
    vistoria = db.query(Vistoria).filter(Vistoria.id == vistoria_id).first()
    if not vistoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vistoria não encontrada"
        )
    
    # Criar diretório de PDFs se não existir
    os.makedirs(PDF_DIR, exist_ok=True)
    
    # Obter fotos e análises
    fotos = db.query(Foto).filter(Foto.vistoria_id == vistoria_id).all()
    analises = []
    fotos_caminhos = []
    
    for foto in fotos:
        foto_analise = db.query(Analise).filter(Analise.foto_id == foto.id).first()
        if foto_analise:
            analises.append(json.loads(foto_analise.descricao))
            fotos_caminhos.append(foto.caminho_arquivo)
    
    # Gerar resumo
    resumo = IAAnalysisService.generate_analysis_summary(analises)
    
    # Criar relatório no banco
    relatorio = Relatorio(
        vistoria_id=vistoria_id,
        titulo=relatorio_data.titulo,
        descricao=relatorio_data.descricao,
        status="processando",
        resumo_executivo=resumo
    )
    
    db.add(relatorio)
    db.commit()
    db.refresh(relatorio)
    
    # Gerar PDF
    pdf_filename = f"relatorio_{vistoria_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)
    
    pdf_service = PDFGeneratorService(titulo=relatorio_data.titulo)
    
    sucesso = pdf_service.gerar_relatorio(
        caminho_saida=pdf_path,
        vistoria_data={
            "placa_veiculo": vistoria.placa_veiculo,
            "marca_modelo": vistoria.marca_modelo,
            "ano_fabricacao": vistoria.ano_fabricacao,
            "numero_chassi": vistoria.numero_chassi,
            "localizacao": vistoria.localizacao
        },
        fotos=fotos_caminhos,
        analises=analises,
        resumo=resumo
    )
    
    if sucesso:
        relatorio.caminho_pdf = pdf_path
        relatorio.status = "pronto"
        relatorio.gerado_em = datetime.utcnow()
    else:
        relatorio.status = "erro"
    
    db.commit()
    db.refresh(relatorio)
    
    return relatorio

@router.get("/{relatorio_id}/download")
async def download_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db)
):
    """
    Baixar PDF do relatório
    """
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    if not relatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )
    
    if not relatorio.caminho_pdf or not os.path.exists(relatorio.caminho_pdf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo PDF não encontrado"
        )
    
    return FileResponse(
        path=relatorio.caminho_pdf,
        filename=os.path.basename(relatorio.caminho_pdf),
        media_type="application/pdf"
    )
