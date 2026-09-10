from dataclasses import dataclass, field


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    sources: list[str] = field(default_factory=list)
