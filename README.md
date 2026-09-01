# Tech Challenge - Fase 3

Projeto em Python para estruturar dados médicos e gerar dataset de fine-tuning a partir de `MedQuAD` e `PubMedQA`.

## Estrutura

- `src/`: código da aplicação com clean architecture
- `resources/`: dados brutos e saída final do dataset
  - `resources/MedQuAD/`: base XML com pares de pergunta e resposta obtida de `https://github.com/abachaa/MedQuAD`
  - `resources/pubmedqa/`: base JSON com perguntas e respostas obtida de `https://pubmedqa.github.io/`
  - `resources/finetuning_qa.json`: saída gerada para fine-tuning
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
python3 -m src.main --resources-dir resources --output resources/finetuning_qa.json
```

### Saída

O arquivo gerado será um JSON com itens no formato:

```json
{
  "source": "...",
  "text": "ANSWER THE QUESTION. ..."
}
```

## Fontes de dados

- `resources/MedQuAD/`: arquivos XML com perguntas e respostas, originados de `https://github.com/abachaa/MedQuAD`
- `resources/pubmedqa/`: arquivos JSON com perguntas e respostas, originados de `https://pubmedqa.github.io/`

## Documentação

- `documentos/wiki-projeto/`: memória ativa do projeto
- `documentos/wiki-referencia/`: materiais de apoio e referências
