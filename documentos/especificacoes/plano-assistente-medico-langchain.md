# Especificação - Criação de Assistente Médico com LangChain

## Objetivo

Utilizar LangChain para criar um assistente médico que integre a LLM customizada e responda com base em prontuários sintéticos gerados a partir de `MedQuAD` e `PubMedQA`.

## Referências

- `documentos/wiki-referencia/langchain/README.md`
- `resources/medqa-finetuned-model`

## Escopo

- Construir um pipeline com LangChain integrando a LLM customizada.
- Gerar prontuários fictícios a partir dos datasets públicos `MedQuAD` e `PubMedQA`.
- Preservar a identificação de origem do dataset em cada prontuário sintético.
- Salvar os prontuários gerados em formato JSONL para consumo posterior.
- Contextualizar as respostas com informações estruturadas do paciente.

## Fluxo Geral

1. O sistema carrega a LLM customizada.
2. A etapa de geração cria uma base de prontuários sintéticos usando `MedQuAD` e `PubMedQA` como entrada.
3. A API da OpenAI é usada para transformar cada item de origem em um prontuário fictício estruturado.
4. Cada registro é salvo em JSONL com rastreabilidade da fonte original.
5. O LangChain orquestra a entrada do usuário, a consulta às bases estruturadas e a montagem do contexto.
6. A resposta é gerada pela LLM com base no contexto consolidado.

## Etapas do Projeto

### Integração da LLM

- Validar a presença de `resources/medqa-finetuned-model`.
- Definir a forma de carregamento da LLM customizada no runtime.
- Expor a LLM para uso pela camada LangChain.

### Pipeline LangChain

- Criar o pipeline de orquestração com LangChain.
- Integrar a LLM customizada à cadeia de processamento.
- Centralizar a composição da entrada e da saída do assistente.
- Responder perguntas através do modelo carregado

### Geração de prontuários sintéticos

- Definir a estrutura padrão do prontuário sintético.
- Usar `MedQuAD` e `PubMedQA` como base de origem dos casos.
- Fazer requisições à API da OpenAI para converter cada registro em prontuário fictício.
- Manter o mesmo identificador de origem do dataset nos prontuários gerados.
- Salvar o resultado consolidado em JSONL.

### Consulta a dados estruturados

- Consultar prontuários e registros estruturados.
- Selecionar os dados relevantes do paciente para a resposta.
- Preservar rastreabilidade da origem dos dados consultados.

### Contextualização da resposta

- Montar o contexto final com dados do paciente e a pergunta atual.
- Gerar respostas contextualizadas pela LLM.
- Manter o fluxo preparado para atualização contínua das informações do paciente.

### Implementação da consulta a dados estruturados

- Ler `resources/patient_records.jsonl` sem alterar o arquivo original.
- Usar `patient_id` sequencial como identificador único durante a estruturação dos documentos RAG.
- Indexar os prontuários com embeddings e FAISS.
- Recuperar documentos por similaridade semântica e, quando informado, filtrar por `patient_id`.
- Preservar o `source` dos documentos recuperados para rastreabilidade.

### Implementação da contextualização da resposta

- Receber os documentos recuperados pela etapa de consulta.
- Montar o contexto clínico com os dados estruturados do paciente.
- Encadear recuperação, montagem de contexto e geração com LangGraph.
- Usar o template textual compatível com o fine-tuning.
- Gerar a resposta com o modelo local fine-tuned.
- Detectar o idioma e traduzir a pergunta para inglês antes dos nós de recuperação e geração usando a API da OpenAI.
- Traduzir a resposta gerada pelo modelo fine-tuned para o idioma original usando a API da OpenAI.
- Retornar a resposta junto com o `source` dos documentos utilizados.

### Validação

- Testar consultas com diferentes perfis de paciente e tipos de pergunta.
- Verificar se a resposta usa os dados corretos do contexto.
- Confirmar que a atualização das informações altera a resposta quando necessário.

### Documentação

- Atualizar a wiki do projeto com o fluxo da nova fase.
- Registrar as decisões de integração e consulta aos dados.

## Critérios de Conclusão

- A LLM customizada está integrada ao LangChain.
- Os prontuários sintéticos foram gerados a partir de `MedQuAD` e `PubMedQA`.
- O pipeline consulta dados estruturados do paciente.
- As respostas são contextualizadas com informações atualizadas.
- A documentação da fase foi atualizada.
