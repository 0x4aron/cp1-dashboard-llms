# CP1 — Dashboard profissional: Dados e LLMs

> Roteiro de apoio da apresentação. A versão PowerPoint em `deliverables/` já inclui
> as capturas e os gráficos; antes da entrega, confirme que você consegue explicar
> os números e as limitações.

## Slide 1 — Capa

- **Título:** Desempenho e eficiência de LLMs open-weight
- **Subtítulo:** Um estudo de mercado para aplicações de dados e IA no setor financeiro
- **Aluno:** César Aaron Herrera · Turma 2ESPH · RM 565398 · 25/08/2026

## Slide 2 — Contexto profissional

- Minha área de interesse: engenharia de dados e aplicações de LLMs.
- Cenário: organizações precisam comparar qualidade, porte, licença e impacto de infraestrutura antes de selecionar um modelo.
- **Conexão pessoal:** quero atuar com engenharia de dados e aplicações de LLMs no setor financeiro. Comparar desempenho, porte e licença é um exercício próximo das decisões técnicas que pretendo apoiar profissionalmente.

## Slide 3 — Pergunta de análise

> Modelos menores conseguem entregar desempenho competitivo para projetos que precisam equilibrar qualidade e recursos computacionais?

- População observada: modelos open-weight disponíveis na fonte escolhida.
- Unidade de análise: um modelo avaliado no leaderboard.
- Observação: o estudo compara benchmarks gerais; ele não valida diretamente uma solução financeira em produção.

## Slide 4 — Fonte e preparação dos dados

- **Fonte:** Open LLM Leaderboard / Hugging Face.
- **Data de extração:** 25/08/2026.
- **Registros brutos:** 4.576.
- **Registros após padronização:** 4.497; 4.487 válidos para análise de porte e score.
- Campos analisados: nome, organização, parâmetros, score médio, benchmarks, licença e CO₂ estimado.
- Tratamentos aplicados: conversão de tipos numéricos e remoção de duplicidades por nome do modelo.

Inclua uma captura da tabela filtrada do dashboard.

## Slide 5 — Estatísticas descritivas

Inclua os quatro indicadores do dashboard e complete:

- Quantidade de modelos sem filtros adicionais: 4.487.
- Média do score: 21,86.
- Mediana do score: 22,00.
- Desvio-padrão: 10,80.
- Maior score: 52,08 — MaziyarPanahi/calme-3.2-instruct-78b.

**Interpretação:** média e mediana diferem apenas 0,14 ponto no recorte completo. Isso indica centro semelhante pelas duas medidas, embora o histograma ainda seja necessário para observar o formato da distribuição e valores extremos.

## Slide 6 — Porte do modelo × desempenho

Inclua a captura do gráfico de dispersão.

- Tendência observada: a correlação de Pearson é 0,43, uma associação positiva moderada entre porte e score.
- Caso interessante: entre modelos de até 15B, JungZoona/T3Q-qwen2.5-14b-v1.0-e3 alcança 47,09 pontos com 14,77B parâmetros, próximo do grupo de maior desempenho geral.
- Limite de interpretação: correlação visual não prova que aumentar parâmetros causa aumento do score.

## Slide 7 — Benchmarks e comparação de modelos

Inclua as capturas do Top 10 e da matriz de correlação.

- Benchmark com maior associação ao score médio: MMLU-Pro (correlação de 0,95).
- Diferença encontrada: as associações variam; MuSR apresenta a menor correlação com o score médio entre os seis benchmarks (0,69).
- Implicação: um único benchmark não é suficiente para decidir a escolha de um modelo.

## Slide 8 — Conclusões e recomendação

- **Insight 1:** modelos maiores tendem a apresentar scores mais altos, mas o porte explica apenas parte da variação observada.
- **Insight 2:** existem modelos de até 15B com desempenho próximo dos líderes, o que sustenta uma triagem orientada a eficiência.
- **Recomendação:** investigar primeiro candidatos de até 15B com score elevado e licença compatível, antes de comparar custo, latência e qualidade em uma tarefa financeira controlada.
- **Limitação:** benchmarks gerais, dados históricos, diferenças de protocolo e ausência de testes com dados financeiros reais.

## Slide 9 — Próximos passos

- Avaliar modelos candidatos em uma tarefa financeira definida e sem dados sensíveis.
- Medir custo, latência, segurança e qualidade com critérios de negócio.
- Criar uma prova de conceito com logs, monitoramento e avaliação humana.

## Slide 10 — Demonstração

- Link do dashboard: https://cesar-aaron-llms.streamlit.app
- Repositório: https://github.com/0x4aron/cp1-dashboard-llms
- Demonstre filtros por licença e porte e explique uma mudança de resultado.
