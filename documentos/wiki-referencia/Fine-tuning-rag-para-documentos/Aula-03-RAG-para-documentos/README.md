# Aula 03 - RAG para documentos

Esta aula aborda a construção de uma aplicação RAG para consulta de documentos.

O PDF `POSTECH - Aula 3.pdf` reforça a ideia de recuperar contexto antes da geração da resposta.

## Arquivos

- `POSTECH - Aula 3.pdf`: material base da aula com foco em RAG.
- `rag-application.ipynb`: notebook principal da aplicação RAG.
- `CNN_Links.txt`: base de links/documentos usada como fonte.

## Pontos principais

- Instalação e uso de bibliotecas de orquestração de LLM.
- Integração com Google Drive/Colab.
- Carregamento de documentos a partir de uma lista de links.
- Uso de embeddings para recuperação semântica.

## Relação com o projeto

- Reforça a etapa de busca e recuperação de conhecimento sobre documentos.
- Pode ser usado como referência para a camada de consulta do sistema.
- Para a T3, é a referência mais próxima de enriquecer a pergunta com contexto recuperado antes de chamar o modelo local.
