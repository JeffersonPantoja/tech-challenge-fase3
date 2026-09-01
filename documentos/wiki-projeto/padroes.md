# Padrões

## Código

- Nomes explícitos por domínio.
- Classes e funções pequenas, com responsabilidade única.
- Tipagem forte com `Path`, `list[...]` e `dataclass`.

## Dados

- Entradas brutas ficam em `resources/MedQuAD` e `resources/pubmedqa`.
- A saída de treino é um JSON com campo `text`.
- Marcadores usados para manter estrutura estável no fine-tuning.

## Convenções de texto

- `ANSWER THE QUESTION.` como instrução base.
- Blocos delimitados por marcadores no estilo da wiki de referência.
