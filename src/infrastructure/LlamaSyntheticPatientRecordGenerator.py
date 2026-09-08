from __future__ import annotations

import json
import os
import re
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

from src.application.SyntheticPatientRecordGenerator import SyntheticPatientRecordGenerator
from src.domain.QARecord import QARecord
from src.domain.SyntheticPatientRecord import SyntheticPatientRecord


class LlamaSyntheticPatientRecordGenerator(SyntheticPatientRecordGenerator):
    def __init__(self, model_path: str, max_new_tokens: int = 512) -> None:
        self._model_path = Path(model_path)
        self._max_new_tokens = max_new_tokens
        self._tokenizer = AutoTokenizer.from_pretrained(
            str(self._model_path),
            use_fast=True,
            local_files_only=True,
        )
        if self._tokenizer.pad_token is None and self._tokenizer.eos_token is not None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        if torch.cuda.is_available():
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        else:
            dtype = torch.float32

        self._model = AutoModelForCausalLM.from_pretrained(
            str(self._model_path),
            torch_dtype=dtype,
            device_map="auto",
            local_files_only=True,
        )
        self._model.eval()

    def generate(self, record: QARecord) -> SyntheticPatientRecord:
        return self.generate_batch([record])[0]

    def generate_batch(self, records: list[QARecord]) -> list[SyntheticPatientRecord]:
        prompt = self._build_prompt(records)
        content = self._request(prompt)
        payloads = self._parse_payloads(content, records)
        return self._build_records(records, payloads)

    def _request(self, prompt: str) -> str:
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        with torch.inference_mode():
            output_ids = self._model.generate(
                **inputs,
                max_new_tokens=self._max_new_tokens,
                do_sample=False,
                temperature=1.0,
                top_p=None,
                repetition_penalty=1.05,
            )

        generated_ids = output_ids[0][inputs["input_ids"].shape[-1] :]
        return self._tokenizer.decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        ).strip()

    def _parse_payloads(self, content: str, records: list[QARecord]) -> list[dict[str, str]]:
        payload_text = self._strip_code_fence(content.strip())
        if payload_text.startswith("["):
            payloads = self._normalize_json_payload(payload_text)
        else:
            payloads = self._extract_batched_payload(payload_text)
        return self._validate_payloads(payloads, records)

    def _normalize_json_payload(self, content: str) -> list[dict[str, str]]:
        data = json.loads(content)
        if isinstance(data, dict):
            data = [data]
        normalized: list[dict[str, str]] = []
        for item in data:
            normalized.append({str(key).lower(): str(value) for key, value in dict(item).items()})
        return normalized

    def _validate_payloads(self, payloads: list[dict[str, str]], records: list[QARecord]) -> list[dict[str, str]]:
        expected_sources = [record.source for record in records]
        payload_by_source: dict[str, dict[str, str]] = {}
        duplicate_sources: set[str] = set()

        for payload in payloads:
            source = payload.get("source", "").strip()
            if not source:
                continue
            if source in payload_by_source:
                duplicate_sources.add(source)
            payload_by_source[source] = payload

        missing_sources = [source for source in expected_sources if source not in payload_by_source]
        unexpected_sources = [source for source in payload_by_source if source not in expected_sources]
        if missing_sources or unexpected_sources or duplicate_sources:
            raise ValueError(
                "Resposta do lote inválida: "
                f"missing={missing_sources}, unexpected={unexpected_sources}, duplicates={sorted(duplicate_sources)}"
            )

        return [payload_by_source[source] for source in expected_sources]

    def _strip_code_fence(self, content: str) -> str:
        lines = content.splitlines()
        if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].startswith("```"):
            return "\n".join(lines[1:-1]).strip()
        return content.strip()

    def _extract_batched_payload(self, content: str) -> list[dict[str, str]]:
        blocks = [block.strip() for block in content.split("\n\n---\n\n") if block.strip()]
        return [self._extract_fields(block) for block in blocks]

    def _extract_fields(self, content: str) -> dict[str, str]:
        pattern = re.compile(r"^(patient_id|chief_complaint|history|medications|vitals|assessment|plan)\s*:\s*(.*)$", re.IGNORECASE)
        current_key: str | None = None
        current_value: list[str] = []
        extracted: dict[str, str] = {}

        def flush() -> None:
            nonlocal current_key, current_value
            if current_key is not None:
                extracted[current_key] = " ".join(part.strip() for part in current_value if part.strip()).strip()
            current_key = None
            current_value = []

        for line in content.splitlines():
            match = pattern.match(line.strip())
            if match:
                flush()
                current_key = match.group(1).lower()
                current_value = [match.group(2).strip()]
                continue
            if current_key is not None:
                current_value.append(line.strip())

        flush()
        return extracted

    def _build_records(self, records: list[QARecord], payloads: list[dict[str, str]]) -> list[SyntheticPatientRecord]:
        synthetic_records: list[SyntheticPatientRecord] = []
        for record, payload in zip(records, payloads, strict=True):
            synthetic_records.append(
                SyntheticPatientRecord(
                    source=record.source,
                    patient_id=str(payload.get("patient_id", record.source)),
                    chief_complaint=str(payload.get("chief_complaint", "")),
                    history=str(payload.get("history", "")),
                    medications=str(payload.get("medications", "")),
                    vitals=str(payload.get("vitals", "")),
                    assessment=str(payload.get("assessment", "")),
                    plan=str(payload.get("plan", "")),
                )
            )
        return synthetic_records

    def _build_prompt(self, records: list[QARecord]) -> str:
        cases = []
        for index, record in enumerate(records, start=1):
            cases.append(
                f"CASE {index}\n"
                f"SOURCE: {record.source}\n"
                f"QUESTION: {record.question}\n"
                f"ANSWER: {record.answer}\n"
                f"CONTEXT: {record.context}"
            )

        return (
            "Generate synthetic patient records in English for the cases below.\n"
            "Respond only with a valid JSON array.\n"
            "Each array item must contain exactly these keys: source, patient_id, chief_complaint, history, medications, vitals, assessment, plan.\n"
            "The source field must be copied exactly from the input case.\n"
            "The array order may differ from the input order, but every input source must appear exactly once.\n"
            "If a case cannot be answered, still return an item with the same source and empty or minimal fields.\n"
            "Do not duplicate any source.\n"
            "Do not include markdown, explanations, or any text outside the JSON.\n\n"
            + "\n\n".join(cases)
        )
