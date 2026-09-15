# Execução pela CLI

O código em `src/` possui entradas independentes para preparar o dataset, gerar prontuários sintéticos, normalizar identificadores e executar os assistentes. Os comandos devem ser executados a partir da raiz do repositório.

## Preparar o dataset de fine-tuning

```bash
python3 -m src.main \
  --resources-dir resources \
  --output resources/finetuning_qa.jsonl
```

O comando lê `MedQuAD` e `PubMedQA`, aplica curadoria e grava um objeto JSON por linha com `source` e `text`. Os argumentos disponíveis são `--resources-dir` e `--output`.

## Gerar prontuários sintéticos

```bash
python3 -m src.main_synthetic_records \
  --resources-dir resources \
  --output resources/patient_records.jsonl \
  --backend openai \
  --batch-size 10
```

Principais opções:

- `--backend openai|llama`: seleciona o gerador via OpenAI ou o modelo local/Hugging Face.
- `--openai-model`: modelo da OpenAI, padrão `gpt-4o-mini`.
- `--llama-model-path`: caminho do modelo usado pelo backend Llama.
- `--llama-max-new-tokens`: limite de tokens gerados pelo backend Llama, padrão `512`.
- `--batch-size`: quantidade de casos por lote, padrão `10`.
- `--num-batches`: limita a quantidade de lotes processados.
- `--checkpoint`: checkpoint de registros concluídos, padrão `resources/patient_records.checkpoint.json`.
- `--failed-checkpoint`: checkpoint de lotes falhos, padrão `resources/patient_records.failed.checkpoint.json`.
- `--resume` e `--no-resume`: habilita ou desabilita a retomada, habilitada por padrão no controller.
- `--save-to-drive` e `--drive-dir`: direciona saída e checkpoints para um diretório do Google Drive.

O backend OpenAI exige `OPENAI_API_KEY`. Os dois backends retornam registros validados por `source`; itens ausentes, inesperados ou duplicados invalidam o lote.

## Variáveis de ambiente

- `OPENAI_API_KEY`: obrigatória para os geradores, tradutor e revisor que usam OpenAI.
- `HF_TOKEN`: secret usado pelo notebook de fine-tuning para autenticar no Hugging Face.
- `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` e `LANGFUSE_HOST`: habilitam o tracing opcional.
- `LANGFUSE_CAPTURE_CONTENT`: controla a captura do conteúdo no tracing; o padrão é `false`.

## Normalizar IDs de pacientes

```bash
python3 -m src.main_normalize_patient_ids \
  --input resources/patient_records.jsonl \
  --output resources/patient_records_sequential.jsonl
```

O fluxo substitui `patient_id` por strings sequenciais iniciadas em `1`, preservando os demais campos. Os padrões de entrada e saída são os mostrados no comando.

## Assistente sem RAG

```bash
python3 -m src.main_langchain \
  --model-dir resources/medqa-finetuned-model
```

O modelo local mesclado é carregado e consultado em um loop interativo. `--base-model` pode ser informado quando o diretório salvo é um adapter que precisa de um modelo base explícito. Os comandos `sair`, `exit` e `quit` encerram a sessão.

## Assistente com RAG

```bash
python3 -m src.main_rag \
  --model-dir resources/medqa-finetuned-model \
  --patient-records resources/patient_records.jsonl \
  --top-k 4
```

Além dos caminhos do modelo e dos prontuários, o controller aceita `--embedding-model`, `--openai-model` e `--top-k`. Esse fluxo exige `OPENAI_API_KEY` para tradução e revisão. O comando interativo aceita `sair`, `exit`, `quit` e `/clear`; o último remove o paciente mantido na sessão.
