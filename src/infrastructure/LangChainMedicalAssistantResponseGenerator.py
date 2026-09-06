from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.application.ports import MedicalAssistantResponseGenerator
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


SYSTEM_PROMPT = """ANSWER THE QUESTION.
[|Question|] {question}[|eQuestion|]

[|Answer|]"""


class LangChainMedicalAssistantResponseGenerator(MedicalAssistantResponseGenerator):
    def __init__(self, runtime: MedicalAssistantRuntime) -> None:
        self._runtime = runtime
        prompt = PromptTemplate.from_template(SYSTEM_PROMPT)
        self._chain = prompt | runtime.llm | StrOutputParser()

    def generate(self, question: str) -> str:
        response = self._chain.invoke({"question": question})
        return str(response).strip()
