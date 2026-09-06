from __future__ import annotations

from pathlib import Path
from typing import Callable

import torch
from langchain_core.runnables import RunnableLambda
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from src.application.ports import MedicalAssistantRuntimeLoader
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


class LocalMedicalAssistantRuntimeLoader(MedicalAssistantRuntimeLoader):
    _MODEL_CONFIG_FILE = "config.json"
    _MODEL_WEIGHTS_FILE = "model.safetensors"
    _MAX_NEW_TOKENS = 128
    _REPETITION_PENALTY = 1.05

    def load(self, options: MedicalAssistantCommandOptions) -> MedicalAssistantRuntime:
        self._validate_model_directory(options.model_dir)

        tokenizer = self._load_tokenizer(options.model_dir)
        model = self._load_model(options.model_dir)
        self._configure_generation(model, options.model_dir)
        model.eval()

        llm = RunnableLambda(self._build_generate_text(tokenizer, model))
        return MedicalAssistantRuntime(
            model_dir=Path(options.model_dir),
            base_model_name=options.base_model_name,
            pipeline_type=llm.__class__.__name__,
            tokenizer_name=tokenizer.__class__.__name__,
            llm=llm,
        )

    def _validate_model_directory(self, model_dir: Path) -> None:
        if not (model_dir / self._MODEL_CONFIG_FILE).exists() or not (model_dir / self._MODEL_WEIGHTS_FILE).exists():
            raise FileNotFoundError(
                f"Modelo local mesclado não encontrado em {model_dir}. "
                "Rerode o notebook de fine-tuning para gerar o modelo completo."
            )

    def _load_tokenizer(self, model_dir: Path):
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_dir),
            use_fast=True,
            local_files_only=True,
            fix_mistral_regex=True,
            clean_up_tokenization_spaces=False,
        )
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    def _load_model(self, model_dir: Path):
        if torch.cuda.is_available():
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        else:
            dtype = torch.float32

        return AutoModelForCausalLM.from_pretrained(
            str(model_dir),
            dtype=dtype,
            device_map="auto",
            low_cpu_mem_usage=True,
            local_files_only=True,
        )

    def _configure_generation(self, model: object, model_dir: Path) -> None:
        model.generation_config = GenerationConfig.from_pretrained(str(model_dir), local_files_only=True)
        model.generation_config.max_new_tokens = self._MAX_NEW_TOKENS
        model.generation_config.do_sample = False
        model.generation_config.repetition_penalty = self._REPETITION_PENALTY
        model.generation_config.temperature = 1.0
        model.generation_config.top_p = None
        model.generation_config.max_length = None

    def _build_generate_text(self, tokenizer: object, model: object) -> Callable[[object], str]:
        def generate_text(prompt_value: object) -> str:
            prompt_text = prompt_value.to_string() if hasattr(prompt_value, "to_string") else str(prompt_value)
            inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
            with torch.inference_mode():
                output_ids = model.generate(**inputs)

            generated_ids = output_ids[0][inputs["input_ids"].shape[-1] :]
            return tokenizer.decode(
                generated_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            ).strip()

        return generate_text
