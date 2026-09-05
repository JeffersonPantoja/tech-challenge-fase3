from __future__ import annotations

from src.application.ports import MedicalAssistantRuntimeLoader
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


class LoadMedicalAssistantUseCase:
    def __init__(self, loader: MedicalAssistantRuntimeLoader) -> None:
        self._loader = loader

    def execute(self, options: MedicalAssistantCommandOptions) -> MedicalAssistantRuntime:
        if not options.model_dir.exists():
            raise FileNotFoundError(f"Modelo não encontrado em {options.model_dir}")
        if not options.model_dir.is_dir():
            raise NotADirectoryError(f"Caminho inválido para o modelo: {options.model_dir}")

        return self._loader.load(options)
