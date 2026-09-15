# Padrões

## Código

- Nomes explícitos por domínio.
- Classes e funções pequenas, com responsabilidade única.
- Tipagem forte com `Path`, `list[...]` e `dataclass`.

## Dados

- Entradas brutas ficam em `resources/MedQuAD` e `resources/pubmedqa`.
- A saída de treino é um arquivo JSONL UTF-8, com um objeto por linha e os campos `source` e `text`.
- Marcadores usados para manter estrutura estável no fine-tuning.

## Convenções de texto

- `ANSWER THE QUESTION.` como instrução base.
- Blocos delimitados por marcadores no estilo da wiki de referência.
- O bloco `Context` é omitido quando o registro não possui contexto.
- O template de treino e o template de inferência usam os mesmos marcadores; o fluxo RAG acrescenta o contexto recuperado.

## Organização do código

- `src/domain/`: dataclasses e modelos de estado sem dependência de infraestrutura.
- `src/application/`: casos de uso, portas e contratos do sistema.
- `src/infrastructure/`: parsers, JSONL, modelo local, OpenAI, embeddings, FAISS e Langfuse.
- `src/presentation/`: composição das dependências, argumentos de CLI e loops interativos.
