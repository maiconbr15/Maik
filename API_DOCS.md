# API Documentation - Maik

## Base URL

```
http://localhost:8000/api
```

## Authentication

Todos os endpoints (exceto auth) requerem header:

```
Authorization: Bearer {token}
```

## Endpoints

### Autenticação

#### Registrar

```http
POST /auth/registrar
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "nome": "João Silva",
  "senha": "senha123"
}

RESPONSE 200:
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "nome": "João Silva"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "senha": "senha123"
}

RESPONSE 200:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "nome": "João Silva",
    "administrador": false
  }
}
```

### Vistorias

#### Criar Vistoria

```http
POST /vistorias/
Authorization: Bearer {token}
Content-Type: application/json

{
  "placa_veiculo": "ABC-1234",
  "marca_modelo": "Toyota Corolla",
  "ano_fabricacao": 2022,
  "numero_chassi": "1234567890123456",
  "localizacao": "São Paulo - SP",
  "observacoes": "Opcional"
}

RESPONSE 200:
{
  "id": 1,
  "numero_protocolo": "VISO-20260909121548-ABC123",
  "placa_veiculo": "ABC-1234",
  "marca_modelo": "Toyota Corolla",
  "ano_fabricacao": 2022,
  "numero_chassi": "1234567890123456",
  "localizacao": "São Paulo - SP",
  "observacoes": "Opcional",
  "status": "pendente",
  "criado_em": "2026-09-09T12:15:48Z",
  "atualizado_em": "2026-09-09T12:15:48Z"
}
```

#### Obter Vistoria

```http
GET /vistorias/{id}
Authorization: Bearer {token}

RESPONSE 200:
{Same as above}
```

#### Upload de Foto

```http
POST /vistorias/{vistoria_id}/fotos
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [image_file]

RESPONSE 200:
{
  "foto_id": 1,
  "arquivo": "550e8400-e29b-41d4-a716-446655440000.jpg",
  "analise": {
    "sucesso": true,
    "modelo": "gpt-4-vision",
    "dados": {
      "danos_detectados": ["Arranhão na porta"],
      "condicao_geral": "bom",
      "confianca": 92,
      "areas_preocupacao": ["Pintura desgastada"],
      "recomendacoes": ["Reparo de pintura"]
    }
  }
}
```

### Relatórios

#### Gerar Relatório

```http
POST /relatorios/{vistoria_id}/gerar
Authorization: Bearer {token}
Content-Type: application/json

{
  "titulo": "Relatório - ABC-1234",
  "descricao": "Vistoria completa do veículo"
}

RESPONSE 200:
{
  "id": 1,
  "vistoria_id": 1,
  "titulo": "Relatório - ABC-1234",
  "descricao": "Vistoria completa do veículo",
  "status": "pronto",
  "caminho_pdf": "./uploads/vistorias/pdfs/relatorio_1_20260909121548.pdf",
  "criado_em": "2026-09-09T12:15:48Z",
  "gerado_em": "2026-09-09T12:16:00Z"
}
```

#### Download Relatório

```http
GET /relatorios/{relatorio_id}/download
Authorization: Bearer {token}

RESPONSE 200:
[Binary PDF File]
```

## Status Codes

| Code | Significado |
|------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

## Erros

```json
{
  "detail": "Email já cadastrado"
}
```

## Rate Limiting

Não há limitação de requisições atualmente. Para produção, considere adicionar rate limiting.

## Paginação

Listagens suportam:

```
?skip=0&limit=20
```

## Filtros

Vistorias podem ser filtradas por:

```
GET /vistorias?status=pendente
GET /vistorias?placa=ABC-1234
```

---

**Última atualização**: 2026-09-09
