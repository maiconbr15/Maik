from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
from typing import List, Dict, Optional

class PDFGeneratorService:
    def __init__(self, titulo: str = "Relatório de Vistoria Veicular"):
        self.titulo = titulo
        self.styles = getSampleStyleSheet()
        self._adicionar_estilos_customizados()
    
    def _adicionar_estilos_customizados(self):
        """Adicionar estilos customizados ao documento"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
    
    def gerar_relatorio(
        self,
        caminho_saida: str,
        vistoria_data: Dict,
        fotos: List[str],
        analises: List[Dict],
        resumo: str
    ) -> bool:
        """
        Gera PDF do relatório de vistoria
        
        Args:
            caminho_saida: Caminho onde salvar o PDF
            vistoria_data: Dados da vistoria (placa, marca, etc)
            fotos: Lista de caminhos das fotos
            analises: Lista de análises de IA
            resumo: Resumo executivo
        """
        try:
            # Criar documento
            doc = SimpleDocTemplate(
                caminho_saida,
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            # Lista de elementos
            elementos = []
            
            # Cabeçalho
            elementos.append(Paragraph(
                self.titulo,
                self.styles['CustomTitle']
            ))
            elementos.append(Spacer(1, 0.3*inch))
            
            # Informações da vistoria
            elementos.append(Paragraph(
                "Informações do Veículo",
                self.styles['CustomHeading']
            ))
            
            # Tabela com dados do veículo
            dados_veiculo = [
                ['Campo', 'Valor'],
                ['Placa', vistoria_data.get('placa_veiculo', 'N/A')],
                ['Marca/Modelo', vistoria_data.get('marca_modelo', 'N/A')],
                ['Ano', str(vistoria_data.get('ano_fabricacao', 'N/A'))],
                ['Chassi', vistoria_data.get('numero_chassi', 'N/A')],
                ['Localização', vistoria_data.get('localizacao', 'N/A')],
                ['Data da Vistoria', datetime.now().strftime('%d/%m/%Y %H:%M')]
            ]
            
            tabela_veiculo = Table(dados_veiculo, colWidths=[2*inch, 4*inch])
            tabela_veiculo.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elementos.append(tabela_veiculo)
            elementos.append(Spacer(1, 0.3*inch))
            
            # Resumo executivo
            elementos.append(Paragraph(
                "Resumo Executivo",
                self.styles['CustomHeading']
            ))
            elementos.append(Paragraph(resumo, self.styles['BodyText']))
            elementos.append(Spacer(1, 0.3*inch))
            
            # Fotos e análises
            if fotos:
                elementos.append(PageBreak())
                elementos.append(Paragraph(
                    "Fotos e Análises",
                    self.styles['CustomHeading']
                ))
                
                for idx, (foto_path, analise) in enumerate(zip(fotos, analises), 1):
                    if os.path.exists(foto_path):
                        try:
                            # Adicionar imagem
                            elementos.append(Paragraph(
                                f"Foto {idx}",
                                self.styles['Heading3']
                            ))
                            img = Image(foto_path, width=5*inch, height=4*inch)
                            elementos.append(img)
                            elementos.append(Spacer(1, 0.2*inch))
                            
                            # Adicionar análise da foto
                            elementos.append(Paragraph(
                                "Análise IA:",
                                self.styles['Heading4']
                            ))
                            
                            if isinstance(analise, dict):
                                analise_texto = json.dumps(analise, ensure_ascii=False, indent=2)
                            else:
                                analise_texto = str(analise)
                            
                            elementos.append(Paragraph(
                                analise_texto,
                                self.styles['BodyText']
                            ))
                            elementos.append(Spacer(1, 0.3*inch))
                            
                        except Exception as e:
                            elementos.append(Paragraph(
                                f"Erro ao processar foto {idx}: {str(e)}",
                                self.styles['BodyText']
                            ))
            
            # Rodapé
            elementos.append(Spacer(1, 0.3*inch))
            elementos.append(Paragraph(
                f"<i>Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</i>",
                self.styles['Normal']
            ))
            
            # Construir PDF
            doc.build(elementos)
            return True
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {str(e)}")
            return False
