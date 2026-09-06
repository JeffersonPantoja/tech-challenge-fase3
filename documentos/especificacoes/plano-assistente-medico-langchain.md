# Especificação - Criação de Assistente Médico com LangChain

## Objetivo

Utilizar LangChain para criar um assistente médico que integre a LLM customizada e responda com base em dados estruturados e informações atualizadas do paciente.

## Referências

- `documentos/wiki-referencia/langchain/README.md`
- `resources/medqa-finetuned-model`

## Escopo

- Construir um pipeline com LangChain integrando a LLM customizada.
- Consultar base de dados estruturadas, como prontuários e registros.
- Contextualizar as respostas com informações atualizadas do paciente.

## Fluxo Geral

1. O sistema carrega a LLM customizada.
2. O LangChain orquestra a entrada do usuário, a consulta às bases estruturadas e a montagem do contexto.
3. O pipeline recupera dados relevantes do paciente.
4. A resposta é gerada pela LLM com base no contexto consolidado.

## Etapas do Projeto

### T1 - Integração da LLM

- Validar a presença de `resources/medqa-finetuned-model`.
- Definir a forma de carregamento da LLM customizada no runtime.
- Expor a LLM para uso pela camada LangChain.

### T2 - Pipeline LangChain

- Criar o pipeline de orquestração com LangChain.
- Integrar a LLM customizada à cadeia de processamento.
- Centralizar a composição da entrada e da saída do assistente.
- Responder perguntas através do modelo carregado

### T3 - Consulta a dados estruturados

- Consultar prontuários e registros estruturados.
- Selecionar os dados relevantes do paciente para a resposta.
- Preservar rastreabilidade da origem dos dados consultados.

### T4 - Contextualização da resposta

- Montar o contexto final com dados do paciente e a pergunta atual.
- Gerar respostas contextualizadas pela LLM.
- Manter o fluxo preparado para atualização contínua das informações do paciente.

### T5 - Validação

- Testar consultas com diferentes perfis de paciente e tipos de pergunta.
- Verificar se a resposta usa os dados corretos do contexto.
- Confirmar que a atualização das informações altera a resposta quando necessário.

### T6 - Documentação

- Atualizar a wiki do projeto com o fluxo da nova fase.
- Registrar as decisões de integração e consulta aos dados.

## Critérios de Conclusão

- A LLM customizada está integrada ao LangChain.
- O pipeline consulta dados estruturados do paciente.
- As respostas são contextualizadas com informações atualizadas.
- A documentação da fase foi atualizada.
