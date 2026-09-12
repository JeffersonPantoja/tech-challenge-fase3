# Tech Challenge - Fase 3

Assistente médico em Python com preparação de dados, geração de prontuários sintéticos, fine-tuning local, RAG, tradução multilíngue e observabilidade com Langfuse.

## Fluxo do Projeto

```text
MedQuAD + PubMedQA
        |
        v
Curadoria e dataset de fine-tuning
        |
        v
Prontuários sintéticos em JSONL
        |
        v
Normalização dos patient_id
        |
        v
Fine-tuning do modelo no Colab
        |
        v
Embeddings + FAISS + recuperação
        |
        v
Tradução (`OpenAITranslator`) + contexto + geração + tradução
        |
        v
Resposta com fontes e tracing no Langfuse
```

## Requisitos

- Python 3.12 ou superior
- Git
- Docker e Docker Compose, para o Langfuse self-hosted
- GPU recomendada para fine-tuning e inferência
- Conta Hugging Face com acesso a `meta-llama/Llama-3.2-1B-Instruct`
- Chave `OPENAI_API_KEY` para geração sintética e tradução

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

As variáveis do arquivo `.env` não são carregadas automaticamente pelo shell. Para carregá-las na sessão atual:

```bash
set -a
source .env
set +a
```

## Estrutura de Diretórios

```text
src/
  application/       casos de uso e portas
  domain/            modelos imutáveis
  infrastructure/   leitores, writers, LLM, RAG e integrações
  presentation/     controllers de CLI
  notebooks/         notebooks para Colab
resources/
  MedQuAD/           dataset XML de origem
  pubmedqa/          dataset JSON de origem
  finetuning_qa.jsonl
  patient_records.jsonl
  medqa-finetuned-model/
documentos/
  wiki-projeto/      decisões e fluxos do projeto
  especificacoes/    planos técnicos
```

## Fontes de Dados

O projeto usa duas bases públicas de conhecimento médico. Os arquivos são mantidos localmente em `resources/` e não são versionados neste repositório.

### MedQuAD

- Origem: [repositório oficial no GitHub](https://github.com/abachaa/MedQuAD)
- Localização esperada: `resources/MedQuAD/`
- Formato: arquivos XML organizados em subdiretórios
- Conteúdo: pares de perguntas e respostas médicas extraídos de fontes do National Institutes of Health (NIH)
- Uso no projeto: preparação do dataset, curadoria e geração de prontuários sintéticos

### PubMedQA

- Origem: [página oficial do PubMedQA](https://pubmedqa.github.io/)
- Localização esperada: `resources/pubmedqa/`
- Formato: arquivos JSON
- Conteúdo: perguntas biomédicas associadas a contextos e respostas baseados em artigos científicos do PubMed
- Uso no projeto: preparação do dataset, curadoria e geração de prontuários sintéticos

### Preparação Local

Antes de executar os pipelines, confirme que os diretórios estão disponíveis:

```text
resources/
├── MedQuAD/
└── pubmedqa/
```

O campo `source` é preservado durante o processamento para permitir rastrear cada registro até o arquivo e identificador de origem.

## Dataset de Fine-Tuning

### O que acontece

O pipeline lê MedQuAD e PubMedQA, normaliza os registros, remove duplicidades e escreve um JSONL com o campo `source` e o texto no formato usado pelo fine-tuning.

O prompt usa:

```text
ANSWER THE QUESTION.
[|Context|] ...[|eContext|]

[|Question|] ...[|eQuestion|]

[|Answer|] ...[|eAnswer|]
```

### Como executar

Garanta que existam:

```text
resources/MedQuAD/
resources/pubmedqa/
```

Execute:

```bash
python3 -m src.main \
  --resources-dir resources \
  --output resources/finetuning_qa.jsonl
```

Saída:

```text
resources/finetuning_qa.jsonl
```

## Geração de Prontuários Sintéticos

### O que acontece

Cada caso curado é convertido em um prontuário sintético em inglês. A execução usa lotes, valida o retorno por `source`, repete lotes inválidos até três vezes e mantém checkpoints para permitir retomada.

O formato final contém:

```json
{
  "source": "...",
  "patient_id": "...",
  "chief_complaint": "...",
  "history": "...",
  "medications": "...",
  "vitals": "...",
  "assessment": "...",
  "plan": "..."
}
```

### Como executar com OpenAI

```bash
export OPENAI_API_KEY="sua-chave"
python3 -m src.main_synthetic_records \
  --backend openai \
  --resources-dir resources \
  --output resources/patient_records.jsonl
```

Opções úteis:

```bash
python3 -m src.main_synthetic_records \
  --batch-size 10 \
  --num-batches 2 \
  --openai-model gpt-4o-mini
```

Para reiniciar sem reutilizar checkpoints:

```bash
python3 -m src.main_synthetic_records --no-resume
```

### Como executar com Llama local

```bash
python3 -m src.main_synthetic_records \
  --backend llama \
  --llama-model-path caminho/para/llama-model
```

Saída principal:

```text
resources/patient_records.jsonl
```

## Normalização dos Pacientes

### O que acontece

O processo substitui os `patient_id` gerados por identificadores sequenciais, evitando duplicidades entre os prontuários.

### Como executar

```bash
python3 -m src.main_normalize_patient_ids
```

Por padrão:

```text
Entrada: resources/patient_records.jsonl
Saída:   resources/patient_records_sequential.jsonl
```

Para definir outros caminhos:

```bash
python3 -m src.main_normalize_patient_ids \
  --input resources/patient_records.jsonl \
  --output resources/patient_records_sequential.jsonl
```

Depois da normalização, use o arquivo sequencial como base do RAG ou substitua o arquivo original conforme o fluxo de dados adotado.

## Fine-Tuning no Colab

### O que acontece

O notebook usa QLoRA, Unsloth, Transformers e `trl.SFTTrainer` para ajustar o modelo base `meta-llama/Llama-3.2-1B-Instruct`. Ao final, o adapter é mesclado e o modelo completo é salvo.

### Como executar

1. Gere `resources/finetuning_qa.jsonl` localmente.
2. Envie o arquivo para o Google Drive.
3. Abra `src/notebooks/fine-tuning-colab.ipynb` no Google Colab.
4. Configure o secret `HF_TOKEN` com acesso ao modelo Llama.
5. Ajuste `DATASET_PATH` e `OUTPUT_DIR`.
6. Execute as células em ordem.
7. Aguarde o merge e o salvamento do modelo final.

O diretório final precisa conter pelo menos:

```text
config.json
model.safetensors
tokenizer files
```

Copie ou monte esse diretório como:

```text
resources/medqa-finetuned-model/
```

## Consulta a Dados Estruturados

### O que acontece

O `JsonPatientRecordDocumentReader` lê os prontuários e cria documentos com `source` e `patient_id`. O campo `plan` permanece no JSONL, mas não é incluído no conteúdo indexado pelo RAG.

O `FaissPatientRecordRetriever`:

- gera embeddings com `sentence-transformers/all-MiniLM-L6-v2`;
- cria um índice FAISS em memória;
- recupera os documentos semanticamente mais relevantes;
- filtra pelo `patient_id` atual quando informado;
- preserva `source` para rastreabilidade.

## Contextualização da Resposta

### O que acontece

O grafo LangGraph executa os nós nesta ordem:

```text
translate_question
  └── retrieve
        └── build_context
              └── generate
                    └── translate_answer
```

1. A API da OpenAI identifica o idioma da pergunta e a traduz para inglês.
2. A recuperação consulta os prontuários usando a pergunta em inglês.
3. O contexto é montado sem o campo `plan`.
4. O modelo local fine-tuned gera a resposta em inglês.
5. A resposta é traduzida para o idioma original pela API da OpenAI.
6. O resultado retorna a resposta e as fontes consultadas.

O `patient_id` é mantido na sessão. Pressione Enter no campo do paciente para continuar usando o paciente atual, informe outro ID para trocá-lo ou use `/clear` para removê-lo.

### Como executar

Garanta que existam:

```text
resources/medqa-finetuned-model/
resources/patient_records.jsonl
```

Configure a OpenAI:

```bash
export OPENAI_API_KEY="sua-chave"
```

Execute:

```bash
python3 -m src.main_rag
```

Opções:

```bash
python3 -m src.main_rag \
  --model-dir resources/medqa-finetuned-model \
  --patient-records resources/patient_records.jsonl \
  --embedding-model sentence-transformers/all-MiniLM-L6-v2 \
  --translation-model gpt-4o-mini \
  --top-k 4
```

## Langfuse Self-Hosted

### O que acontece

O Langfuse observa o fluxo sem participar da lógica de resposta. Os traces do LangGraph e as chamadas diretas da OpenAI podem ser visualizados no dashboard local.

### Como executar

Use uma instalação self-hosted do Langfuse com Docker Compose e acesse:

```text
http://localhost:3000
```

Crie um projeto e configure suas chaves no `.env`:

```bash
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_TRACING_ENVIRONMENT=local
LANGFUSE_RELEASE=local
LANGFUSE_CAPTURE_CONTENT=false
```

Carregue as variáveis e execute o RAG:

```bash
set -a
source .env
set +a
python3 -m src.main_rag
```

No dashboard, consulte **Traces** e abra uma execução individual. Os nós esperados são:

```text
translate_question
retrieve
build_context
generate
translate_answer
```

Para visualizar prompts e respostas integrais durante desenvolvimento:

```bash
LANGFUSE_CAPTURE_CONTENT=true
```

Esse modo pode registrar perguntas, contexto clínico e respostas. Use-o somente em ambiente controlado.

## Assistente Sem RAG

Para executar o fluxo original, sem recuperação de prontuários e sem tradução automática:

```bash
python3 -m src.main_langchain \
  --model-dir resources/medqa-finetuned-model
```

## Colab do Assistente

O notebook `src/notebooks/medical-assistant-colab.ipynb` executa o assistente sem RAG usando os use cases diretamente.

Passos:

1. Monte o Google Drive.
2. Clone ou atualize o repositório.
3. Configure `MODEL_PATH` para o modelo mesclado.
4. Instale as dependências do notebook.
5. Execute as células em ordem.

## Verificação Local

```bash
python3 -m compileall src
git diff --check
```

O projeto não possui uma suíte de testes ou configuração de CI atualmente.

## Documentação

- [Wiki do projeto](documentos/wiki-projeto/README.md)
- [Fluxos](documentos/wiki-projeto/fluxos.md)
- [Decisões de arquitetura](documentos/wiki-projeto/decisoes-arquitetura.md)
- [Plano do assistente com LangChain](documentos/especificacoes/plano-assistente-medico-langchain.md)
- [Wiki de referência](documentos/wiki-referencia/README.md)
