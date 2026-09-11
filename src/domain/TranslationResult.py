from dataclasses import dataclass


@dataclass(frozen=True)
class TranslationResult:
    language: str
    translated_text: str
