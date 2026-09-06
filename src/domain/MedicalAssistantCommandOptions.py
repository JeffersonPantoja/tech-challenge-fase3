from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MedicalAssistantCommandOptions:
    model_dir: Path
    base_model_name: str | None = None
    use_local_model: bool = False
