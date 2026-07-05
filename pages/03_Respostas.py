import plotly.express as px
import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions
from src.filters import apply_sidebar_filters, filter_related_data


st.title("Respostas")
st.caption("Análise de aceitação e rejeição dos cards do FORJA Match.")

sessions = load_firestore_sessions()

sessions_df = normalize_sessions(sessions)
answers_df = normalize_answers(sessions)
ranking_df = normalize_ranking(sessions)

filtered_sessions_df = apply_sidebar_filters(sessions_df)

filtered_answers_df, filtered_ranking_df = filter_related_data(
    filtered_sessions_df,
    answers_df,
    ranking_df,
)

if filtered_answers_df.empty:
    st.warning("Nenhuma resposta encontrada para os filtros selecionados.")
    st.stop()

total_answers = len(filtered_answers_df)
accepted_answers = int(filtered_answers_df["accepted"].sum())
rejected_answers = total_answers - accepted_answers
acceptance_rate = accepted_answers / total_answers if total_answers else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "Respostas totais",
    total_answers,
    help="Quantidade total de respostas dadas aos cards no recorte filtrado.",
)

col2.metric(
    "Aceitações",
    accepted_answers,
    help="Quantidade de respostas em que o visitante indicou que a frase combinava com ele.",
)

col3.metric(
    "Taxa de aceitação",
    f"{acceptance_rate:.1%}",
    help="Percentual de respostas positivas em relação ao total de respostas.",
)

card_summary = (
    filtered_answers_df.groupby(["card_id", "card_text"], dropna=False)
    .agg(
        total_respostas=("direction", "count"),
        aceites=("accepted", "sum"),
    )
    .reset_index()
)

card_summary["rejeicoes"] = (
    card_summary["total_respostas"] - card_summary["aceites"]
)

card_summary["taxa_aceitacao"] = (
    card_summary["aceites"] / card_summary["total_respostas"]
)

card_summary["taxa_rejeicao"] = 1 - card_summary["taxa_aceitacao"]

st.divider()

st.subheader("Cards mais aceitos")
st.caption(
    "Mostra as frases que mais receberam respostas positivas. "
    "Esses cards indicam preferências fortes do público filtrado."
)

most_accepted = card_summary.sort_values(
    ["taxa_aceitacao", "total_respostas"],
    ascending=[False, False],
)

fig_acceptance = px.bar(
    most_accepted,
    x="taxa_aceitacao",
    y="card_text",
    orientation="h",
    text=most_accepted["taxa_aceitacao"].map(lambda value: f"{value:.0%}"),
)

fig_acceptance.update_xaxes(tickformat=".0%")
fig_acceptance.update_layout(
    xaxis_title="Taxa de aceitação",
    yaxis_title="Card",
    yaxis={"categoryorder": "total ascending"},
)

st.plotly_chart(fig_acceptance, use_container_width=True)

st.subheader("Cards mais rejeitados")
st.caption(
    "Mostra as frases que mais receberam respostas negativas. "
    "Esses cards indicam preferências com menor aderência ao público filtrado."
)

most_rejected = card_summary.sort_values(
    ["taxa_rejeicao", "total_respostas"],
    ascending=[False, False],
)

fig_rejection = px.bar(
    most_rejected,
    x="taxa_rejeicao",
    y="card_text",
    orientation="h",
    text=most_rejected["taxa_rejeicao"].map(lambda value: f"{value:.0%}"),
)

fig_rejection.update_xaxes(tickformat=".0%")
fig_rejection.update_layout(
    xaxis_title="Taxa de rejeição",
    yaxis_title="Card",
    yaxis={"categoryorder": "total ascending"},
)

st.plotly_chart(fig_rejection, use_container_width=True)

st.subheader("Tabela detalhada")
st.caption("Tabela com o desempenho de cada card no recorte filtrado.")

st.dataframe(
    card_summary.sort_values("total_respostas", ascending=False),
    use_container_width=True,
)
