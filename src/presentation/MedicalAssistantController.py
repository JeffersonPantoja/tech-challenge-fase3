from __future__ import annotations

import argparse
from pathlib import Path

from src.application.AskMedicalAssistantUseCase import AskMedicalAssistantUseCase
from src.application.LoadMedicalAssistantUseCase import LoadMedicalAssistantUseCase
from src.domain.MedicalAssistantConversation import MedicalAssistantConversation
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.infrastructure.LocalMedicalAssistantRuntimeLoader import LocalMedicalAssistantRuntimeLoader
from src.infrastructure.LangChainMedicalAssistantResponseGenerator import LangChainMedicalAssistantResponseGenerator


class MedicalAssistantController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Carrega a LLM customizada para o assistente médico.")
        self._parser.add_argument("--model-dir", default="resources/medqa-finetuned-model")
        self._parser.add_argument("--base-model", default=None)
        self._parser.add_argument("--question", default=None, help="Pergunta inicial opcional; a sessão continua em modo interativo.")

    def run(self) -> None:
        args = self._parser.parse_args()
        options = MedicalAssistantCommandOptions(
            model_dir=Path(args.model_dir),
            base_model_name=args.base_model,
        )

        loader = LocalMedicalAssistantRuntimeLoader()
        use_case = LoadMedicalAssistantUseCase(loader=loader)
        runtime = use_case.execute(options)

        responder = LangChainMedicalAssistantResponseGenerator(runtime=runtime)
        ask_use_case = AskMedicalAssistantUseCase(responder=responder)
        conversation = MedicalAssistantConversation()

        print(f"Modelo carregado em: {runtime.model_dir}")
        print(f"Base model: {runtime.base_model_name or 'auto'}")
        print(f"LLM LangChain: {runtime.pipeline_type}")
        print(f"Tokenizer: {runtime.tokenizer_name}")

        if args.question:
            self._ask_once(args.question, ask_use_case, conversation)

        self._interactive_loop(ask_use_case, conversation)

    def _ask_once(
        self,
        question: str,
        use_case: AskMedicalAssistantUseCase,
        conversation: MedicalAssistantConversation,
    ) -> None:
        answer = use_case.execute(question)
        conversation.add_user_message(question)
        conversation.add_assistant_message(answer)
        print(f"\nResposta: {answer}")

    def _interactive_loop(
        self,
        use_case: AskMedicalAssistantUseCase,
        conversation: MedicalAssistantConversation,
    ) -> None:
        print("Digite uma pergunta ou 'sair' para encerrar.")
        while True:
            try:
                question = input("Pergunta: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if question.lower() in {"sair", "exit", "quit"}:
                break
            if not question:
                continue

            answer = use_case.execute(question)
            conversation.add_user_message(question)
            conversation.add_assistant_message(answer)
            print(f"Resposta: {answer}")
