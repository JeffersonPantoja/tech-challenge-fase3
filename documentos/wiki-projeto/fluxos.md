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
3. O `LocalMedicalAssistantRuntimeLoader` carrega o tokenizer e a LLM customizada a partir do modelo local mesclado.
4. O `LangChainMedicalAssistantResponseGenerator` monta o prompt e a cadeia de resposta.
5. O `AskMedicalAssistantUseCase` envia apenas a pergunta normalizada para a cadeia.
6. A LLM é exposta ao LangChain por uma função local que chama `model.generate` diretamente.
7. O `MedicalAssistantController` registra pergunta e resposta em memória local da sessão.

## Fluxo de prontuários sintéticos

1. A etapa de Geração de Prontuários Sintéticos usa registros de `MedQuAD` e `PubMedQA` como fonte de origem.
2. Cada item preserva o `source` completo com pasta, arquivo e identificador interno para rastreabilidade.
3. O `BuildSyntheticPatientRecordsUseCase` agrupa os registros em lotes configuráveis.
4. A API da OpenAI recebe um lote por chamada e devolve um JSON array com um item por `source`.
5. O lote é validado por `source`; se faltar, sobrar ou duplicar item, a execução tenta novamente até 3 vezes.
6. Se o lote continuar inválido após as 3 tentativas, ele é descartado e o fluxo segue para o próximo lote.
7. Os itens válidos são gravados incrementalmente em JSONL e o checkpoint é atualizado por registro processado.
8. A estrutura do prontuário deve permanecer consistente entre as fontes para facilitar consulta e validação.

## Prompt da geração

1. O prompt é escrito em inglês para o modelo responder com um `JSON array` válido.
2. Cada item de entrada inclui `source`, `QUESTION`, `ANSWER` e `CONTEXT`.
3. O modelo deve devolver exatamente um item por `source`, sem duplicar registros.
4. As chaves exigidas no retorno são `source`, `patient_id`, `chief_complaint`, `history`, `medications`, `vitals`, `assessment` e `plan`.
5. Se um caso não puder ser resolvido, o item ainda deve existir com o mesmo `source` e campos vazios ou mínimos.
6. O retorno não pode conter markdown, explicações ou texto fora do JSON.

### Formato final do prompt gerador de prontuários sintético

```text
Generate synthetic patient records in English for the cases below.
Respond only with a valid JSON array.
Each array item must contain exactly these keys: source, patient_id, chief_complaint, history, medications, vitals, assessment, plan.
The source field must be copied exactly from the input case.
The array order may differ from the input order, but every input source must appear exactly once.
If a case cannot be answered, still return an item with the same source and empty or minimal fields.
Do not duplicate any source.
Do not include markdown, explanations, or any text outside the JSON.
```

## Fluxo do notebook no Colab

1. O Colab monta o Google Drive.
2. O notebook clona o repositório por HTTPS em uma célula separada para permitir atualização.
3. O notebook aponta `MODEL_PATH` para o modelo mesclado salvo no Drive, que precisa conter `config.json` e `model.safetensors`.
4. O notebook instala as dependências inline no próprio Colab.
5. Os usecases são instanciados diretamente no notebook.
6. O loop interativo faz chamadas diretas a `AskMedicalAssistantUseCase`.

## Formato final do prompt do fine-tuning

```text
ANSWER THE QUESTION.
[|Context|] ...[|eContext|]

[|Question|] ...[|eQuestion|]

[|Answer|] ...[|eAnswer|]
```

Se não houver contexto, o bloco `Context` não é incluído.
