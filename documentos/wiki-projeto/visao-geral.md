# Visão Geral

O projeto prepara dados médicos para fine-tuning de LLM e usa o modelo resultante em um assistente médico com LangChain.

O fluxo geral começa com duas bases principais, que também servem como origem para prontuários sintéticos:

- `MedQuAD`, em XML com pares de pergunta e resposta
- `PubMedQA`, em JSON com pergunta, contexto e resposta

## Estrutura de `resources`

- `resources/MedQuAD/`: base XML obtida de `https://github.com/abachaa/MedQuAD`
- `resources/pubmedqa/`: base JSON obtida de `https://pubmedqa.github.io/`
- `resources/finetuning_qa.jsonl`: dataset final gerado para treino
- `resources/patient_records.jsonl`: base sintética planejada para prontuários fictícios

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

Na T3, cada item recebe um `source` completo com pasta, arquivo e identificador interno, e esses registros são enviados em lote para a API da OpenAI.

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
6. Gerar prontuários sintéticos a partir de `MedQuAD` e `PubMedQA` para a T3 do assistente médico
7. Processar os registros sintéticos em lotes com validação, retry e descarte de lotes inválidos
8. Salvar o modelo mesclado no Google Drive e usá-lo no assistente médico interativo
