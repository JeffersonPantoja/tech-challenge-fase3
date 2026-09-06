from __future__ import annotations

from src.application.ports import MedicalAssistantResponseGenerator


class AskMedicalAssistantUseCase:
    def __init__(self, responder: MedicalAssistantResponseGenerator) -> None:
        self._responder = responder

    def execute(self, question: str) -> str:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("A pergunta não pode estar vazia")

        return self._responder.generate(question=normalized_question)
