import base64
import json
from typing import Optional, List, Dict
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class IAAnalysisService:
    @staticmethod
    def analyze_vehicle_damage(image_path: str) -> Dict:
        """
        Analisa danos veiculares em uma imagem usando GPT-4 Vision
        """
        try:
            # Ler e codificar a imagem
            with open(image_path, "rb") as image_file:
                image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
            
            # Determinar tipo de imagem
            image_type = "image/jpeg" if image_path.lower().endswith(".jpg") else "image/png"
            
            # Chamar API do OpenAI
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Você é um especialista em inspeção veicular. 
                                Analise esta imagem de um veículo e identifique:
                                1. Danos visíveis (arranhões, amassados, quebras)
                                2. Condição geral (excelente, bom, regular, ruim)
                                3. Áreas de risco ou preocupação
                                4. Recomendações de reparo
                                
                                Forneça a resposta em JSON com estrutura:
                                {
                                    "danos_detectados": [],
                                    "condicao_geral": "string",
                                    "confianca": 0-100,
                                    "areas_preocupacao": [],
                                    "recomendacoes": [],
                                    "necessita_manutencao": boolean
                                }"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{image_type};base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
            )
            
            # Extrair resposta
            result_text = response.choices[0].message.content
            
            # Tentar parsear JSON da resposta
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, retornar resposta como texto
                result = {
                    "descricao": result_text,
                    "confianca": 0,
                    "necessita_manutencao": False
                }
            
            return {
                "sucesso": True,
                "modelo": "gpt-4-vision",
                "dados": result
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e)
            }
    
    @staticmethod
    def generate_analysis_summary(analises: List[Dict]) -> str:
        """
        Gera um resumo das análises de múltiplas fotos
        """
        if not analises:
            return "Nenhuma análise disponível."
        
        try:
            summary_prompt = f"""Com base nas seguintes análises de inspeção veicular, 
            gere um resumo executivo em português:
            
            {json.dumps(analises, ensure_ascii=False)}
            
            O resumo deve incluir:
            - Avaliação geral do veículo
            - Principais problemas encontrados
            - Recomendações de ação
            - Estimativa de severidade (Baixa/Média/Alta)
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": summary_prompt}
                ],
                max_tokens=500,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erro ao gerar resumo: {str(e)}"
