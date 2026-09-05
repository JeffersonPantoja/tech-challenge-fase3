# Plano Técnico - Assistente Médico com LangChain

## Objetivo

Criar a segunda fase do projeto: um assistente médico baseado em LangChain, usando como motor principal o modelo fine-tuned salvo em `resources/medqa-finetuned-model`.

## Referências

- `documentos/especificacoes/requisitos-fine-tuning-llm-dados-medicos-internos.md`
- `documentos/especificacoes/plano-fine-tuning-colab.md`
- `documentos/wiki-referencia/langchain/README.md`
- `documentos/wiki-referencia/Fine-tuning-rag-para-documentos/Aula-03-RAG-para-documentos/README.md`
- `src/notebooks/fine-tuning-colab.ipynb`

## Escopo

- Carregar localmente o modelo ajustado em `resources/medqa-finetuned-model`.
- Criar a camada de orquestração com LangChain.
- Definir prompt do assistente médico com instruções, contexto e restrições de segurança.
- Manter histórico de conversa quando fizer sentido para a interação.
- Estruturar o fluxo para futuras integrações com recuperação de documentos e ferramentas.

## Fluxo Geral

1. O aplicativo carrega o modelo fine-tuned local.
2. O LangChain encapsula o modelo em uma cadeia de conversa.
3. O prompt do sistema define papel, tom, limites e formato da resposta.
4. O usuário envia perguntas clínicas ou operacionais.
5. O assistente gera resposta com base no modelo e no contexto da conversa.
6. Quando houver base documental, a cadeia pode consultar fontes adicionais antes de responder.

## Etapas do Projeto

### T1 - Preparação do modelo local

- Validar a presença de `resources/medqa-finetuned-model`.
- Definir como o modelo será carregado no runtime local.
- Confirmar compatibilidade com o fluxo de inferência escolhido.

### T2 - Camada LangChain

- Criar a abstração de orquestração com LangChain.
- Centralizar prompt, memória e composição da resposta.
- Manter o código desacoplado da origem do modelo.

### T3 - Prompt e guardrails

- Definir instruções de sistema para um assistente médico seguro.
- Limitar o comportamento a orientação informativa e apoio clínico.
- Preservar rastreabilidade do contexto quando houver uso de base externa.

### T4 - Conversa e recuperação de contexto

- Implementar histórico de conversa quando útil.
- Preparar a cadeia para integrar documentos internos ou base de conhecimento.
- Permitir evolução para RAG sem refatoração grande.

### T5 - Validação

- Testar o assistente com perguntas clínicas curtas e longas.
- Verificar consistência, aderência ao prompt e uso correto do contexto.
- Registrar limitações e casos em que o assistente deve recusar ou recomendar revisão humana.

### T6 - Documentação

- Atualizar a wiki do projeto com o fluxo da nova fase.
- Registrar decisões de arquitetura relevantes.
- Manter o plano alinhado ao notebook/modelo gerado na fase anterior.

## Critérios de Conclusão

- O modelo `resources/medqa-finetuned-model` é usado como base do assistente.
- A camada LangChain executa o fluxo de pergunta e resposta.
- O prompt do assistente médico está definido e documentado.
- O fluxo está pronto para expansão com memória e recuperação de documentos.
- A documentação do projeto foi atualizada.
