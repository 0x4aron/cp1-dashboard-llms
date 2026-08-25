# CP1 — Dashboard profissional: Dados e LLMs

> Use este roteiro para montar os slides. Troque todos os campos entre colchetes
> e inclua capturas do seu dashboard já preenchido. A apresentação deve refletir
> apenas análises que você conferiu e consegue explicar.

## Slide 1 — Capa

- **Título:** Desempenho e eficiência de LLMs open-weight
- **Subtítulo:** Um estudo de mercado para aplicações de dados e IA no setor financeiro
- **Aluno:** [seu nome] · [turma] · [data]

## Slide 2 — Contexto profissional

- Minha área de interesse: engenharia de dados e aplicações de LLMs.
- Cenário: organizações precisam comparar qualidade, porte, licença e impacto de infraestrutura antes de selecionar um modelo.
- **Conexão pessoal:** [em 2–3 frases, explique por que o tema é relevante para seus objetivos profissionais].

## Slide 3 — Pergunta de análise

> Modelos menores conseguem entregar desempenho competitivo para projetos que precisam equilibrar qualidade e recursos computacionais?

- População observada: modelos open-weight disponíveis na fonte escolhida.
- Unidade de análise: um modelo avaliado no leaderboard.
- Observação: o estudo compara benchmarks gerais; ele não valida diretamente uma solução financeira em produção.

## Slide 4 — Fonte e preparação dos dados

- **Fonte:** Open LLM Leaderboard / Hugging Face.
- **Data de extração:** [copie de `data/source_metadata.json`].
- **Registros brutos:** [copie de `data/source_metadata.json`].
- **Registros após padronização:** [copie de `data/source_metadata.json`].
- Campos analisados: nome, organização, parâmetros, score médio, benchmarks, licença e CO₂ estimado.
- Tratamentos aplicados: conversão de tipos numéricos e remoção de duplicidades por nome do modelo.

Inclua uma captura da tabela filtrada do dashboard.

## Slide 5 — Estatísticas descritivas

Inclua os quatro indicadores do dashboard e complete:

- Quantidade de modelos após filtros: [valor].
- Média do score: [valor].
- Mediana do score: [valor].
- Maior score e respectivo modelo: [valor].

**Interpretação própria:** [descreva se a média e a mediana estão próximas ou afastadas e o que isso sugere sobre a distribuição].

## Slide 6 — Porte do modelo × desempenho

Inclua a captura do gráfico de dispersão.

- Tendência observada: [descreva somente o que o gráfico mostra].
- Exceção ou caso interessante: [modelo/intervalo de porte].
- Limite de interpretação: correlação visual não prova que aumentar parâmetros causa aumento do score.

## Slide 7 — Benchmarks e comparação de modelos

Inclua as capturas do Top 10 e da matriz de correlação.

- Benchmark com maior associação ao score médio: [preencha após verificar].
- Diferença encontrada entre benchmarks: [preencha].
- Implicação: um único benchmark não é suficiente para decidir a escolha de um modelo.

## Slide 8 — Conclusões e recomendação

- **Insight 1:** [resultado sustentado por um gráfico ou estatística].
- **Insight 2:** [resultado sustentado por um gráfico ou estatística].
- **Recomendação:** [perfil de modelo que você investigaria primeiro e justificativa].
- **Limitação:** benchmarks gerais, dados históricos e ausência de testes com dados financeiros reais.

## Slide 9 — Próximos passos

- Avaliar modelos candidatos em uma tarefa financeira definida e sem dados sensíveis.
- Medir custo, latência, segurança e qualidade com critérios de negócio.
- Criar uma prova de conceito com logs, monitoramento e avaliação humana.

## Slide 10 — Demonstração

- Link do dashboard: [URL depois da publicação].
- Repositório: [URL do GitHub].
- Demonstre filtros por licença e porte e explique uma mudança de resultado.
