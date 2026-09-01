# Decisões de Arquitetura

O código foi organizado em clean architecture para manter baixo acoplamento.

## Camadas

- `domain`: entidade `QARecord`
- `application`: portas e caso de uso `BuildMedQaDatasetUseCase`
- `infrastructure`: leitores dos dados e writer do JSON final
- `presentation`: controller de linha de comando

## Decisões

- O dataset final é gerado como texto único com marcadores.
- O `context` é preservado quando existir na fonte.
- A escrita final é em JSON para facilitar consumo posterior no treino.
- O pipeline foi ajustado para processamento em streaming, evitando carregar todo o dataset em memória.
- O reader expõe registros como `Iterable`, e o writer grava o arquivo progressivamente.
- A leitura dos datasets foi mantida fora do LangChain para reduzir custo de abstração, melhorar desempenho e evitar consumo excessivo de memória.
- A curadoria foi isolada em `QARecordCurationService` para aplicar limpeza, deduplicação e métricas de descarte antes da escrita final.
