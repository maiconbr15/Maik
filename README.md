# Extrator Veicular - GitHub Pages

Projeto 100% estático para uso no GitHub Pages.

## Como usar

1. Crie um repositório no GitHub.
2. Envie o arquivo `index.html` para a raiz do repositório.
3. Abra **Settings > Pages**.
4. Em **Build and deployment**, escolha **Deploy from a branch**.
5. Selecione a branch `main` e a pasta `/ (root)`.
6. Salve.
7. O GitHub mostrará o endereço público da página.

## Funcionamento

O sistema não usa servidor, banco de dados ou armazenamento.
Você copia o conteúdo textual da consulta veicular e cola na página.
A extração é feita em JavaScript diretamente no navegador.

## Observação

Por ser um projeto estático, ele não acessa automaticamente outros sites que bloqueiam requisições por CORS. Por isso, o método mais confiável é copiar e colar o conteúdo da consulta.

## Privacidade

Nada é enviado para nenhum servidor pelo código deste projeto.