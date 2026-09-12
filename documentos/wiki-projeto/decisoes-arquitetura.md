# Decisões de Arquitetura

O código foi organizado em clean architecture para manter baixo acoplamento.

## Camadas

- `domain`: entidade `QARecord`
- `domain`: `QARecord`, `CurationStats`, `CurationResult`, `CommandOptions` e `BuildDatasetResult`
- `application`: portas e caso de uso `BuildMedQaDatasetUseCase`
- `application`: portas e caso de uso `LoadMedicalAssistantUseCase`
- `application`: portas e caso de uso `AskMedicalAssistantUseCase`
- `infrastructure`: leitores dos dados, curadoria e writer do JSONL final
- `infrastructure`: gerador de prontuários sintéticos via API da OpenAI
- `infrastructure`: loader local da LLM customizada para o assistente médico
- `infrastructure`: gerador LangChain da resposta do assistente
- `presentation`: controller de linha de comando `MedQaController`
- `presentation`: controller de linha de comando `MedicalAssistantController`

## Decisões

- O dataset final é gerado como texto único com marcadores.
- O `context` é preservado quando existir na fonte.
- A escrita final é em JSONL para facilitar consumo posterior no treino.
- O pipeline foi ajustado para processamento em streaming, evitando carregar todo o dataset em memória.
- O reader expõe registros como `Iterable`, e o writer grava o arquivo progressivamente.
- A leitura dos datasets foi mantida fora do LangChain para reduzir custo de abstração, melhorar desempenho e evitar consumo excessivo de memória.
- A curadoria foi isolada em `QARecordCurationService` para aplicar limpeza, deduplicação e métricas de descarte antes da escrita final.
- Na geração de prontuários sintéticos, a curadoria ajuda a limpar a entrada, mas o valor principal vem do lote validado por `source` e do checkpoint de falhas.
- O treino fica concentrado no notebook `src/notebooks/fine-tuning-colab.ipynb`, que usa `unsloth`, `datasets`, `transformers` e `trl.SFTTrainer` com QLoRA.
- A etapa de Geração de Prontuários Sintéticos gera prontuários fictícios a partir de `MedQuAD` e `PubMedQA`, preservando `source` para rastreabilidade.
- A etapa de Geração de Prontuários Sintéticos trabalha em lotes, valida o retorno por `source`, tenta novamente em caso de resposta inválida e descarta o lote após 3 falhas.
- A escrita dos prontuários sintéticos é em JSONL para facilitar consumo posterior pelo assistente.
- O checkpoint é persistido por `source` processado para permitir retomada sem repetir lotes já concluídos.
- T4 usa `patient_records.jsonl` como base RAG sem alterar o arquivo original; o `patient_id` sequencial identifica o paciente.
- T4 usa embeddings Hugging Face com FAISS para recuperar registros por similaridade semântica.
- O campo `plan` é preservado nos prontuários, mas fica fora do conteúdo indexado e do contexto RAG.
- T5 usa LangGraph para orquestrar a montagem do contexto e a geração da resposta.
- T5 reutiliza o template textual do dataset para reduzir o desalinhamento entre fine-tuning e inferência.
- T5 usa a API da OpenAI exclusivamente para detectar o idioma e traduzir a pergunta para inglês antes da recuperação e a resposta depois da geração; a resposta médica continua sendo gerada pela LLM local fine-tuned.
- O assistente médico da fase 2 carrega sempre o modelo local mesclado salvo no notebook.
- O fine-tuning, os prontuários sintéticos, o prompt de inferência e o modelo atual de embeddings estão em inglês; por isso, o fluxo RAG deve ser validado inicialmente com perguntas em inglês.
- Perguntas em português não são traduzidas automaticamente. Suporte em português deverá adicionar uma etapa explícita de tradução para inglês antes da recuperação e, se necessário, tradução da resposta na saída.
- A interação do assistente acontece pelo terminal em modo interativo.
- A conversa da sessão fica restrita ao controlador e não entra no prompt de geração.
- Os módulos do projeto seguem nomes CamelCase para refletir diretamente as classes exportadas.
