# Visão Geral

O projeto prepara dados médicos para fine-tuning de LLM e usa o modelo resultante em um assistente médico com LangChain.

O fluxo geral começa com duas bases principais, que também servem como origem para prontuários sintéticos:

- `MedQuAD`, em XML com pares de pergunta e resposta
- `PubMedQA`, em JSON com pergunta, contexto e resposta

## Estrutura de `resources`

- `resources/MedQuAD/`: base XML obtida de `https://github.com/abachaa/MedQuAD`
- `resources/pubmedqa/`: base JSON obtida de `https://pubmedqa.github.io/`
- `resources/finetuning_qa.jsonl`: dataset final gerado para treino
- `resources/patient_records.jsonl`: prontuários sintéticos gerados para o fluxo RAG

## Módulos de `src`

### Domain

Modelos imutáveis e resultados: `QARecord`, `CurationResult`, `CurationStats`, `BuildDatasetResult`, `SyntheticPatientRecord`, `PatientRecordDocument`, `RagAnswer`, `TranslationResult`, `MedicalAssistantRuntime`, `MedicalAssistantConversation`, `MedicalAssistantMessage`, `SyntheticPatientRecordsCheckpoint` e os objetos de opções e resultados dos comandos.

### Application

Casos de uso: construção do dataset, geração de prontuários, normalização de IDs, carregamento do runtime, consulta simples, consulta RAG e interfaces para leitura, escrita, geração, tradução, recuperação, revisão, observabilidade e checkpoints.

### Infrastructure

Implementações de leitura e escrita JSONL, parsing de MedQuAD e PubMedQA, curadoria, geradores de prontuários via OpenAI e Llama, carregamento da LLM local, integração LangChain, embeddings com FAISS, tradução, revisão médica e tracing Langfuse.

### Presentation

Controllers de dataset, prontuários sintéticos, normalização, assistente simples e assistente RAG. Cada controller monta as dependências da aplicação e expõe uma CLI própria.

## Estrutura dos dados

Os registros centrais do pipeline ficam em `src/domain/`:

- `QARecord`
- `CurationStats`
- `CurationResult`
- `CommandOptions`
- `BuildDatasetResult`

### PubMedQA

Arquivos atuais:

- `ori_pqal.json`
- `ori_pqaa.json`
- `ori_pqau.json`

Cada item do JSON contém, em geral:

- `QUESTION`: pergunta principal
- `CONTEXTS`: lista de contextos ou trechos de apoio
- `LABELS`: rótulos/resposta curta
- `LONG_ANSWER`: resposta completa, quando disponível

### MedQuAD

Os arquivos são XML com estrutura semelhante a:

```xml
<Document>
  <Focus>...</Focus>
  <QAPairs>
    <QAPair>
      <Question>...</Question>
      <Answer>...</Answer>
    </QAPair>
  </QAPairs>
</Document>
```

Cada `QAPair` é convertido em um registro de treino com `question`, `answer` e `context` opcional.

Na Geração de Prontuários Sintéticos, cada item recebe um `source` completo com pasta, arquivo e identificador interno, e esses registros são enviados em lote para a API da OpenAI.

Pastas atuais dentro de `resources/MedQuAD/`:

- `1_CancerGov_QA`
- `2_GARD_QA`
- `3_GHR_QA`
- `4_MPlus_Health_Topics_QA`
- `5_NIDDK_QA`
- `6_NINDS_QA`
- `7_SeniorHealth_QA`
- `8_NHLBI_QA_XML`
- `9_CDC_QA`
- `10_MPlus_ADAM_QA`
- `11_MPlusDrugs_QA`
- `12_MPlusHerbsSupplements_QA`

Objetivo do fluxo atual:

1. Ler os dados brutos em `resources/`
2. Extrair `question`, `answer` e `context`
3. Converter cada item em texto único com marcadores
4. Salvar o dataset final em JSONL para treino supervisionado
5. Consumir o JSONL no notebook `src/notebooks/fine-tuning-colab.ipynb` para executar o fine-tuning
6. Gerar prontuários sintéticos a partir de `MedQuAD` e `PubMedQA` para a etapa de Geração de Prontuários Sintéticos do assistente médico
7. Processar os registros sintéticos em lotes com validação, retry e descarte de lotes inválidos
8. Salvar o modelo mesclado no Google Drive e usá-lo no assistente médico interativo

Os pontos de entrada são `src.main`, `src.main_synthetic_records`, `src.main_normalize_patient_ids`, `src.main_langchain` e `src.main_rag`. Os parâmetros e variáveis de ambiente estão detalhados em [Execução pela CLI](./execucao-cli.md).
