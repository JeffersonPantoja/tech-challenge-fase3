# Plano Técnico - Fine-tuning no Google Colab

## Objetivo

Executar o fine-tuning em ambiente Google Colab, mantendo o código local responsável pela preparação do dataset e seguindo o padrão atual do projeto com `UseCase` e separação por camadas.

## Referências

- `documentos/wiki-referencia/requisitos_finetuning_llm.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-01-Preparando-dados-de-treinamento-para-fine-tuning/README.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-02-Fine-tuning-de-LLM-para-documentos/README.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-03-RAG-para-documentos/README.md`

## Escopo

- Gerar localmente o dataset final em `resources/finetuning_qa.jsonl`.
- Enviar manualmente esse arquivo para o Google Drive.
- Executar o treinamento no Colab.
- Registrar parâmetros, artefatos e resultado final no repositório.

## Fluxo Geral

1. O código local lê `MedQuAD` e `PubMedQA`.
2. O `UseCase` aplica curadoria e prepara os registros.
3. O writer exporta `resources/finetuning_qa.jsonl`.
4. O arquivo JSONL é enviado manualmente ao Google Drive.
5. O notebook no Colab monta o Drive, carrega o dataset e executa o fine-tuning.
6. O modelo ajustado e os artefatos do treino são salvos no Drive.

## Etapas do Projeto

### T1 - Preparação local do dataset

- Manter o fluxo atual do projeto em clean architecture.
- Produzir o dataset em JSONL para consumo no Colab.
- Garantir que cada linha siga o formato compatível com o modelo de treino.


### T2 - Transferência manual para o Drive (odesenvolvedor fará essa etapa)

- Enviar `resources/finetuning_qa.jsonl` manualmente para o Google Drive.
- Padronizar o caminho de acesso no notebook do Colab.
- Manter o dataset fora do repositório remoto quando necessário por tamanho.

### T3 - Notebook de fine-tuning no Colab

- Instalar dependências no ambiente do Colab.
- Carregar o dataset do Drive.
- Definir o modelo base open-source.
- Configurar o treino com parâmetros viáveis para Colab.
- Executar o ajuste fino e persistir o resultado.

### T4 - Verificação do modelo treinado

- Rodar prompts de teste no próprio notebook.
- Comparar comportamento antes e depois do ajuste fino.
- Registrar observações, limitações e qualidade das respostas.

### T5 - Documentação final

- Registrar os parâmetros usados no treino.
- Documentar o fluxo completo no repositório.
- Manter a wiki do projeto alinhada ao processo executado.

## Arquivos da Wiki de Referência

- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/README.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-01-Preparando-dados-de-treinamento-para-fine-tuning/README.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-02-Fine-tuning-de-LLM-para-documentos/README.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-03-RAG-para-documentos/README.md`
- `documentos/wiki-referencia/requisitos_finetuning_llm.md`

## Critérios de Conclusão

- `resources/finetuning_qa.jsonl` gerado localmente.
- Dataset enviado manualmente ao Google Drive.
- Fine-tuning executado no Colab com resultado salvo.
- Documentação do processo atualizada no repositório.
