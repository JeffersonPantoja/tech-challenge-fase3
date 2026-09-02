# Fluxos

## Fluxo de dataset

1. O `MedQaController` lê os argumentos da CLI.
2. O `BuildMedQaDatasetUseCase` chama o reader de fontes.
3. O `MedQaSourcesReader` percorre `MedQuAD` e `PubMedQA` em modo incremental.
4. O `QARecordCurationService` limpa e deduplica os registros.
5. Cada `QARecord` é convertido em `text` com marcadores.
6. O `JsonDatasetWriter` grava o JSONL final progressivamente em `resources/finetuning_qa.jsonl`.

## Fluxo de fine-tuning no Colab

1. O dataset `resources/finetuning_qa.jsonl` é enviado manualmente ao Google Drive.
2. O notebook em `src/notebooks/fine-tuning-colab.ipynb` monta o Drive.
3. O `datasets.load_dataset` lê o JSONL e separa treino e teste.
4. O `transformers` carrega o modelo base em 4-bit.
5. O `trl.SFTTrainer` aplica `LoRA` e executa o treinamento.
6. O modelo ajustado e o tokenizer são salvos no Drive.
7. Um prompt de validação é executado ao final do notebook.

## Formato final

```text
ANSWER THE QUESTION.
[|Context|] ...[|eContext|]

[|Question|] ...[|eQuestion|]

[|Answer|] ...[|eAnswer|]
```

Se não houver contexto, o bloco `Context` não é incluído.
