from __future__ import annotations

import argparse
from pathlib import Path

from src.application.AskMedicalAssistantWithRagUseCase import AskMedicalAssistantWithRagUseCase
from src.application.LoadMedicalAssistantUseCase import LoadMedicalAssistantUseCase
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.infrastructure.FaissPatientRecordRetriever import FaissPatientRecordRetriever
from src.infrastructure.JsonPatientRecordDocumentReader import JsonPatientRecordDocumentReader
from src.infrastructure.LocalMedicalAssistantRuntimeLoader import LocalMedicalAssistantRuntimeLoader


class RagMedicalAssistantController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Assistente médico com RAG sobre prontuários sintéticos.")
        self._parser.add_argument("--model-dir", default="resources/medqa-finetuned-model")
        self._parser.add_argument("--patient-records", default="resources/patient_records.jsonl")
        self._parser.add_argument("--embedding-model", default="sentence-transformers/all-MiniLM-L6-v2")
        self._parser.add_argument("--top-k", type=int, default=4)

    def run(self) -> None:
        args = self._parser.parse_args()
        runtime = LoadMedicalAssistantUseCase(LocalMedicalAssistantRuntimeLoader()).execute(
            MedicalAssistantCommandOptions(model_dir=Path(args.model_dir))
        )
        documents = JsonPatientRecordDocumentReader().read(Path(args.patient_records))
        retriever = FaissPatientRecordRetriever(
            documents=documents,
            embedding_model=args.embedding_model,
            top_k=args.top_k,
        )
        use_case = AskMedicalAssistantWithRagUseCase(runtime=runtime, retriever=retriever)

        print(f"Prontuários indexados: {len(documents)}")
        print("Digite uma pergunta ou 'sair' para encerrar.")
        while True:
            try:
                question = input("\nPergunta: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if question.lower() in {"sair", "exit", "quit"}:
                break
            if not question:
                continue

            patient_id = input("Patient ID (opcional): ").strip() or None
            result = use_case.execute(question, patient_id=patient_id)
            print(f"\nResposta: {result.answer}")
            print(f"Fontes: {', '.join(result.sources) or 'nenhuma'}")
