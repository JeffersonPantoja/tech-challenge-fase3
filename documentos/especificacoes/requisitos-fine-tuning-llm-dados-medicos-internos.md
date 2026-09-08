# Requisitos 1 - Fine-tuning de LLM com dados médicos internos

Fonte: `documentos/especificacoes/8IADT - Fase 3 - Tech challenge.pdf`

## Objetivo

Realizar o fine-tuning de um modelo LLM para atuar como assistente médico treinado com dados do próprio hospital, capaz de auxiliar em condutas clínicas, responder dúvidas de médicos e sugerir procedimentos com base nos protocolos internos.

## Dados de entrada

- Protocolos médicos do hospital.
- Exemplos de perguntas frequentes feitas por médicos.
- Modelos de laudos, receitas e procedimentos internos.

## Preparação dos dados

- `preprocessing`: limpeza, estruturação e formatação dos textos para o formato aceito pelo modelo.
- Anonimização: remoção de dados pessoais e sensíveis.
- Curadoria: validação de qualidade, consistência médica e ausência de conflitos.

## Modelos sugeridos

- LLaMA.
- Falcon.
- Outro modelo open-source equivalente adequado para fine-tuning.

## Entregáveis relacionados

- Pipeline de fine-tuning em Python.
- Dataset anonimizado ou sintético.
- Relatório técnico com explicação do processo, parâmetros e avaliação dos resultados.
- Demonstração em vídeo do treinamento e do funcionamento da LLM personalizada.
