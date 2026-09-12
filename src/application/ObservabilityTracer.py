from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ObservabilityTracer(ABC):
    @abstractmethod
    def callbacks(self) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError
