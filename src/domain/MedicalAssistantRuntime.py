from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MedicalAssistantRuntime:
    model_dir: Path
    base_model_name: str | None
    pipeline_type: str
    tokenizer_name: str
    llm: Any
