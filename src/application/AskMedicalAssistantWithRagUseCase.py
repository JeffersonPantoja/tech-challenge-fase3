from __future__ import annotations

import uuid
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.application.QuestionTranslator import QuestionTranslator
from src.application.ObservabilityTracer import ObservabilityTracer
from src.application.ports import MedicalResponseReviewer
from src.application.PatientRecordRetriever import PatientRecordRetriever
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime
from src.domain.PatientRecordDocument import PatientRecordDocument
from src.domain.RagAnswer import RagAnswer


class _RagState(TypedDict, total=False):
    original_question: str
    question: str
    language: str
    patient_id: str | None
    documents: list[PatientRecordDocument]
    context: str
    answer: str


class AskMedicalAssistantWithRagUseCase:
    def __init__(
        self,
        runtime: MedicalAssistantRuntime,
        retriever: PatientRecordRetriever,
        translator: QuestionTranslator,
        observability: ObservabilityTracer | None = None,
        response_reviewer: MedicalResponseReviewer | None = None,
    ) -> None:
        self._runtime = runtime
        self._retriever = retriever
        self._translator = translator
        self._observability = observability
        self._response_reviewer = response_reviewer
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
        graph.add_node("translate_question", self._translate_question)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("build_context", self._build_context)
        graph.add_node("generate", self._generate)
        graph.add_node("translate_answer", self._translate_answer)
        graph.add_node("review_output", self._review_output)
        graph.add_edge(START, "translate_question")
        graph.add_edge("translate_question", "retrieve")
        graph.add_edge("retrieve", "build_context")
        graph.add_edge("build_context", "generate")
        graph.add_edge("generate", "translate_answer")
        graph.add_edge("translate_answer", "review_output")
        graph.add_edge("review_output", END)
        self._graph = graph.compile()

    def execute(
        self,
        question: str,
        patient_id: str | None = None,
    ) -> RagAnswer:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("A pergunta não pode estar vazia")
        config: dict[str, object] = {}
        if self._observability:
            config["callbacks"] = self._observability.callbacks()
            config["metadata"] = {
                "request_id": str(uuid.uuid4()),
                "patient_id": patient_id,
            }
            config["run_name"] = "medical_assistant_request"
        result = self._graph.invoke(
            {"original_question": normalized_question, "patient_id": patient_id}, config=config
        )
        if self._observability:
            self._observability.flush()
        documents = result.get("documents", [])
        return RagAnswer(
            answer=str(result.get("answer", "")).strip(),
            sources=[
                f"{document.source} (ID do paciente: {document.patient_id})"
                for document in documents
            ],
        )

    def _retrieve(self, state: _RagState) -> _RagState:
        documents = self._retriever.retrieve(state["question"], state.get("patient_id"))
        return {"documents": documents}

    def _translate_question(self, state: _RagState) -> _RagState:
        translation = self._translator.translate_question_to_english(state["original_question"])
        return {"question": translation.translated_text, "language": translation.language}

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

    def _translate_answer(self, state: _RagState) -> _RagState:
        answer = self._translator.translate_answer_from_english(
            state["answer"], state["language"]
        )
        return {"answer": answer}

    def _review_output(self, state: _RagState) -> _RagState:
        if self._response_reviewer is None:
            return {}
        return {
            "answer": self._response_reviewer.review(
                record_context=state.get("context", ""),
                answer=state["answer"],
            )
        }
