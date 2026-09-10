from __future__ import annotations

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from src.application.PatientRecordRetriever import PatientRecordRetriever
from src.domain.PatientRecordDocument import PatientRecordDocument


class FaissPatientRecordRetriever(PatientRecordRetriever):
    def __init__(
        self,
        documents: list[PatientRecordDocument],
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        top_k: int = 4,
    ) -> None:
        if not documents:
            raise ValueError("Nenhum prontuário disponível para indexação RAG")
        self._documents = documents
        self._top_k = max(1, top_k)
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        langchain_documents = [
            Document(
                page_content=document.content,
                metadata={
                    "patient_id": document.patient_id,
                    "source": document.source,
                },
            )
            for document in documents
        ]
        self._index = FAISS.from_documents(langchain_documents, embeddings)

    def retrieve(
        self,
        question: str,
        patient_id: str | None = None,
    ) -> list[PatientRecordDocument]:
        if patient_id:
            filtered = [document for document in self._documents if document.patient_id == patient_id]
            if not filtered:
                return []
            return self._rank_filtered(question, filtered)

        results = self._index.similarity_search(question, k=self._top_k)
        by_source = {document.source: document for document in self._documents}
        return [by_source[result.metadata["source"]] for result in results]

    def _rank_filtered(self, question: str, documents: list[PatientRecordDocument]) -> list[PatientRecordDocument]:
        # Keep patient filtering deterministic; semantic ranking is applied by a temporary index.
        embeddings = self._index.embedding_function
        index = FAISS.from_documents(
            [Document(page_content=document.content, metadata={"source": document.source}) for document in documents],
            embeddings,
        )
        results = index.similarity_search(question, k=min(self._top_k, len(documents)))
        by_source = {document.source: document for document in documents}
        return [by_source[result.metadata["source"]] for result in results]
