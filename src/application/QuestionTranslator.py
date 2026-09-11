from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.TranslationResult import TranslationResult


class QuestionTranslator(ABC):
    @abstractmethod
    def translate_question_to_english(self, question: str) -> TranslationResult:
        raise NotImplementedError

    @abstractmethod
    def translate_answer_from_english(self, answer: str, language: str) -> str:
        raise NotImplementedError
