# Recuperação Aumentada por Geração

O fluxo RAG é implementado por `AskMedicalAssistantWithRagUseCase` e executado pelo `RagMedicalAssistantController`. Ele combina a LLM local fine-tuned com informações recuperadas dos prontuários sintéticos.

## Indexação

`JsonPatientRecordDocumentReader` lê `patient_records.jsonl`, valida a presença de `source`, `patient_id` e conteúdo e cria documentos indexáveis. O conteúdo inclui identificador, queixa principal, histórico, medicamentos, sinais vitais e avaliação. O campo `plan` permanece armazenado, mas não é indexado nem enviado como contexto ao modelo.

`FaissPatientRecordRetriever` usa `sentence-transformers/all-MiniLM-L6-v2` para converter os documentos em embeddings. Os vetores são armazenados em um índice FAISS criado na inicialização do processo. O modelo de embeddings pode ser trocado por `--embedding-model`.

## Recuperação

Para cada pergunta, o retriever gera ou utiliza o embedding correspondente e executa busca semântica no índice. O padrão é retornar os quatro documentos mais similares, controlado por `--top-k`. A busca considera significado semântico, e não apenas coincidência literal de palavras.

Quando `patient_id` é informado, o conjunto é filtrado primeiro por igualdade exata do identificador. Um índice temporário é criado para ranquear semanticamente apenas os documentos daquele paciente. Se não houver registros para o identificador, nenhum documento é retornado.

## Grafo de consulta

O estado interno `_RagState` preserva pergunta original, pergunta traduzida, idioma, paciente, documentos, contexto e resposta. As etapas do grafo são:

1. `translate_question`: traduz a pergunta para inglês usando a OpenAI API.
2. `retrieve`: busca documentos relevantes com embeddings e FAISS.
3. `build_context`: concatena os documentos e suas fontes.
4. `generate`: executa a LLM local fine-tuned com o template compatível com o treinamento.
5. `translate_answer`: traduz a resposta para o idioma original.
6. `review_output`: revisa a resposta e retorna as fontes.

Se nenhum documento for encontrado, o contexto informa que não há prontuário relevante. A resposta final mantém as fontes recuperadas no objeto `RagAnswer`.
