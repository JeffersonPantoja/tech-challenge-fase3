# Repository Guide

## Run and verify
- Use Python 3.12+ with `.venv`: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Generate the dataset with `python3 -m src.main --resources-dir resources --output resources/finetuning_qa.jsonl`.
- Baseline verification is `python3 -m compileall src`; there is no repo test/lint/typecheck/CI config.

## Data pipeline
- Raw inputs live in `resources/MedQuAD/` and `resources/pubmedqa/`; the CLI reads those paths directly.
- The dataset writer outputs JSONL with one object per line: `source` and `text`.
- Do not change the `ANSWER THE QUESTION.` prompt or `[|...|]` markers without updating the matching Colab notebook.
- `src/presentation/MedQaController.py` wires the dataset CLI; `BuildMedQaDatasetUseCase` owns read -> curate -> write.

## Code structure
- Keep `domain` for immutable models, `application` for ports/use cases, `infrastructure` for parsing/curation/writing, and `presentation` for CLI/composition.
- Source modules intentionally use CamelCase filenames that match their exported classes.
- `src/main.py` runs dataset generation; `src/main_langchain.py` runs the medical assistant CLI.
- `documentos/wiki-projeto/` is the project decision log; update it for important architectural changes.
