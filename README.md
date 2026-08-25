# CP1 — Dashboard de Dados e LLMs (base de estudo)

Este projeto é um ponto de partida para estudar Streamlit e estruturar o CP1. Antes de usar qualquer conteúdo em uma entrega, complete os textos marcados como `TODO`, valide os cálculos e escreva suas próprias interpretações.

Repositório público: [0x4aron/cp1-dashboard-llms](https://github.com/0x4aron/cp1-dashboard-llms).

## Tema e pergunta

**Tema:** estudo de mercado de LLMs open-weight para aplicações de dados no setor financeiro.

**Pergunta:** modelos menores conseguem entregar desempenho competitivo para projetos que precisam equilibrar qualidade e recursos computacionais?

## Dados

Use uma cópia local e datada do [dataset `open-llm-leaderboard/contents`](https://huggingface.co/datasets/open-llm-leaderboard/contents) do Hugging Face. A análise precisa identificar a data de extração, a fonte e as limitações: benchmarks gerais não são uma medição direta de qualidade em tarefas financeiras ou em produção.

Para gerar uma cópia local e normalizada, execute:

```bash
python fetch_and_prepare_dataset.py
```

O processo cria `data/llm_leaderboard.csv` e `data/source_metadata.json`. A
segunda contém a fonte, a data de extração e o número de linhas obtidas. Em
seguida, revise a base e remova apenas registros que você consiga justificar.

O CSV resultante tem, entre outras, estas colunas normalizadas:

```text
model_name,organization,parameters_b,average_score,benchmark_1,benchmark_2,license,release_date
```

Abra o arquivo `data/llm_leaderboard_template.csv` como referência de formato. Não use os dados de exemplo como análise final.

## Execução local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Checklist de autoria e apresentação

- Reescrevi as seções de perfil, qualificações e skills com informações que posso defender.
- Registrei a fonte e a data de obtenção da base.
- Verifiquei dados nulos, duplicados e unidades das colunas.
- Expliquei média, mediana, dispersão e correlação sem inferir causalidade.
- Registrei ao menos uma limitação da análise.
- Preparei a apresentação coringa com prints, pergunta, método, gráficos e conclusões.

O arquivo [presentation_coringa.md](presentation_coringa.md) traz um roteiro de 10 slides para essa apresentação. Use-o como estrutura e complete as interpretações com suas próprias palavras.

## Publicação

Depois de validar localmente, crie você mesmo um repositório GitHub com `app.py`, `requirements.txt` e a base permitida. Em seguida, conecte-o à sua conta no [Streamlit Community Cloud](https://share.streamlit.io/) e escolha `app.py` como arquivo principal. Não envie credenciais, dados pessoais ou dados confidenciais ao repositório. Veja o passo a passo completo em [DEPLOYMENT.md](DEPLOYMENT.md).

O arquivo `.gitignore` já evita o envio do ambiente virtual e de arquivos temporários. A pasta `data/` deve permanecer no projeto se a base fizer parte do entregável solicitado pelo professor.
