from __future__ import annotations

from pathlib import Path

from langchain_community.llms import HuggingFacePipeline
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline

from src.application.ports import MedicalAssistantRuntimeLoader
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


class LocalMedicalAssistantRuntimeLoader(MedicalAssistantRuntimeLoader):
    def load(self, options: MedicalAssistantCommandOptions) -> MedicalAssistantRuntime:
        tokenizer = AutoTokenizer.from_pretrained(str(options.model_dir), use_fast=True, local_files_only=True, fix_mistral_regex=True)
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
        model.eval()

        text_generation_pipeline = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            return_full_text=False,
        )

        llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
        return MedicalAssistantRuntime(
            model_dir=Path(options.model_dir),
            base_model_name=options.base_model_name,
            pipeline_type=llm.__class__.__name__,
            tokenizer_name=tokenizer.__class__.__name__,
            llm=llm,
        )
