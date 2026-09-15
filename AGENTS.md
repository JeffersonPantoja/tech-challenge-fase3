# Repository Guide

## Setup and verification
- Use Python 3.12+ from the repository root with `.venv`: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- There is no test, lint, typecheck, or CI configuration. Run `python3 -m compileall src` and `git diff --check` for baseline verification.
- `.env` is not loaded automatically; export variables or use `set -a; source .env; set +a`. Never commit `.env` or API keys.

## Inputs and commands
- `resources/MedQuAD/` and `resources/pubmedqa/` are required local inputs and are not versioned. Generate the QA dataset with `python3 -m src.main --resources-dir resources --output resources/finetuning_qa.jsonl`.
- Generate synthetic records with `python3 -m src.main_synthetic_records --backend openai --resources-dir resources --output resources/patient_records.jsonl`; it resumes from checkpoints by default. Use `--no-resume` to restart, and `OPENAI_API_KEY` is required for the OpenAI backend.
- Normalize IDs with `python3 -m src.main_normalize_patient_ids --input resources/patient_records.jsonl --output resources/patient_records_sequential.jsonl`.
- The local assistant entrypoint is `python3 -m src.main_langchain --model-dir resources/medqa-finetuned-model`; the RAG entrypoint is `python3 -m src.main_rag --model-dir resources/medqa-finetuned-model --patient-records resources/patient_records.jsonl` and requires `OPENAI_API_KEY`.
- The assistant entrypoints require a locally generated merged model containing `config.json`, `model.safetensors`, and tokenizer files. Fine-tuning is performed by `src/notebooks/fine-tuning-colab.ipynb`.

## Boundaries and contracts
- Keep immutable models in `src/domain`, ports and use cases in `src/application`, concrete I/O/LLM/RAG integrations in `src/infrastructure`, and CLI composition in `src/presentation`.
- Module filenames intentionally use CamelCase to match exported class names.
- Dataset output is UTF-8 JSONL with `source` and `text`. Preserve `ANSWER THE QUESTION.` and the `[|Context|]`, `[|Question|]`, and `[|Answer|]` markers unless the matching Colab notebook is updated too.
- Important architectural decisions belong in `documentos/wiki-projeto/`; keep that wiki synchronized with non-trivial changes.
