# Fluxos

## Fluxo de dataset

1. O controller lê os argumentos da CLI.
2. O caso de uso chama o reader de fontes.
3. O reader percorre `MedQuAD` e `PubMedQA` em modo incremental.
4. Cada `QARecord` é convertido em `text` com marcadores.
5. O writer grava o JSON final progressivamente em `resources/finetuning_qa.json`.

## Formato final

```text
ANSWER THE QUESTION.
[|Context|] ...[|eContext|]

[|Question|] ...[|eQuestion|]

[|Answer|] ...[|eAnswer|]
```

Se não houver contexto, o bloco `Context` não é incluído.
