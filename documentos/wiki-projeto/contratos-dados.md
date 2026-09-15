# Contratos de Dados

Os modelos imutáveis ficam em `src/domain/`. As interfaces da aplicação ficam em `src/application/` e permitem trocar leitores, geradores, escritores, retrievers e integrações externas sem alterar os casos de uso.

## Dataset de perguntas e respostas

`QARecord` contém `source`, `question`, `answer` e `context` opcional. O método `to_finetuning_text()` gera o texto supervisionado com a instrução `ANSWER THE QUESTION.` e os marcadores `[|Context|]`, `[|Question|]` e `[|Answer|]`. O bloco de contexto só é emitido quando não está vazio.

`CurationStats` registra itens mantidos e descartados por campos vazios, duplicidade ou tamanho insuficiente. `CurationResult` agrupa os registros curados e essas estatísticas. `BuildDatasetResult` retorna a quantidade processada, o caminho de saída e as estatísticas de curadoria.

O arquivo final é JSONL UTF-8, com um objeto por linha:

```json
{"source":"MedQuAD:arquivo:pid","text":"ANSWER THE QUESTION. ..."}
```

## Prontuário sintético

`SyntheticPatientRecord` representa um prontuário com `source`, `patient_id`, `chief_complaint`, `history`, `medications`, `vitals`, `assessment` e `plan`. A geração pode usar OpenAI ou Llama. O identificador retornado pelo gerador não é necessariamente sequencial; a sequência é aplicada pelo comando de normalização.

`SyntheticPatientRecordReader` e `SyntheticPatientRecordWriter` encapsulam leitura e escrita do JSONL. O writer grava registros progressivamente durante a geração por lotes.

## Documentos e resposta RAG

`PatientRecordDocument` contém o `source`, o `patient_id` e o `content` indexável. O leitor transforma os prontuários em documentos e exclui `plan` do conteúdo indexado.

`RagAnswer` contém a resposta textual e as fontes recuperadas. As fontes são devolvidas com o identificador do paciente para permitir rastreabilidade.

`TranslationResult` representa o idioma detectado e o texto traduzido. `MedicalAssistantRuntime` encapsula o modelo local carregado, tokenizer, nome do modelo base, tipo de pipeline e LLM usada pelo LangChain.

## Checkpoints

`SyntheticPatientRecordsCheckpoint` mantém os conjuntos `processed_sources` e `failed_sources`. O checkpoint normal registra fontes concluídas; o checkpoint de falhas registra fontes de lotes descartados. Ambos são persistidos em JSON pelos respectivos stores e permitem retomar a geração sem repetir fontes concluídas ou falhadas.

## Portas da aplicação

As portas em `src/application/` definem contratos para leitores e escritores de QA, geradores e leitores/escritores de prontuários, carregamento do runtime, geração de respostas, tradução, recuperação, revisão médica, observabilidade e persistência dos checkpoints. As implementações concretas ficam em `src/infrastructure/`.
