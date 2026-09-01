from dataclasses import dataclass


@dataclass(frozen=True)
class QARecord:
    source: str
    question: str
    answer: str
    context: str = ""

    def to_finetuning_text(self) -> str:
        if self.context:
            return (
                "ANSWER THE QUESTION.\n"
                f"[|Context|] {self.context}[|eContext|]\n\n"
                f"[|Question|] {self.question}[|eQuestion|]\n\n"
                f"[|Answer|] {self.answer}[|eAnswer|]"
            )

        return (
            "ANSWER THE QUESTION.\n"
            f"[|Question|] {self.question}[|eQuestion|]\n\n"
            f"[|Answer|] {self.answer}[|eAnswer|]"
        )
