# Sistema de Memória para Agentes de IA: Padrão LLM Wiki (Karpathy)

Este documento descreve os conceitos e arquitetura de memória persistente baseados no padrão **LLM Wiki** proposto por **Andrej Karpathy** e detalhado na análise de **Fabio Akita**, servindo como diretriz de design e referência técnica para este projeto desenvolvido via *Vibe Coding* com o **opencode**.

---

## 1. O Problema da Memória em LLMs e a Limitação da *Compaction*

Modelos de linguagem não possuem memória persistente nativa. Toda a interatividade baseia-se na janela de contexto enviada a cada turno. Quando a janela se aproxima do limite (por exemplo, em sessões longas de coding), os agentes de CLI (como *opencode*, *Claude Code* e *Codex*) disparam processos de **Compaction** (resumo/compactação do histórico).

Embora a compactação evite o estouro do limite de tokens, ela possui desvantagens críticas:
- **Perda de detalhes sutis:** Decisões tomadas no início da sessão podem ser purgadas ou excessivamente sintetizadas.
- **Custo financeiro e latência:** Reenviar contextos massivos e rodar chamadas contínuas de compactação consome cota e reduz a velocidade de resposta.
- **Volatilidade entre sessões:** Ao encerrar ou reiniciar o agente, o contexto volátil desaparece.

---

## 2. O Padrão *LLM Wiki* de Andrej Karpathy

Para resolver a limitação da memória de curto prazo (janela de contexto), Andrej Karpathy propõe o uso de uma **Wiki Estruturada mantida pela própria IA** como mecanismo de memória de longo prazo (*Long-Term Memory*).

### Princípios de Funcionamento:
1. **Conhecimento Digestivo e Ativo:** Em vez de depender apenas de RAG passivo (busca vetorial bruta sobre arquivos esparsos), a IA compõe, edita e reorganiza ativamente artigos e sínteses em arquivos `.md` estruturados.
2. **Navegabilidade por Hiperlinks e Índices:** A estrutura utiliza convenções claras de nomenclatura, links e seções para permitir que a IA leia e atualize tópicos específicos sob demanda.
3. **Redução de Alucinações:** Fatos cruciais, convenções do projeto e decisões de arquitetura ficam ancorados na Wiki, evitando reprocessar outputs de terminal e logs brutos.
4. **Armazenamento em Texto Puro (Markdown):** Garante auditabilidade humana, portabilidade extrema e alinhamento nativo com a forma como as LLMs processam tokens.

---

## 3. Recomendações e Análises Práticas (Akita)

Na análise prática conduzida por Akita sobre a gestão de memória para agentes:

- **Memória é Texto:** A gestão de memória não exige obrigatoriamente bancos de dados complexos ou infraestruturas pesadas. Arquivos de texto estruturados (`.md`) bem geridos superam arquiteturas frágeis de indexação vetorial contínua.
- **Ancoragem Incremental:** O modelo deve atualizar o conhecimento de forma incremental (estilo o *anchored summary* do opencode), mesclando novos fatos e removendo detalhes obsoletos sem reconstruir o histórico do zero a cada alteração.
- **Supervisão do Desenvolvedor:** O fluxo de *vibe coding* é otimizado quando o desenvolvedor atua na curadoria do topo da Wiki (índices e especificações primárias), permitindo que o agente navegue autonomamente pelo conteúdo granular.

---

## 4. Aplicação Prática no Projeto (`opencode`)

Neste repositório, a memória e a documentação técnica são organizadas seguindo o padrão da LLM Wiki na seguinte estrutura base:

```text
├── documentos/
│   ├── especificacoes/         # Especificações originais e requisitos (PDFs/Briefings)
│   ├── wiki-projeto/           # LLM Wiki ativa (visão geral, decisões de arquitetura, manuais)
│   └── wiki-referencia/        # Artigos, guias externos e referências de APIs
```

### Regras de Engajamento para o `opencode`:
* **Consulta Obrigatória:** Antes de iniciar refatorações complexas, consulte a pasta `documentos/wiki-projeto/`.
* **Atualização da Wiki:** Ao finalizar um requisito importante ou tomar uma decisão de design, registre ou atualize a página Markdown correspondente na Wiki.
* **Manutenção do Contexto:** Mantenha os resumos concisos e diretos para otimizar o uso do buffer de tokens do `opencode`.
