from __future__ import annotations

from pathlib import Path

import torch
from langchain_core.runnables import RunnableLambda
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from src.application.ports import MedicalAssistantRuntimeLoader
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


class LocalMedicalAssistantRuntimeLoader(MedicalAssistantRuntimeLoader):
    def load(self, options: MedicalAssistantCommandOptions) -> MedicalAssistantRuntime:
        tokenizer = AutoTokenizer.from_pretrained(
            str(options.model_dir),
            use_fast=True,
            local_files_only=True,
            fix_mistral_regex=True,
            clean_up_tokenization_spaces=False,
        )
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token

        if not (options.model_dir / "config.json").exists() or not (options.model_dir / "model.safetensors").exists():
            raise FileNotFoundError(
                f"Modelo local mesclado não encontrado em {options.model_dir}. "
                "Rerode o notebook de fine-tuning para gerar o modelo completo."
            )

        if torch.cuda.is_available():
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        else:
            dtype = torch.float32

        model = AutoModelForCausalLM.from_pretrained(
            str(options.model_dir),
            dtype=dtype,
            device_map="auto",
            low_cpu_mem_usage=True,
            local_files_only=True,
        )
        model.generation_config = GenerationConfig.from_pretrained(str(options.model_dir), local_files_only=True)
        model.generation_config.max_new_tokens = 128
        model.generation_config.do_sample = False
        model.generation_config.repetition_penalty = 1.05
        model.generation_config.temperature = 1.0
        model.generation_config.top_p = None
        model.generation_config.max_length = None
        model.eval()

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

        llm = RunnableLambda(generate_text)
        return MedicalAssistantRuntime(
            model_dir=Path(options.model_dir),
            base_model_name=options.base_model_name,
            pipeline_type=llm.__class__.__name__,
            tokenizer_name=tokenizer.__class__.__name__,
            llm=llm,
        )
