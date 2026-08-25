# CP1 — Portfólio de Dados e LLMs

Dashboard profissional desenvolvido em Python e Streamlit para o CP1 de **Data Science and Statistical Computing**. O projeto conecta o objetivo profissional de César Aaron Herrera — engenharia de dados e aplicações de LLMs no setor financeiro — a um estudo de mercado baseado no Open LLM Leaderboard.

**Aluno:** César Aaron Herrera · **Turma:** 2ESPH · **RM:** 565398

**Dashboard publicado:** [cesar-aaron-llms.streamlit.app](https://cesar-aaron-llms.streamlit.app)

**Repositório:** [0x4aron/cp1-dashboard-llms](https://github.com/0x4aron/cp1-dashboard-llms)

## Entregáveis acadêmicos

- Link público do dashboard acima.
- Código-fonte, dependências e configuração do Streamlit.
- Base local em `data/llm_leaderboard.csv` e metadados da fonte.
- Apresentação coringa em PowerPoint na pasta `deliverables/`.
- Roteiro editável em `presentation_coringa.md`.

## Estrutura do dashboard

- **Quem sou eu:** posicionamento profissional, foco de carreira e proposta de valor.
- **Qualificações:** formação, experiência, cursos e projetos relevantes.
- **Skills:** competências técnicas, humanas e idiomas.
- **Análise de Dados:** estatísticas descritivas, filtros, distribuição, correlação, faixas de porte, benchmarks, síntese e limitações.

Cada área utiliza uma rota própria para manter a navegação estável no Streamlit Community Cloud.

## Pergunta de análise

> Modelos menores conseguem entregar desempenho competitivo para projetos que precisam equilibrar qualidade e recursos computacionais?

O dashboard apresenta evidências para uma triagem inicial de modelos open-weight. A análise não substitui avaliações em tarefas financeiras reais e não interpreta correlação como causalidade.

## Dados e preparação

A cópia local e datada foi obtida do dataset público [`open-llm-leaderboard/contents`](https://huggingface.co/datasets/open-llm-leaderboard/contents), no Hugging Face.

- 4.576 registros brutos.
- 4.497 registros após normalização.
- 4.487 registros válidos para a análise de porte e score.
- 0 duplicidades exatas na base normalizada.
- Campos principais: modelo, organização, parâmetros, score médio, seis benchmarks, licença, data, CO₂ estimado e tipo.

O script [`fetch_and_prepare_dataset.py`](fetch_and_prepare_dataset.py) reproduz a coleta e cria:

- `data/llm_leaderboard.csv`
- `data/source_metadata.json`

## Execução local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Decisões de qualidade

- Tema claro definido em `.streamlit/config.toml` para garantir contraste consistente.
- Base carregada sob demanda e mantida em cache.
- Registros com porte não positivo ou score inválido não entram nos cálculos.
- Filtros de licença, porte e score atualizam indicadores e gráficos.
- Gráficos usam paleta consistente, fundo claro e textos de alto contraste.
- Fonte, data de extração, tratamento e limitações ficam documentados no próprio app.

## Entregáveis

- Link público do dashboard.
- Código-fonte e base no repositório.
- Arquivo ZIP do projeto.
- Roteiro da apresentação coringa em [`presentation_coringa.md`](presentation_coringa.md).

## Limitações

Os benchmarks são gerais e dependem do protocolo de avaliação. Número de parâmetros não representa sozinho custo, latência ou qualidade em produção. Uma decisão no setor financeiro também exige avaliação de segurança, privacidade, licença, dados do domínio e revisão humana.
