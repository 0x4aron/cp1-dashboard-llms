import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Portfólio | Dados e LLMs", page_icon="📊", layout="wide")
st.markdown(
    """
    <style>
        .stApp { background: #f7f9fc; }
        [data-testid="stMetricValue"] { color: #175cd3; }
        h1, h2, h3 { color: #101828; }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_PATH = Path("data/llm_leaderboard.csv")
METADATA_PATH = Path("data/source_metadata.json")
REQUIRED_COLUMNS = {"model_name", "organization", "parameters_b", "average_score", "license"}


@st.cache_data
def load_data(uploaded_file=None):
    """Carrega o CSV padronizado que será usado na análise."""
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return None


def validate_data(dataframe: pd.DataFrame) -> list[str]:
    missing = REQUIRED_COLUMNS.difference(dataframe.columns)
    return [f"Coluna obrigatória ausente: `{column}`" for column in sorted(missing)]


def load_metadata() -> dict:
    """Lê os dados de proveniência gerados junto ao CSV, se disponíveis."""
    if METADATA_PATH.exists():
        return json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return {}


def render_profile():
    st.title("Quem sou eu")
    st.markdown(
        """
        Sou **César Aaron Herrera**, estudante de Engenharia de Software na FIAP,
        com interesse em engenharia de dados e aplicações de modelos de linguagem
        (LLMs) no setor financeiro.

        Minha experiência em suporte e infraestrutura de TI desenvolveu minha
        capacidade de diagnosticar problemas, comunicar soluções técnicas e atuar
        em ambientes dinâmicos. Busco aplicar Python, SQL e cloud em projetos que
        transformem dados confiáveis em decisões melhores.

        Este dashboard une duas áreas em que pretendo me desenvolver: análise de
        dados e avaliação de LLMs. O estudo de mercado permite observar critérios
        relevantes para uma futura adoção profissional, como desempenho, porte e
        licença de modelos open-weight.
        """
    )


def render_qualifications():
    st.title("Minhas qualificações")
    education, experience = st.columns(2)
    with education:
        st.subheader("Formação")
        st.markdown(
            """
            **Engenharia de Software — FIAP**  
            3º semestre · conclusão prevista em dez/2028

            **Técnico em Administração — Etec Arujá**  
            Concluído em 2024 · TCC sobre o impacto da IA no comércio.
            """
        )
    with experience:
        st.subheader("Experiência")
        st.markdown(
            """
            **Monitor de Laboratório de TI — FIAP**  
            Suporte técnico, configuração de ambientes e diagnóstico de incidentes.

            **Operador de Atendimento ao Cliente — Konecta**  
            Atendimento orientado a resolução, satisfação e registro em CRM.
            """
        )

    st.subheader("Projetos e cursos relevantes")
    st.markdown(
        """
        - **FIAP Monitor:** sistema de suporte a laboratórios com chat em tempo real
          e monitoramento remoto; 1º lugar em hackathon interno de estagiários.
        - **Projetos acadêmicos e open source:** simulador de ATM com DDD, apoio à
          decisão com algoritmos e contribuições aceitas no projeto Yara.
        - **Cursos:** Imersão Inteligência Artificial (Alura) e Design Thinking e
          Processos de Inovação (FIAP).
        """
    )


def render_skills():
    st.title("Skills")
    technical, interpersonal = st.columns(2)
    with technical:
        st.subheader("Técnicas")
        st.markdown(
            "Python · SQL · Java · JavaScript · C++ · Pandas · Visualização de Dados · "
            "Git/GitHub · AWS · Cloud e infraestrutura"
        )
    with interpersonal:
        st.subheader("Comportamentais")
        st.markdown("Comunicação técnica · Autonomia · Curiosidade · Resolução de problemas · Adaptabilidade")
    st.subheader("Idiomas")
    st.markdown("Português (nativo) · Inglês (fluente) · Espanhol (fluente) · Norueguês e Russo (básico)")
    st.caption("Competências apresentadas conforme currículo; revise-as antes de entregar e citar em uma entrevista.")


def render_analysis(dataframe: pd.DataFrame | None):
    st.title("Estudo de mercado: LLMs open-weight")
    st.markdown(
        "**Pergunta de análise:** modelos menores conseguem entregar desempenho competitivo "
        "para projetos que precisam equilibrar qualidade e recursos computacionais?"
    )
    metadata = load_metadata()
    if metadata:
        st.caption(
            f"Fonte: {metadata['source_dataset']} · extração em "
            f"{metadata['extracted_at_utc']} · {metadata['normalized_records']} registros."
        )

    uploaded_file = st.file_uploader("Envie o CSV padronizado", type="csv")
    if uploaded_file is not None:
        dataframe = load_data(uploaded_file)

    if dataframe is None:
        st.warning("Inclua `data/llm_leaderboard.csv` ou envie o arquivo nesta página.")
        st.code("model_name,organization,parameters_b,average_score,benchmark_1,benchmark_2,license,release_date")
        return

    problems = validate_data(dataframe)
    if problems:
        st.error("O arquivo ainda não está no formato esperado.")
        st.markdown("\n".join(f"- {problem}" for problem in problems))
        return

    dataframe = dataframe.copy()
    dataframe["parameters_b"] = pd.to_numeric(dataframe["parameters_b"], errors="coerce")
    dataframe["average_score"] = pd.to_numeric(dataframe["average_score"], errors="coerce")
    dataframe = dataframe.dropna(subset=["parameters_b", "average_score"])

    with st.sidebar:
        st.subheader("Filtros da análise")
        licenses = sorted(dataframe["license"].dropna().astype(str).unique())
        selected_licenses = st.multiselect("Licenças", licenses, default=licenses)
        max_parameters = float(dataframe["parameters_b"].max())
        parameter_range = st.slider("Parâmetros (bilhões)", 0.0, max_parameters, (0.0, max_parameters))

    filtered = dataframe[
        dataframe["license"].astype(str).isin(selected_licenses)
        & dataframe["parameters_b"].between(*parameter_range)
    ]
    if filtered.empty:
        st.warning("Nenhum modelo atende aos filtros selecionados.")
        return

    median_score = filtered["average_score"].median()
    mean_score = filtered["average_score"].mean()
    best = filtered.loc[filtered["average_score"].idxmax()]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Modelos analisados", len(filtered))
    col2.metric("Score médio", f"{mean_score:.2f}")
    col3.metric("Score mediano", f"{median_score:.2f}")
    col4.metric("Maior score", f"{best['average_score']:.2f}", best["model_name"])

    left, right = st.columns(2)
    with left:
        fig = px.scatter(
            filtered,
            x="parameters_b",
            y="average_score",
            color="license",
            hover_name="model_name",
            hover_data=["organization"],
            title="Porte do modelo × desempenho médio",
            labels={"parameters_b": "Parâmetros (bilhões)", "average_score": "Score médio"},
        )
        st.plotly_chart(fig, width="stretch")
    with right:
        top_models = filtered.nlargest(10, "average_score").sort_values("average_score")
        fig = px.bar(
            top_models,
            x="average_score",
            y="model_name",
            color="parameters_b",
            orientation="h",
            title="Top 10 modelos por score médio",
            labels={"average_score": "Score médio", "model_name": "Modelo", "parameters_b": "Parâmetros (B)"},
        )
        st.plotly_chart(fig, width="stretch")

    benchmark_columns = [c for c in dataframe.columns if c.startswith("benchmark_")]
    if benchmark_columns:
        st.subheader("Comparação entre benchmarks")
        numeric_benchmarks = filtered[benchmark_columns].apply(pd.to_numeric, errors="coerce")
        st.plotly_chart(
            px.imshow(numeric_benchmarks.corr(), text_auto=".2f", title="Correlação entre benchmarks"),
            width="stretch",
        )

    st.subheader("Conclusão do estudante")
    st.text_area(
        "Explique os achados com base nos gráficos e nas estatísticas; não afirme causalidade apenas pela correlação.",
        placeholder="TODO: descreva pelo menos dois insights e uma limitação da base.",
        height=150,
    )
    st.subheader("Dados filtrados")
    st.dataframe(filtered, width="stretch", hide_index=True)


st.sidebar.title("Portfólio profissional")
st.sidebar.caption("Dados · IA · LLMs")
page = st.sidebar.radio("Navegação", ["Quem sou eu", "Qualificações", "Skills", "Análise de Dados"])

if page == "Quem sou eu":
    render_profile()
elif page == "Qualificações":
    render_qualifications()
elif page == "Skills":
    render_skills()
else:
    # A base só é lida quando a área analítica é aberta, reduzindo o tempo da tela inicial.
    render_analysis(load_data())
