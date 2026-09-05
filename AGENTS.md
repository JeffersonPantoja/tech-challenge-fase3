# Repository Guide

## Run and verify

- Use Python 3.12+ in `.venv`: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Generate the fine-tuning dataset with `python3 -m src.main --resources-dir resources --output resources/finetuning_qa.jsonl`.
- There is no test, lint, formatter, typecheck, or CI configuration. Use `python3 -m compileall src` as the available baseline verification.

## Data pipeline

- Raw inputs are intentionally ignored by Git: place MedQuAD XML below `resources/MedQuAD/` and PubMedQA JSON files directly below `resources/pubmedqa/` before running the CLI.
- The output is JSONL, one object per record with `source` and `text`; do not change the `ANSWER THE QUESTION.` and `[|...|]` markers without coordinating the matching Colab training notebook.
- The CLI wiring is in `src/presentation/MedQaController.py`; the use case coordinates reading, curation, and writing.

## Code structure

- Preserve the dependency direction: `domain` holds immutable models, `application` defines ports and `BuildMedQaDatasetUseCase`, `infrastructure` implements source parsing/curation/writing, and `presentation` owns argparse and composition.
- Source modules deliberately use CamelCase filenames matching their exported classes.
- `documentos/wiki-projeto/` is the project decision log; update it when making an important architectural decision.
