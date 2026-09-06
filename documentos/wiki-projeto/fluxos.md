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
2. O notebook em `src/notebooks/fine-tuning-colab.ipynb` monta o Drive e autentica no Hugging Face com `HF_TOKEN`.
3. O `datasets.load_dataset` lê o JSONL e separa treino e teste com `train_test_split`.
4. O `unsloth.FastLanguageModel` carrega o `meta-llama/Llama-3.2-1B-Instruct` em 4-bit.
5. O tokenizer processa o campo `text` e o notebook aplica `QLoRA` com `FastLanguageModel.get_peft_model`.
6. O `trl.SFTTrainer` executa o treinamento com `TrainingArguments` e retomada de checkpoint quando existir.
7. O adapter é mesclado no modelo base e o modelo completo é salvo no diretório final.
8. Um prompt de validação é executado ao final do notebook.

## Fluxo do assistente médico

1. O `MedicalAssistantController` lê os argumentos da CLI.
2. O `LoadMedicalAssistantUseCase` valida o diretório do modelo local.
3. O `LocalMedicalAssistantRuntimeLoader` carrega o tokenizer e a LLM customizada, escolhendo entre modelo local mesclado e adapter.
4. O `LangChainMedicalAssistantResponseGenerator` monta o prompt e a cadeia de resposta.
5. O `AskMedicalAssistantUseCase` envia apenas a pergunta normalizada para a cadeia.
6. A LLM é exposta ao LangChain via `HuggingFacePipeline`.
7. O `MedicalAssistantController` registra pergunta e resposta em memória local da sessão.

## Fluxo do notebook no Colab

1. O Colab monta o Google Drive.
2. O notebook clona o repositório por HTTPS em uma célula separada para permitir atualização.
3. O notebook aponta `MODEL_PATH` para o modelo mesclado salvo no Drive, que precisa conter `config.json` e `model.safetensors`.
4. O notebook instala as dependências inline no próprio Colab.
5. Os usecases são instanciados diretamente no notebook.
6. O loop interativo faz chamadas diretas a `AskMedicalAssistantUseCase`.

## Formato final

```text
ANSWER THE QUESTION.
[|Context|] ...[|eContext|]

[|Question|] ...[|eQuestion|]

[|Answer|] ...[|eAnswer|]
```

Se não houver contexto, o bloco `Context` não é incluído.
