from __future__ import annotations

import logging
import os
from typing import Any

from src.application.ObservabilityTracer import ObservabilityTracer

logger = logging.getLogger(__name__)


class LangfuseObservabilityTracer(ObservabilityTracer):
    def __init__(self) -> None:
        self._handler: Any | None = None
        self._client: Any | None = None
        if not self._is_configured():
            return
        try:
            from langfuse import Langfuse
            from langfuse.langchain import CallbackHandler

            self._client = Langfuse()
            self._handler = CallbackHandler()
        except Exception:  # noqa: BLE001
            logger.exception("Não foi possível inicializar o tracing do Langfuse")

    @property
    def enabled(self) -> bool:
        return self._handler is not None

    def callbacks(self) -> list[Any]:
        return [self._handler] if self._handler is not None else []

    def trace_openai_call(self, name: str, prompt: str, output: str) -> None:
        if self._client is None:
            return
        try:
            input_value: object = prompt if self._capture_content else {"length": len(prompt)}
            output_value: object = output if self._capture_content else {"length": len(output)}
            with self._client.start_as_current_observation(
                as_type="generation",
                name=name,
                input=input_value,
            ) as generation:
                generation.update(output=output_value)
        except Exception:  # noqa: BLE001
            logger.exception("Falha ao registrar chamada OpenAI no Langfuse")

    def flush(self) -> None:
        if self._client is None:
            return
        try:
            self._client.flush()
        except Exception:  # noqa: BLE001
            logger.exception("Falha ao enviar traces ao Langfuse")

    @property
    def _capture_content(self) -> bool:
        return os.getenv("LANGFUSE_CAPTURE_CONTENT", "false").lower() == "true"

    def _is_configured(self) -> bool:
        return bool(
            os.getenv("LANGFUSE_PUBLIC_KEY")
            and os.getenv("LANGFUSE_SECRET_KEY")
            and os.getenv("LANGFUSE_HOST")
        )
