# Curadoria e Limpeza

Os datasets públicos usados no projeto não exigem anonimização pesada de LGPD, mas exigem curadoria técnica antes do fine-tuning.

## Conclusão

- `PubMedQA` e `MedQuAD` são bases públicas.
- A prioridade é limpar, padronizar e validar os registros.
- O foco é qualidade do treino, não remoção de PII de pacientes reais.
- A leitura dos datasets não usa LangChain por decisão de desempenho e memória; a curadoria opera sobre iteradores e parsing direto.

## Plano de implementação

1. Validar campos obrigatórios por fonte.
2. Normalizar texto e espaços em branco.
3. Remover registros vazios, truncados ou duplicados.
4. Filtrar casos com respostas inconsistentes ou incompletas.
5. Preservar `source` para rastreabilidade.
6. Registrar contagem de registros descartados por motivo.

## Regras por fonte

### PubMedQA

- Usar `QUESTION` como pergunta principal.
- Usar `LONG_ANSWER` quando existir; caso contrário, usar `LABELS`.
- Manter `CONTEXTS` como contexto consolidado.

### MedQuAD

- Exigir `Question` e `Answer` não vazios.
- Usar `Focus` como contexto opcional.
- Descartar `QAPair` quebrado ou sem resposta.
