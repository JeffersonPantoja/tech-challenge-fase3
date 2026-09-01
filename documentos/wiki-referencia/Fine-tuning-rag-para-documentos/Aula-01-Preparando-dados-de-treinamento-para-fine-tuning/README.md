# Aula 01 - Preparando dados de treinamento para fine-tuning

Esta aula cobre a coleta, extração e preparação de dados para criação de dataset de fine-tuning.

## Arquivos

- `news-scrapper.ipynb`: coleta links de notícias e organiza a base inicial de entrada.
- `get-news-content.ipynb`: acessa o conteúdo bruto das notícias a partir dos links coletados.
- `generate-output-for-news.ipynb`: gera saídas/resumos para as notícias processadas.
- `prepare-data.ipynb`: consolida os dados em formato de treinamento.
- `data.jsonl`: dataset final em formato JSONL.
- `news_contents.json`: conteúdo bruto das notícias.
- `news_summaries.json`: resumos produzidos.
- `news_dataset_chat_data.json`: versão estruturada para diálogo/chat.
- `CNN_Links.txt`: lista de links utilizados como fonte.

## Fluxo resumido

1. Coletar links de notícias.
2. Baixar e extrair o conteúdo textual.
3. Gerar resumos/saídas desejadas.
4. Consolidar tudo em arquivos JSON e JSONL para treinamento.

## Observações

- O conjunto de notebooks parece usar Google Drive/Colab como ambiente de execução.
- A etapa foca em preparar dados limpos e reutilizáveis para fine-tuning.
