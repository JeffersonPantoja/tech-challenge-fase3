from dataclasses import dataclass


@dataclass(frozen=True)
class MedicalAssistantMessage:
    role: str
    content: str
