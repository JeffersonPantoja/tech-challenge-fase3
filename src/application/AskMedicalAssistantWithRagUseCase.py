from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.application.PatientRecordRetriever import PatientRecordRetriever
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime
from src.domain.PatientRecordDocument import PatientRecordDocument
from src.domain.RagAnswer import RagAnswer


class _RagState(TypedDict, total=False):
    question: str
    patient_id: str | None
    documents: list[PatientRecordDocument]
    context: str
    answer: str


class AskMedicalAssistantWithRagUseCase:
    def __init__(self, runtime: MedicalAssistantRuntime, retriever: PatientRecordRetriever) -> None:
        self._runtime = runtime
        self._retriever = retriever
        self._response_chain = (
            PromptTemplate.from_template(
                "ANSWER THE QUESTION.\n"
                "[|Context|] {context}[|eContext|]\n\n"
                "[|Question|] {question}[|eQuestion|]\n\n"
                "[|Answer|]"
            )
            | runtime.llm
            | StrOutputParser()
        )
        graph = StateGraph(_RagState)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("build_context", self._build_context)
        graph.add_node("generate", self._generate)
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "build_context")
        graph.add_edge("build_context", "generate")
        graph.add_edge("generate", END)
        self._graph = graph.compile()

    def execute(
        self,
        question: str,
        patient_id: str | None = None,
    ) -> RagAnswer:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("A pergunta não pode estar vazia")
        result = self._graph.invoke({"question": normalized_question, "patient_id": patient_id})
        documents = result.get("documents", [])
        return RagAnswer(
            answer=str(result.get("answer", "")).strip(),
            sources=[document.source for document in documents],
        )

    def _retrieve(self, state: _RagState) -> _RagState:
        documents = self._retriever.retrieve(state["question"], state.get("patient_id"))
        return {"documents": documents}

    def _build_context(self, state: _RagState) -> _RagState:
        documents = state.get("documents", [])
        context = "\n\n---\n\n".join(
            f"Source: {document.source}\n{document.content}" for document in documents
        )
        return {"context": context or "No relevant patient record was found."}

    def _generate(self, state: _RagState) -> _RagState:
        response = self._response_chain.invoke(
            {"context": state["context"], "question": state["question"]}
        )
        return {"answer": response.strip()}
