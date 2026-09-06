# Plano Técnico - Correção da Fase 2 do Assistente Médico com LangChain

## Objetivo

Ajustar a implementação da fase 2 para que a inferência fique mais coerente com o dataset de fine-tuning, separando histórico de conversa do contexto factual e deixando a interface mais explícita.

## Escopo

- Alinhar o prompt de inferência ao template usado no dataset.
- Manter o histórico da sessão separado do `Context` do prompt.
- Revisar o papel do argumento `--base-model` na CLI.
- Tornar explícita a dependência do modelo base ou consolidar o artefato local, conforme a decisão arquitetural.
- Validar a saída com exemplos reais do dataset.

## Plano de Correção

### T1 - Alinhamento do prompt

- Usar o mesmo formato estrutural do dataset na inferência.
- Preservar `ANSWER THE QUESTION.`, `Question` e `Answer`.
- Evitar injetar histórico de conversa como contexto factual.

### T2 - Separação de responsabilidades

- Manter `MedicalAssistantConversation` apenas como memória da sessão.
- Não misturar mensagens anteriores com o bloco `[|Context|]`.
- Preparar o fluxo para futura fonte factual separada.

### T3 - Ajuste da T1

- O notebook salva o modelo completo após o merge do adapter no base model.
- A inferência prioriza o diretório local final e mantém compatibilidade transitória com o adapter antigo.
- A documentação deve refletir que o runtime usa o modelo mesclado quando disponível.

### T4 - Revisão da CLI

- Verificar se `--base-model` será realmente usado no carregamento.
- Caso não seja necessário, remover a opção para evitar ambiguidade.

### T5 - Validação

- Testar perguntas do dataset original.
- Comparar a resposta gerada com o padrão esperado.
- Confirmar redução de repetição e melhora de aderência ao treino.

## Critérios de Conclusão

- A resposta da inferência está mais próxima do template do dataset.
- Histórico de conversa e contexto factual não estão misturados.
- A CLI reflete com precisão o que o carregamento faz.
- A documentação da fase 2 permanece consistente com a implementação.
