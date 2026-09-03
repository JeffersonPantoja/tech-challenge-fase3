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
4. Faça login no Hugging Face com um token com acesso ao modelo `meta-llama/Llama-3.2-1B-Instruct`.
5. Ajuste `DATASET_PATH` e `OUTPUT_DIR` para o caminho do seu Drive.
6. Execute as células em ordem: dependências, Drive, autenticação HF, dataset, modelo, treino e teste.
7. Salve o adapter/modelo final no Drive.

### Requisitos de armazenamento

- Dataset local gerado: cerca de 25 MB a 80 MB, dependendo do conteúdo final.
- Dataset no Drive: mesmo tamanho do arquivo local, mais a cópia de backup que você mantiver.
- Artefatos do treino no Drive: reserve de 2 GB a 8 GB.
- Espaço no runtime do Colab: reserve pelo menos 12 GB livres para dependências, cache e checkpoints.
- Se usar um modelo maior que o `LLaMA 3.2 1B`, aumente a folga de armazenamento e memória da GPU.

### Observações técnicas

- O notebook usa QLoRA para reduzir o consumo de VRAM.
- O notebook autentica no Hugging Face antes de baixar o modelo base.
- O carregamento espera um arquivo JSONL com uma linha por exemplo.
- O prompt final segue o formato `ANSWER THE QUESTION.` usado no dataset.

## Fontes de dados

- `resources/MedQuAD/`: arquivos XML com perguntas e respostas, originados de `https://github.com/abachaa/MedQuAD`
- `resources/pubmedqa/`: arquivos JSON com perguntas e respostas, originados de `https://pubmedqa.github.io/`

## Documentação

- `documentos/wiki-projeto/`: memória ativa do projeto
- `documentos/wiki-referencia/`: materiais de apoio e referências
