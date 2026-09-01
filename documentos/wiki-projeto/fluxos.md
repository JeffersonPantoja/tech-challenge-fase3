# Fluxos

## Fluxo de dataset

1. O `MedQaController` lê os argumentos da CLI.
2. O `BuildMedQaDatasetUseCase` chama o reader de fontes.
3. O `MedQaSourcesReader` percorre `MedQuAD` e `PubMedQA` em modo incremental.
4. O `QARecordCurationService` limpa e deduplica os registros.
5. Cada `QARecord` é convertido em `text` com marcadores.
6. O `JsonDatasetWriter` grava o JSON final progressivamente em `resources/finetuning_qa.json`.

## Formato final

```text
ANSWER THE QUESTION.
[|Context|] ...[|eContext|]

[|Question|] ...[|eQuestion|]

[|Answer|] ...[|eAnswer|]
```

Se não houver contexto, o bloco `Context` não é incluído.
