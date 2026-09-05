from __future__ import annotations

from pathlib import Path

from langchain_community.llms import HuggingFacePipeline
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer, pipeline

from src.application.ports import MedicalAssistantRuntimeLoader
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


class LocalMedicalAssistantRuntimeLoader(MedicalAssistantRuntimeLoader):
    def load(self, options: MedicalAssistantCommandOptions) -> MedicalAssistantRuntime:
        tokenizer = AutoTokenizer.from_pretrained(str(options.model_dir), use_fast=True)
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoPeftModelForCausalLM.from_pretrained(
            str(options.model_dir),
            device_map="auto",
            low_cpu_mem_usage=True,
        )
        model.eval()

        text_generation_pipeline = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=128,
            do_sample=False,
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
