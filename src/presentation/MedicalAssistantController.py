from __future__ import annotations

import argparse
from pathlib import Path

from src.application.LoadMedicalAssistantUseCase import LoadMedicalAssistantUseCase
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.infrastructure.LocalMedicalAssistantRuntimeLoader import LocalMedicalAssistantRuntimeLoader


class MedicalAssistantController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Carrega a LLM customizada para o assistente médico.")
        self._parser.add_argument("--model-dir", default="resources/medqa-finetuned-model")
        self._parser.add_argument("--base-model", default=None)

    def run(self) -> None:
        args = self._parser.parse_args()
        options = MedicalAssistantCommandOptions(
            model_dir=Path(args.model_dir),
            base_model_name=args.base_model,
        )

        loader = LocalMedicalAssistantRuntimeLoader()
        use_case = LoadMedicalAssistantUseCase(loader=loader)
        runtime = use_case.execute(options)

        print(f"Modelo carregado em: {runtime.model_dir}")
        print(f"Base model: {runtime.base_model_name or 'auto'}")
        print(f"LLM LangChain: {runtime.pipeline_type}")
        print(f"Tokenizer: {runtime.tokenizer_name}")
