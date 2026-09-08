# Fluxos com Dados Estruturados

Referência para fluxos parecidos com modelo fine-tuned enriquecido por dados estruturados.

## Ideia central

O padrão mais próximo do que precisamos para a T3 é:

1. Receber dados estruturados do paciente ou do caso clínico.
2. Enriquecer esse dado com conteúdo textual médico.
3. Gerar a resposta com um modelo fine-tuned ou instruído.
4. Validar a saída antes de retornar.

## Estruturas comuns

- Identificação sintética do caso
- Queixa principal
- Histórico clínico resumido
- Medicações
- Sinais vitais
- Hipótese/conduta

## Fluxos similares úteis

- Classificação de intenção com contexto estruturado.
- Assistente de suporte com memória curta baseada em estado.
- RAG com metadados clínicos para selecionar contexto relevante.
- Pipeline de triagem com nós de validação e enriquecimento.

## Como aplicar ao projeto

- Usar `MedQuAD` e `PubMedQA` como fonte para gerar casos sintéticos.
- Transformar perguntas e respostas em registros clínicos fictícios.
- Alimentar o grafo com esse estado estruturado.
- Produzir respostas contextualizadas e marcadas como sintéticas.

## Observação

Ainda não há, na wiki, um exemplo pronto de prontuário real. A alternativa segura é criar registros fictícios e documentar explicitamente que são sintéticos.
