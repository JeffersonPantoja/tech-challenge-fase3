from __future__ import annotations

import json
import os

from openai import OpenAI

from src.application.QuestionTranslator import QuestionTranslator
from src.domain.TranslationResult import TranslationResult


class OpenAIQuestionTranslator(QuestionTranslator):
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY não definida")
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def translate_question_to_english(self, question: str) -> TranslationResult:
        response = self._client.responses.create(
            model=self._model,
            input=(
                "Detect the language of the question and translate it to English.\n"
                "Return only valid JSON with the keys language and translated_text.\n"
                "Preserve patient IDs, medication names, measurements, and medical terms.\n\n"
                f"Question: {question}"
            ),
        )
        payload = self._parse_json(response.output_text)
        language = str(payload.get("language", "")).strip().lower()
        translated_text = str(payload.get("translated_text", "")).strip()
        if not language or not translated_text:
            raise ValueError("A API de tradução retornou um resultado incompleto")
        return TranslationResult(language=language, translated_text=translated_text)

    def translate_answer_from_english(self, answer: str, language: str) -> str:
        if language in {"en", "eng", "english"}:
            return answer
        response = self._client.responses.create(
            model=self._model,
            input=(
                f"Translate the following medical answer from English to {language}.\n"
                "Return only the translated answer. Preserve the exact meaning.\n"
                "Do not add or remove clinical information. Preserve patient IDs, "
                "medication names, measurements, and medical terms.\n\n"
                f"Answer: {answer}"
            ),
        )
        translated_answer = response.output_text.strip()
        if not translated_answer:
            raise ValueError("A API de tradução retornou uma resposta vazia")
        return translated_answer

    def _parse_json(self, content: str) -> dict[str, object]:
        normalized = content.strip()
        if normalized.startswith("```"):
            normalized = normalized.removeprefix("```json").removeprefix("```")
            normalized = normalized.removesuffix("```").strip()
        payload = json.loads(normalized)
        if not isinstance(payload, dict):
            raise ValueError("A API de tradução não retornou um objeto JSON")
        return payload
