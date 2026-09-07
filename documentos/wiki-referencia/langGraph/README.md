# LangGraph

Materiais de aula e referências sobre orquestração de fluxos com grafo.

## Visão geral

- LangGraph é o runtime de orquestração para fluxos longos e stateful.
- É útil quando o fluxo combina passos determinísticos com passos guiados por LLM.
- No projeto, serve como base para criar assistentes com controle fino do estado e das transições.

## Aulas

- `LangGraph-Aula-01.pdf`: introdução ao LangGraph e conceito de grafo.
- `LangGraph-Aula-02.pdf`: configuração inicial, `StateGraph`, nós e estado compartilhado.
- `LangGraph-Aula-03.pdf`: casos de uso e aprofundamento em fluxos com decisões.
- `LangGraph-Aula-04.pdf`: continuação dos exemplos e padrões práticos.

## Padrões úteis para o projeto

- `TypedDict` para estado tipado.
- Nós especializados para leitura, curadoria, enriquecimento e resposta.
- Arestas condicionais para decidir quando seguir para enriquecimento ou finalizar.
- Mistura de lógica determinística com geração do modelo.

## Fluxos parecidos

- Assistente clínico com triagem: entrada estruturada, classificação, recuperação de contexto e resposta final.
- Enriquecimento de prompt: dados do paciente fictício + base médica + regra de resposta.
- Revisão de resposta: nó adicional valida consistência antes de devolver a saída.
