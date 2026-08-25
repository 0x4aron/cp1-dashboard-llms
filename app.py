import json
from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="César Aaron | Dados e LLMs",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path("data/llm_leaderboard.csv")
METADATA_PATH = Path("data/source_metadata.json")
REQUIRED_COLUMNS = {"model_name", "organization", "parameters_b", "average_score", "license"}
COLORS = {
    "ink": "#172033",
    "muted": "#5B6475",
    "blue": "#2563EB",
    "violet": "#7C3AED",
    "green": "#059669",
}

st.markdown(
    """
    <style>
        :root { color-scheme: light; }
        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        .stApp, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 96% 3%, rgba(37,99,235,.10), transparent 27rem),
                radial-gradient(circle at 4% 95%, rgba(124,58,237,.08), transparent 24rem),
                #F3F6FB;
            color: #172033;
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 1240px;
            padding-top: 2.5rem;
            padding-bottom: 5rem;
        }
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stCaptionContainer"],
        .stApp label { color: #172033; }
        h1, h2, h3, h4 { color: #0B1220 !important; letter-spacing: -.025em; }
        a { color: #1D4ED8; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0B1220 0%, #111C33 100%);
            border-right: 1px solid rgba(255,255,255,.08);
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #E8EEF8 !important; }
        [data-testid="stSidebarNav"] a {
            border-radius: 12px;
            margin: .25rem .6rem;
            color: #DDE7F7;
        }
        [data-testid="stSidebarNav"] a:hover { background: rgba(255,255,255,.08); }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(90deg, rgba(37,99,235,.40), rgba(124,58,237,.30));
            border: 1px solid rgba(147,197,253,.25);
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="input"] > div {
            background: #FFFFFF;
            color: #172033;
        }
        [data-testid="stMetric"] {
            background: rgba(255,255,255,.95);
            border: 1px solid #DCE3EE;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 25px rgba(15,23,42,.055);
        }
        [data-testid="stMetricLabel"] p { color: #5B6475 !important; font-weight: 650; }
        [data-testid="stMetricValue"] { color: #172033; }
        [data-testid="stMetricDelta"] { white-space: normal; }
        [data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid #DCE3EE;
            border-radius: 18px;
            padding: .35rem;
            box-shadow: 0 8px 28px rgba(15,23,42,.05);
        }
        [data-testid="stExpander"] {
            background: rgba(255,255,255,.82);
            border: 1px solid #DCE3EE;
            border-radius: 14px;
        }
        .page-kicker {
            color: #2563EB;
            font-size: .77rem;
            font-weight: 800;
            letter-spacing: .14em;
            text-transform: uppercase;
            margin-bottom: .45rem;
        }
        .page-title {
            color: #0B1220;
            font-size: clamp(2rem, 5vw, 3.35rem);
            line-height: 1.04;
            font-weight: 820;
            letter-spacing: -.045em;
            margin: 0;
        }
        .page-subtitle {
            color: #5B6475;
            font-size: 1.05rem;
            line-height: 1.7;
            max-width: 800px;
            margin: .9rem 0 1.8rem;
        }
        .hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(125deg, #0B1220 0%, #132A53 58%, #312E81 100%);
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 24px;
            padding: clamp(1.6rem, 4vw, 3.2rem);
            box-shadow: 0 22px 55px rgba(15,23,42,.20);
            margin: .5rem 0 1.5rem;
        }
        .hero:after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: -70px;
            top: -90px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(96,165,250,.50), rgba(124,58,237,0));
        }
        .hero-eyebrow { color: #93C5FD; font-size: .78rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
        .hero-name { color: #FFFFFF; font-size: clamp(2rem, 5vw, 3.55rem); line-height: 1.05; font-weight: 840; letter-spacing: -.045em; margin: .55rem 0; }
        .hero-role { color: #DCE8FB; font-size: 1.12rem; max-width: 780px; line-height: 1.65; margin-bottom: 1.25rem; }
        .tag {
            display: inline-block;
            color: #EAF2FF;
            background: rgba(255,255,255,.09);
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 999px;
            padding: .43rem .78rem;
            margin: .15rem .28rem .15rem 0;
            font-size: .86rem;
            font-weight: 650;
        }
        .card {
            height: 100%;
            background: rgba(255,255,255,.96);
            border: 1px solid #DCE3EE;
            border-radius: 18px;
            padding: 1.35rem;
            box-shadow: 0 9px 28px rgba(15,23,42,.055);
        }
        .card-icon { color: #2563EB; font-size: 1.45rem; margin-bottom: .7rem; }
        .card-title { color: #172033; font-size: 1.05rem; font-weight: 780; margin-bottom: .42rem; }
        .card-copy { color: #5B6475; font-size: .94rem; line-height: 1.62; }
        .timeline-card {
            background: #FFFFFF;
            border: 1px solid #DCE3EE;
            border-left: 4px solid #2563EB;
            border-radius: 0 16px 16px 0;
            padding: 1.15rem 1.25rem;
            margin-bottom: .85rem;
            box-shadow: 0 7px 22px rgba(15,23,42,.045);
        }
        .timeline-date { color: #2563EB; font-size: .75rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
        .timeline-title { color: #172033; font-size: 1.02rem; font-weight: 780; margin: .3rem 0; }
        .timeline-copy { color: #5B6475; font-size: .91rem; line-height: 1.58; }
        .skill-group { margin-bottom: .75rem; }
        .skill-chip {
            display: inline-block;
            color: #1E3A5F;
            background: #EAF2FF;
            border: 1px solid #CFE0FB;
            border-radius: 9px;
            padding: .42rem .67rem;
            margin: .22rem .18rem .05rem 0;
            font-size: .86rem;
            font-weight: 680;
        }
        .callout {
            background: linear-gradient(90deg, #EFF6FF, #F5F3FF);
            border: 1px solid #CFE0FB;
            border-radius: 16px;
            color: #25324A;
            padding: 1.1rem 1.25rem;
            line-height: 1.62;
            margin: 1rem 0 1.5rem;
        }
        .callout strong { color: #172033; }
        .section-label { color: #172033; font-size: 1.35rem; font-weight: 800; letter-spacing: -.025em; margin: 2rem 0 .85rem; }
        .insight {
            background: #FFFFFF;
            border: 1px solid #DCE3EE;
            border-radius: 16px;
            padding: 1.1rem 1.2rem;
            margin-bottom: .7rem;
        }
        .insight-number { color: #2563EB; font-size: .74rem; font-weight: 850; letter-spacing: .1em; }
        .insight-copy { color: #334155; line-height: 1.62; margin-top: .35rem; }
        div.stButton > button, div.stLinkButton > a { border-radius: 10px; font-weight: 720; }
        @media (max-width: 700px) {
            [data-testid="stMainBlockContainer"] { padding-top: 1.2rem; }
            .hero { border-radius: 18px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Preparando a base de modelos…")
def load_data(uploaded_file=None):
    """Carrega o CSV padronizado usado na análise."""
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return None


@st.cache_data
def load_metadata() -> dict:
    """Lê os dados de proveniência gerados junto ao CSV."""
    if METADATA_PATH.exists():
        return json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return {}


def validate_data(dataframe: pd.DataFrame) -> list[str]:
    missing = REQUIRED_COLUMNS.difference(dataframe.columns)
    return [f"Coluna obrigatória ausente: `{column}`" for column in sorted(missing)]


def prepare_data(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Padroniza tipos e remove apenas registros inválidos para a análise."""
    prepared = dataframe.copy()
    raw_rows = len(prepared)
    prepared["parameters_b"] = pd.to_numeric(prepared["parameters_b"], errors="coerce")
    prepared["average_score"] = pd.to_numeric(prepared["average_score"], errors="coerce")
    prepared["license"] = prepared["license"].fillna("não informada").astype(str)
    prepared["organization"] = prepared["organization"].fillna("não informada").astype(str)
    prepared = prepared.dropna(subset=["parameters_b", "average_score"])
    prepared = prepared[prepared["parameters_b"] > 0].copy()
    prepared["size_group"] = pd.cut(
        prepared["parameters_b"],
        bins=[0, 3, 8, 15, 35, 70, float("inf")],
        labels=["até 3B", "3–8B", "8–15B", "15–35B", "35–70B", "acima de 70B"],
        include_lowest=True,
    )
    quality = {
        "raw_rows": raw_rows,
        "valid_rows": len(prepared),
        "removed_rows": raw_rows - len(prepared),
        "duplicates": int(dataframe.duplicated().sum()),
        "licenses": int(prepared["license"].nunique()),
    }
    return prepared, quality


def page_header(kicker: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="page-kicker">{escape(kicker)}</div>
        <div class="page-title">{escape(title)}</div>
        <div class="page-subtitle">{escape(subtitle)}</div>
        """,
        unsafe_allow_html=True,
    )


def card(icon: str, title: str, copy: str):
    st.markdown(
        f"""
        <div class="card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{escape(title)}</div>
            <div class="card-copy">{escape(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def timeline(date: str, title: str, copy: str):
    st.markdown(
        f"""
        <div class="timeline-card">
            <div class="timeline-date">{escape(date)}</div>
            <div class="timeline-title">{escape(title)}</div>
            <div class="timeline-copy">{escape(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def skill_card(title: str, skills: list[str]):
    chips = "".join(f'<span class="skill-chip">{escape(skill)}</span>' for skill in skills)
    st.markdown(
        f'<div class="card"><div class="card-title">{escape(title)}</div><div class="skill-group">{chips}</div></div>',
        unsafe_allow_html=True,
    )


def style_figure(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color=COLORS["ink"], family="Inter, Arial, sans-serif", size=12),
        title_font=dict(color=COLORS["ink"], size=17),
        margin=dict(l=35, r=25, t=65, b=40),
        legend_title_text="",
        hoverlabel=dict(bgcolor="#FFFFFF", font_color=COLORS["ink"]),
    )
    fig.update_xaxes(gridcolor="#E8EDF5", zerolinecolor="#DCE3EE")
    fig.update_yaxes(gridcolor="#E8EDF5", zerolinecolor="#DCE3EE")
    return fig


def correlation_label(value: float) -> str:
    if pd.isna(value):
        return "amostra insuficiente"
    magnitude = abs(value)
    if magnitude < 0.2:
        strength = "muito fraca"
    elif magnitude < 0.4:
        strength = "fraca"
    elif magnitude < 0.6:
        strength = "moderada"
    elif magnitude < 0.8:
        strength = "forte"
    else:
        strength = "muito forte"
    direction = "positiva" if value >= 0 else "negativa"
    return f"{strength} e {direction}"


def render_profile():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">Engenharia de Software · Dados · Inteligência Artificial</div>
            <div class="hero-name">César Aaron Herrera</div>
            <div class="hero-role">
                Estudante da FIAP com experiência prática em suporte e infraestrutura de TI,
                construindo uma trajetória em engenharia de dados e aplicações de LLMs no setor financeiro.
            </div>
            <span class="tag">Python & SQL</span>
            <span class="tag">Data Engineering</span>
            <span class="tag">LLMs</span>
            <span class="tag">AWS</span>
            <span class="tag">Trilíngue</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    with cols[0]:
        card("◎", "Foco profissional", "Transformar dados confiáveis em decisões úteis, com interesse especial em aplicações responsáveis de IA no mercado financeiro.")
    with cols[1]:
        card("◇", "Base prática", "Experiência em diagnóstico de incidentes, configuração de ambientes, suporte técnico e comunicação com usuários em contextos dinâmicos.")
    with cols[2]:
        card("↗", "Próximo passo", "Consolidar Python, SQL, cloud e engenharia de software em projetos de dados com impacto mensurável e boa experiência de uso.")

    st.markdown('<div class="section-label">Minha proposta de valor</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="callout">
            Combino <strong>raciocínio técnico</strong>, vivência de atendimento e curiosidade por negócios.
            Este portfólio demonstra essa interseção: uma aplicação funcional, uma base pública rastreável
            e uma análise de mercado sobre modelos de linguagem que equilibra desempenho, porte e licença.
        </div>
        """,
        unsafe_allow_html=True,
    )
    links = st.columns([1, 1, 2])
    with links[0]:
        st.link_button("LinkedIn", "https://linkedin.com/in/cesaraaronherrera", width="stretch")
    with links[1]:
        st.link_button("GitHub", "https://github.com/0x4aron", width="stretch")


def render_qualifications():
    page_header(
        "Trajetória",
        "Formação que encontra prática.",
        "Experiências acadêmicas e profissionais que construíram minha base em tecnologia, atendimento e resolução de problemas.",
    )
    kpis = st.columns(3)
    kpis[0].metric("Formação atual", "Eng. de Software", "FIAP · 3º semestre")
    kpis[1].metric("Experiência atual", "Laboratórios de TI", "FIAP · desde jun/2025")
    kpis[2].metric("Destaque", "1º lugar", "Hackathon FIAP Monitor")

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown('<div class="section-label">Formação</div>', unsafe_allow_html=True)
        timeline("Conclusão prevista · dez/2028", "Bacharelado em Engenharia de Software — FIAP", "Formação em desenvolvimento de software, arquitetura, dados e computação aplicada.")
        timeline("Concluído · 2024", "Técnico em Administração — Etec Arujá", "TCC sobre o impacto da inteligência artificial no comércio e na otimização de processos.")
        st.markdown('<div class="section-label">Cursos complementares</div>', unsafe_allow_html=True)
        timeline("2025", "Imersão Inteligência Artificial — Alura", "Fundamentos e aplicações práticas de inteligência artificial.")
        timeline("2025", "Design Thinking e Processos de Inovação — FIAP", "Abordagem centrada no usuário para investigação e solução de problemas.")
    with right:
        st.markdown('<div class="section-label">Experiência</div>', unsafe_allow_html=True)
        timeline("jun/2025 · atual", "Monitor de Laboratório de TI — FIAP", "Suporte a alunos e docentes, diagnóstico de incidentes, imagens de sistema, rede e administração remota de salas.")
        timeline("mar/2025 · jun/2025", "Operador de Atendimento — Konecta", "Atendimento em ambiente orientado a resolução, satisfação do cliente e registro consistente em CRM.")
        timeline("2023 · 3 meses", "Intercâmbio autodirigido — Estados Unidos", "Planejamento e execução independente de uma experiência de imersão internacional aos 17 anos.")

    st.markdown('<div class="section-label">Projetos que colocaram conhecimento em prática</div>', unsafe_allow_html=True)
    projects = st.columns(3)
    with projects[0]:
        card("🏆", "FIAP Monitor", "Sistema de suporte a laboratórios com chat em tempo real e monitoramento remoto. 1º lugar no hackathon interno de estagiários.")
    with projects[1]:
        card("⌘", "Projetos acadêmicos", "Simulador bancário com DDD e sistema de apoio à decisão com grafos, BST, força bruta e algoritmo guloso.")
    with projects[2]:
        card("◆", "Open source", "Quatro pull requests aceitos no Yara, envolvendo segurança de senhas, acessibilidade e testes.")


def render_skills():
    page_header(
        "Competências",
        "Ferramentas para construir, analisar e comunicar.",
        "Um repertório em formação contínua, sustentado por projetos acadêmicos e experiência prática em TI.",
    )
    row_one = st.columns(3)
    with row_one[0]:
        skill_card("Linguagens", ["Python", "SQL", "Java", "JavaScript", "C++", "C#", "Rust"])
    with row_one[1]:
        skill_card("Dados e análise", ["Pandas", "Estatística descritiva", "Visualização", "Excel avançado", "LLMs"])
    with row_one[2]:
        skill_card("Cloud e infraestrutura", ["AWS", "Terraform", "Redes", "Imagens de sistema", "Edge Computing"])
    st.write("")
    row_two = st.columns(3)
    with row_two[0]:
        skill_card("Engenharia de software", ["Git", "GitHub", "DDD", "APIs", "HTML5", "CSS3", "Testes"])
    with row_two[1]:
        skill_card("Competências humanas", ["Comunicação técnica", "Autonomia", "Adaptabilidade", "Resolução de problemas", "Curiosidade"])
    with row_two[2]:
        skill_card("Idiomas", ["Português · nativo", "Inglês · fluente", "Espanhol · fluente", "Norueguês · básico", "Russo · básico"])

    st.markdown('<div class="section-label">Como essas competências se conectam</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="callout">
            <strong>Engenharia + dados + comunicação:</strong> minha experiência de suporte me ensinou a investigar sintomas,
            formular hipóteses e explicar soluções. Em projetos de dados, aplico o mesmo ciclo para preparar bases,
            validar resultados e apresentar evidências com clareza.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analysis(dataframe: pd.DataFrame | None):
    page_header(
        "Estudo de mercado",
        "Desempenho e eficiência de LLMs open-weight.",
        "Uma análise exploratória para apoiar a triagem de modelos quando qualidade, recursos computacionais e licença precisam ser avaliados em conjunto.",
    )
    st.markdown(
        """
        <div class="callout">
            <strong>Pergunta central:</strong> modelos menores conseguem entregar desempenho competitivo para projetos
            que precisam equilibrar qualidade e recursos computacionais?
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Usar outra base no mesmo formato"):
        uploaded_file = st.file_uploader("Envie um CSV padronizado", type="csv")
        if uploaded_file is not None:
            dataframe = load_data(uploaded_file)

    if dataframe is None:
        st.error("A base não foi encontrada. Inclua `data/llm_leaderboard.csv` no projeto.")
        return

    problems = validate_data(dataframe)
    if problems:
        st.error("A base não contém todas as colunas necessárias.")
        st.markdown("\n".join(f"- {problem}" for problem in problems))
        return

    prepared, quality = prepare_data(dataframe)
    with st.sidebar:
        st.markdown("### Filtros da análise")
        licenses = sorted(prepared["license"].unique())
        selected_licenses = st.multiselect("Licenças", licenses, default=licenses)
        max_parameters = float(prepared["parameters_b"].max())
        parameter_range = st.slider("Parâmetros (bilhões)", 0.0, max_parameters, (0.0, max_parameters), step=1.0)
        score_range = st.slider(
            "Score médio",
            float(prepared["average_score"].min()),
            float(prepared["average_score"].max()),
            (float(prepared["average_score"].min()), float(prepared["average_score"].max())),
        )
        logarithmic_scale = st.toggle("Escala logarítmica no porte", value=True)

    filtered = prepared[
        prepared["license"].isin(selected_licenses)
        & prepared["parameters_b"].between(*parameter_range)
        & prepared["average_score"].between(*score_range)
    ].copy()
    if filtered.empty:
        st.warning("Nenhum modelo atende aos filtros selecionados. Amplie os intervalos ou escolha mais licenças.")
        return

    mean_score = float(filtered["average_score"].mean())
    median_score = float(filtered["average_score"].median())
    standard_deviation = float(filtered["average_score"].std())
    correlation = float(filtered[["parameters_b", "average_score"]].corr().iloc[0, 1])
    best = filtered.loc[filtered["average_score"].idxmax()]

    metrics = st.columns(5)
    metrics[0].metric("Modelos", f"{len(filtered):,}".replace(",", "."))
    metrics[1].metric("Média", f"{mean_score:.2f}")
    metrics[2].metric("Mediana", f"{median_score:.2f}")
    metrics[3].metric("Desvio-padrão", f"{standard_deviation:.2f}" if pd.notna(standard_deviation) else "n/d")
    metrics[4].metric("Correlação", f"{correlation:.2f}" if pd.notna(correlation) else "n/d", correlation_label(correlation))
    st.caption(f"Maior score no recorte: {best['model_name']} · {best['average_score']:.2f} pontos")

    st.markdown('<div class="section-label">Porte do modelo e desempenho</div>', unsafe_allow_html=True)
    scatter = px.scatter(
        filtered,
        x="parameters_b",
        y="average_score",
        color="size_group",
        category_orders={"size_group": ["até 3B", "3–8B", "8–15B", "15–35B", "35–70B", "acima de 70B"]},
        color_discrete_sequence=["#60A5FA", "#2563EB", "#0891B2", "#7C3AED", "#DB2777", "#EA580C"],
        hover_name="model_name",
        hover_data={"organization": True, "license": True, "parameters_b": ":.2f", "average_score": ":.2f", "size_group": False},
        labels={"parameters_b": "Parâmetros (bilhões)", "average_score": "Score médio", "size_group": "Faixa de porte"},
        title="Relação entre número de parâmetros e score médio",
        opacity=0.72,
    )
    if logarithmic_scale:
        scatter.update_xaxes(type="log")
    st.plotly_chart(style_figure(scatter, 500), width="stretch", config={"displaylogo": False})
    st.caption("Cada ponto representa um modelo. A escala logarítmica facilita comparar modelos de portes muito diferentes.")

    left, right = st.columns(2, gap="large")
    with left:
        top_models = filtered.nlargest(10, "average_score").sort_values("average_score").copy()
        top_models["model_label"] = top_models["model_name"].str.split("/").str[-1].str.slice(0, 34)
        bar = px.bar(
            top_models,
            x="average_score",
            y="model_label",
            color="parameters_b",
            color_continuous_scale=["#BFDBFE", "#2563EB", "#312E81"],
            orientation="h",
            text_auto=".1f",
            title="Top 10 modelos por score",
            labels={"average_score": "Score médio", "model_label": "Modelo", "parameters_b": "Parâmetros (B)"},
            hover_data={"model_name": True, "license": True},
        )
        st.plotly_chart(style_figure(bar, 470), width="stretch", config={"displaylogo": False})
    with right:
        histogram = px.histogram(
            filtered,
            x="average_score",
            nbins=35,
            color_discrete_sequence=[COLORS["violet"]],
            title="Distribuição dos scores",
            labels={"average_score": "Score médio", "count": "Modelos"},
        )
        histogram.add_vline(x=mean_score, line_dash="dash", line_color=COLORS["blue"], annotation_text="média")
        histogram.add_vline(x=median_score, line_dash="dot", line_color=COLORS["green"], annotation_text="mediana")
        st.plotly_chart(style_figure(histogram, 470), width="stretch", config={"displaylogo": False})

    size_summary = (
        filtered.groupby("size_group", observed=True)
        .agg(modelos=("model_name", "count"), media=("average_score", "mean"), mediana=("average_score", "median"), melhor_score=("average_score", "max"))
        .reset_index()
    )
    size_chart = px.bar(
        size_summary,
        x="size_group",
        y="mediana",
        color="size_group",
        color_discrete_sequence=["#60A5FA", "#2563EB", "#0891B2", "#7C3AED", "#DB2777", "#EA580C"],
        text_auto=".1f",
        title="Mediana de desempenho por faixa de porte",
        labels={"size_group": "Faixa de porte", "mediana": "Score mediano"},
    )
    size_chart.update_layout(showlegend=False)
    st.plotly_chart(style_figure(size_chart, 420), width="stretch", config={"displaylogo": False})

    benchmark_columns = [column for column in filtered.columns if column.startswith("benchmark_")]
    if benchmark_columns:
        numeric_benchmarks = filtered[benchmark_columns].apply(pd.to_numeric, errors="coerce")
        correlation_matrix = numeric_benchmarks.corr()
        short_labels = [column.removeprefix("benchmark_").upper() for column in benchmark_columns]
        heatmap = px.imshow(
            correlation_matrix,
            x=short_labels,
            y=short_labels,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Correlação entre benchmarks",
        )
        st.plotly_chart(style_figure(heatmap, 500), width="stretch", config={"displaylogo": False})
        st.caption("A correlação mostra associação entre métricas, não causalidade nem qualidade em uma tarefa financeira específica.")

    compact = filtered[filtered["parameters_b"] <= 15]
    compact_best = compact.loc[compact["average_score"].idxmax()] if not compact.empty else None
    strongest_group = size_summary.loc[size_summary["mediana"].idxmax()]
    difference = mean_score - median_score
    st.markdown('<div class="section-label">Síntese orientada por evidências</div>', unsafe_allow_html=True)
    insights = [
        f"A faixa com maior mediana no recorte é {strongest_group['size_group']}, com {strongest_group['mediana']:.2f} pontos entre {int(strongest_group['modelos'])} modelos.",
        f"Média e mediana diferem {abs(difference):.2f} ponto(s), informação útil para avaliar assimetria e influência de valores extremos.",
    ]
    if pd.notna(correlation):
        insights.insert(
            0,
            f"A correlação de Pearson entre porte e score é {correlation:.2f}: associação {correlation_label(correlation)}. Isso sugere relação, mas não demonstra causalidade.",
        )
    if compact_best is not None:
        insights.append(
            f"Entre modelos de até 15B, o maior score é {compact_best['average_score']:.2f}, obtido por {compact_best['model_name']} ({compact_best['parameters_b']:.2f}B)."
        )
    for index, insight in enumerate(insights, start=1):
        st.markdown(
            f'<div class="insight"><div class="insight-number">EVIDÊNCIA {index:02d}</div><div class="insight-copy">{escape(insight)}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="callout">
            <strong>Conclusão aplicada:</strong> o leaderboard é adequado para triagem inicial, mas não basta para uma decisão
            no setor financeiro. Os candidatos selecionados ainda precisam de avaliação em tarefas do domínio, custo,
            latência, privacidade, segurança, licença e revisão humana.
        </div>
        """,
        unsafe_allow_html=True,
    )

    metadata = load_metadata()
    with st.expander("Metodologia, qualidade e limitações"):
        if metadata:
            st.markdown(
                f"**Fonte:** [{metadata['source_dataset']}]({metadata['source_url']})  \n"
                f"**Extração:** {metadata['extracted_at_utc']}  \n"
                f"**Registros brutos:** {metadata['raw_records']:,}  \n"
                f"**Registros normalizados:** {metadata['normalized_records']:,}"
            )
        st.markdown(
            f"**Registros válidos nesta análise:** {quality['valid_rows']:,}  \n"
            f"**Registros removidos por porte/score inválido:** {quality['removed_rows']:,}  \n"
            f"**Duplicidades exatas:** {quality['duplicates']}  \n"
            f"**Licenças distintas:** {quality['licenses']}"
        )
        st.markdown(
            "**Limitações:** benchmarks gerais não medem diretamente qualidade financeira; scores dependem do protocolo "
            "de avaliação; o número de parâmetros não representa sozinho custo real; e correlação não implica causalidade."
        )

    with st.expander("Explorar os dados filtrados"):
        visible_columns = [
            "model_name", "organization", "parameters_b", "average_score", "size_group", "license", "release_date", "co2_cost_kg", "model_type"
        ]
        visible_columns = [column for column in visible_columns if column in filtered.columns]
        st.dataframe(filtered[visible_columns].sort_values("average_score", ascending=False), width="stretch", hide_index=True)


def render_analysis_page():
    render_analysis(load_data())


st.sidebar.title("César Aaron")
st.sidebar.caption("Portfólio · Dados e IA")

navigation = st.navigation(
    [
        st.Page(render_profile, title="Quem sou eu", icon="👤", url_path="perfil", default=True),
        st.Page(render_qualifications, title="Qualificações", icon="🎓", url_path="qualificacoes"),
        st.Page(render_skills, title="Skills", icon="🧩", url_path="skills"),
        st.Page(render_analysis_page, title="Análise de Dados", icon="📊", url_path="analise-de-dados"),
    ],
    position="sidebar",
)
navigation.run()
