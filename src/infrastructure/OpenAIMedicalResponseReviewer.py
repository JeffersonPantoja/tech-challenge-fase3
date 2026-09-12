from __future__ import annotations

import os

from openai import OpenAI

from src.application.ports import MedicalResponseReviewer
from src.infrastructure.LangfuseObservabilityTracer import LangfuseObservabilityTracer


class OpenAIMedicalResponseReviewer(MedicalResponseReviewer):
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        client: OpenAI | None = None,
        observability: LangfuseObservabilityTracer | None = None,
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key and client is None:
            raise EnvironmentError("OPENAI_API_KEY não definida")
        self._client = client or OpenAI(api_key=api_key)
        self._model = model
        self._observability = observability

    def review(self, record_context: str, answer: str) -> str:
        prompt = f"""Review this medical assistant answer using the patient record.
Return only the revised answer, in the same language as the answer.
Keep the original answer first. Then add a blank line and a separate paragraph
starting exactly with "Revisão automática:".
Do not prescribe medication or treatment, give dosages, or tell the patient to
start, stop, or change treatment.
Preserve facts from the record and do not invent information.
If the record contains a diagnosis or treatment, append that the patient was
already diagnosed or received treatment according to the record.
Otherwise append that diagnosis and treatment must be evaluated by a specialized
health professional.

Expected format:
Original answer.

Revisão automática: The patient was already evaluated and the condition is a
possibility according to the record. Diagnosis and treatment require a health
professional's evaluation.

Patient record:
{record_context}

        Model answer:
        {answer}
        """
        try:
            response = self._client.responses.create(model=self._model, input=prompt)
            if self._observability:
                self._observability.trace_openai_call(
                    "review_medical_response", prompt, response.output_text
                )
            revised = response.output_text.strip()
            if revised:
                return revised
        except Exception:
            pass
        return (
            f"{answer.strip()}\n\n"
            "Revisão automática: O diagnóstico e o tratamento devem ser avaliados "
            "por um profissional de saúde especializado."
        )
