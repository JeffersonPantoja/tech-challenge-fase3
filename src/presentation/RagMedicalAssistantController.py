from __future__ import annotations

import argparse
from pathlib import Path

from src.application.AskMedicalAssistantWithRagUseCase import AskMedicalAssistantWithRagUseCase
from src.application.LoadMedicalAssistantUseCase import LoadMedicalAssistantUseCase
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.infrastructure.FaissPatientRecordRetriever import FaissPatientRecordRetriever
from src.infrastructure.JsonPatientRecordDocumentReader import JsonPatientRecordDocumentReader
from src.infrastructure.LocalMedicalAssistantRuntimeLoader import LocalMedicalAssistantRuntimeLoader
from src.infrastructure.OpenAITranslator import OpenAITranslator
from src.infrastructure.LangfuseObservabilityTracer import LangfuseObservabilityTracer


class RagMedicalAssistantController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Assistente médico com RAG sobre prontuários sintéticos.")
        self._parser.add_argument("--model-dir", default="resources/medqa-finetuned-model")
        self._parser.add_argument("--patient-records", default="resources/patient_records.jsonl")
        self._parser.add_argument("--embedding-model", default="sentence-transformers/all-MiniLM-L6-v2")
        self._parser.add_argument("--translation-model", default="gpt-4o-mini")
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
        observability = LangfuseObservabilityTracer()
        translator = OpenAITranslator(model=args.translation_model, observability=observability)
        use_case = AskMedicalAssistantWithRagUseCase(
            runtime=runtime,
            retriever=retriever,
            translator=translator,
            observability=observability,
        )

        print(f"Prontuários indexados: {len(documents)}")
        print("Digite uma pergunta, 'sair' para encerrar ou '/clear' para limpar o paciente atual.")
        current_patient_id: str | None = None
        while True:
            try:
                question = input("\nPergunta: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            normalized_command = question.lower()
            if normalized_command in {"sair", "exit", "quit"}:
                break
            if normalized_command == "/clear":
                current_patient_id = None
                print("Paciente atual removido.")
                continue
            if not question:
                continue

            patient_prompt = (
                f"Patient ID [{current_patient_id}] (Enter para manter): "
                if current_patient_id
                else "Patient ID (opcional): "
            )
            patient_input = input(patient_prompt).strip()
            patient_id = patient_input or current_patient_id
            result = use_case.execute(question, patient_id=patient_id)
            current_patient_id = patient_id
            print(f"\nResposta: {result.answer}")
            print(f"Fontes: {', '.join(result.sources) or 'nenhuma'}")
        observability.flush()
