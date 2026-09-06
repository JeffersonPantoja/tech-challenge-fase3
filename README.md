# Tech Challenge - Fase 3

Projeto em Python para estruturar dados médicos e gerar dataset de fine-tuning a partir de `MedQuAD` e `PubMedQA`.

## Estrutura

- `src/`: código da aplicação com clean architecture
- `resources/`: dados brutos e saída final do dataset
  - `resources/MedQuAD/`: base XML com pares de pergunta e resposta obtida de `https://github.com/abachaa/MedQuAD`
  - `resources/pubmedqa/`: base JSON com perguntas e respostas obtida de `https://pubmedqa.github.io/`
  - `resources/finetuning_qa.jsonl`: saída gerada para fine-tuning
- `documentos/`: especificações, wiki de referência e wiki do projeto

## Requisitos

- Python 3.12+
- Ambiente virtual `.venv`

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

Gerar o dataset final:

```bash
python3 -m src.main --resources-dir resources --output resources/finetuning_qa.jsonl
```

Carregar o assistente médico com LangChain:

```bash
python3 -m src.main_langchain --model-dir resources/medqa-finetuned-model
```

Usar o modelo mesclado local:

```bash
python3 -m src.main_langchain --model-dir resources/medqa-finetuned-model --use-local-model true
```

Pergunta inicial com sessão aberta:

```bash
python3 -m src.main_langchain --model-dir resources/medqa-finetuned-model --question "Qual a conduta para febre?"
```

### Saída

O arquivo gerado será um JSONL com uma linha por registro no formato:

```json
{
  "source": "...",
  "text": "ANSWER THE QUESTION. ..."
}
```

## Fine-tuning no Colab

Notebook base: `src/notebooks/fine-tuning-colab.ipynb`

### Passo a passo

1. Gere o dataset localmente com o comando acima.
2. Envie `resources/finetuning_qa.jsonl` manualmente para o Google Drive.
3. Abra o notebook no Colab e monte o Drive.
4. Defina o Secret `HF_TOKEN` no Colab com um token com acesso ao modelo `meta-llama/Llama-3.2-1B-Instruct`.
5. Ajuste `DATASET_PATH` e `OUTPUT_DIR` para o caminho do seu Drive.
6. Execute as células em ordem: dependências, Drive, autenticação HF, dataset, modelo, treino e teste.
7. O notebook faz merge do adapter e salva o modelo completo no diretório final.

### Requisitos de armazenamento

- Dataset local gerado: cerca de 25 MB a 80 MB, dependendo do conteúdo final.
- Dataset no Drive: mesmo tamanho do arquivo local, mais a cópia de backup que você mantiver.
- Artefatos do treino no Drive: reserve de 2 GB a 8 GB.
- Espaço no runtime do Colab: reserve pelo menos 12 GB livres para dependências, cache e checkpoints.
- Se usar um modelo maior que o `LLaMA 3.2 1B`, aumente a folga de armazenamento e memória da GPU.

### Observações técnicas

- O notebook usa QLoRA para reduzir o consumo de VRAM.
- O notebook usa `unsloth` para baixar e preparar o modelo base, como na referência.
- O notebook faz merge do adapter após o treino e salva o modelo completo no diretório final.
- O runtime prefere esse modelo completo e mantém compatibilidade com o adapter anterior até o notebook ser rerodado.
- O notebook autentica no Hugging Face antes de baixar o modelo base.
- O carregamento espera um arquivo JSONL com uma linha por exemplo.
- O prompt final segue o formato `ANSWER THE QUESTION.` usado no dataset.

## Assistente Médico no Colab

Notebook: `src/notebooks/medical-assistant-colab.ipynb`

### Fluxo

1. Monte o Google Drive.
2. Clone o repositório por HTTPS em uma célula separada para permitir atualizações.
3. Aponte `MODEL_PATH` para o diretório do modelo mesclado no Drive, se o caminho padrão não servir.
4. Instale as dependências inline no próprio notebook.
5. O notebook instancia `LoadMedicalAssistantUseCase` e `AskMedicalAssistantUseCase` diretamente.
6. Execute o loop interativo no próprio notebook.

## Fontes de dados

- `resources/MedQuAD/`: arquivos XML com perguntas e respostas, originados de `https://github.com/abachaa/MedQuAD`
- `resources/pubmedqa/`: arquivos JSON com perguntas e respostas, originados de `https://pubmedqa.github.io/`

## Documentação

- `documentos/wiki-projeto/`: memória ativa do projeto
- `documentos/wiki-referencia/`: materiais de apoio e referências
