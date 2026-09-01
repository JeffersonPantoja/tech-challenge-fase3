# Requisitos Técnicos: Fine-Tuning de LLM com Dados Médicos Internos

Este documento detalha a especificação e as diretrizes de execução para a etapa de **Fine-Tuning de LLM**, extraídas dos requisitos obrigatórios do **Tech Challenge (Fase 3 - Pos Tech)**. 

---

## 1. Visão Geral do Requisito

O objetivo principal desta etapa é adaptar um Modelo de Linguagem de Grande Porte (LLM) de código aberto para atuar no domínio médico-hospitalar, capacitando o assistente virtual a compreender protocolos internos, responder a dúvidas de profissionais de saúde e sugerir procedimentos validados.

---

## 2. Especificações Técnicas de Fine-Tuning

### 2.1. Escolha do Modelo Base (*Base LLM*)
- **Modelos Recomendados:** LLaMA, Falcon ou outro modelo *open-source* equivalente adequado para fine-tuning/instruções técnicas.
- **Premissa:** Escolher um modelo que permita ajuste fino e execução dentro da infraestrutura estipulada.

### 2.2. Composição e Fontes do Dataset Interno
O treinamento deve ser realizado utilizando dados representativos do ecossistema hospitalar:
- **Protocolos Médicos do Hospital:** Diretrizes clínicas e fluxos operacionais internos.
- **Perguntas Frequentes (FAQs Médicas):** Exemplos práticos de dúvidas reais ou simuladas de médicos durante a rotina.
- **Modelos de Documentos Clínicos:** Laudos, receitas médicas, prontuários e descrições de procedimentos internos.

### 2.3. Pipeline de Preparação e Tratamento de Dados
Antes da etapa de treinamento, o pipeline deve implementar obrigatoriamente:
1. **Pré-processamento (*Preprocessing*):** Limpeza, estruturação e formatação dos textos para o formato aceito pelo modelo (ex: formatos de instrução/prompt-completion).
2. **Anonimização (LGPD / Proteção de Dados):** Remoção completa de Informações de Identificação Pessoal (PII) e dados sensíveis de pacientes ou profissionais de saúde.
3. **Curadoria dos Dados:** Filtro de qualidade para garantir factualidade, consistência médica e ausência de informações conflitantes.

---

## 3. Datasets Públicos / Sintéticos Sugeridos

Caso sejam necessários dados complementares para apoio ao fine-tuning ou teste, o documento sugere a utilização das seguintes bases médicas abertas:

| Dataset | Conteúdo | Referência |
| :--- | :--- | :--- |
| **PubMedQA** | Perguntas e respostas clínicas baseadas em publicações médicas | [pubmedqa.github.io](https://pubmedqa.github.io) |
| **MedQuAD** | Conjunto abrangente de perguntas e respostas sobre saúde | [github.com/abachaa/MedQuAD](https://github.com/abachaa/MedQuAD) |

---

## 4. Entregáveis Esperados para esta Etapa

Como parte da avaliação do projeto, os artefatos abaixo relacionados ao Fine-Tuning devem ser incluídos no repositório Git:

- [x] **Pipeline de Fine-Tuning:** Código-fonte em Python modularizado com o script de pré-processamento, carregamento de dados e loop de treinamento/ajuste fino.
- [x] **Dataset Anonimizado / Sintético:** Amostra tratada dos dados utilizados no treinamento.
- [x] **Relatório Técnico Detalhado:** Documentação contendo a explicação do processo de fine-tuning, parâmetros utilizados e a avaliação dos resultados/métricas do modelo treinado.
- [x] **Demonstração em Vídeo:** Gravação (até 15 min) demonstrando o treinamento e funcionamento da LLM personalizada respondendo a perguntas clínicas contextualizadas.
