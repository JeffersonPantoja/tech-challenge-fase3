# Visão Geral

O projeto prepara dados médicos para fine-tuning de LLM a partir de duas bases principais:

- `MedQuAD`, em XML com pares de pergunta e resposta
- `PubMedQA`, em JSON com pergunta, contexto e resposta

## Estrutura de `resources`

- `resources/MedQuAD/`: base XML obtida de `https://github.com/abachaa/MedQuAD`
- `resources/pubmedqa/`: base JSON obtida de `https://pubmedqa.github.io/`
- `resources/finetuning_qa.json`: dataset final gerado para treino

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
4. Salvar o dataset final em JSON para treino supervisionado
