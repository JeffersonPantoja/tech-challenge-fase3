# Segurança e Limitações

O assistente é experimental e serve apenas como apoio informacional. A LLM não substitui avaliação, diagnóstico ou decisão de um profissional de saúde.

## Geração e revisão

O campo `plan` dos prontuários sintéticos é preservado no JSONL, mas excluído do índice e do contexto RAG para evitar que uma conduta terapêutica seja reproduzida automaticamente. O revisor médico baseado na OpenAI analisa pergunta, contexto e resposta. Pedidos de medicamento ou tratamento recebem uma resposta restritiva, sem doses ou instruções para iniciar, interromper ou alterar tratamento. As demais respostas recebem um aviso de avaliação profissional.

No controller RAG, o revisor é sempre configurado. O caso de uso também aceita revisor opcional para permitir composição alternativa. Se a chamada de revisão falhar, o componente usa um fallback local que preserva a resposta e acrescenta o aviso de segurança.

## Dependências externas

O fluxo RAG exige `OPENAI_API_KEY`, pois a OpenAI é usada para detectar idioma, traduzir perguntas e respostas e revisar a saída. Falhas de tradução interrompem essa etapa e não possuem fallback de idioma. A geração principal da resposta é realizada pelo modelo local fine-tuned.

O tracing Langfuse é opcional. Ele só é ativado quando `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` e `LANGFUSE_HOST` estão configuradas. `LANGFUSE_CAPTURE_CONTENT` tem padrão `false`, evitando capturar integralmente conteúdo clínico. Falhas de inicialização, registro ou `flush` do Langfuse não interrompem o assistente.

## Limitações conhecidas

- O fine-tuning, os prontuários sintéticos e o modelo de embeddings foram definidos inicialmente para inglês.
- Perguntas em português dependem da tradução pela OpenAI antes da recuperação e depois da geração.
- A qualidade da resposta depende da qualidade das bases públicas e dos registros sintéticos.
- Métricas textuais não comprovam factualidade nem validade clínica.
- O treinamento e a inferência prática dependem de recursos de GPU.
- A revisão automática reduz riscos, mas não substitui validação humana.
