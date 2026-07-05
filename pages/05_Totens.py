import plotly.express as px
import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions
from src.filters import apply_sidebar_filters, filter_related_data


st.title("Totens")
st.caption("Análise de uso por totem ou dispositivo.")

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

if filtered_sessions_df.empty:
    st.warning("Nenhuma sessão encontrada para os filtros selecionados.")
    st.stop()

kiosk_summary = (
    filtered_sessions_df.groupby("kiosk_id", dropna=False)
    .agg(
        sessoes=("session_id", "count"),
        concluidas=("completed", "sum"),
        tempo_medio=("duration_seconds", "mean"),
        respostas_medias=("answers_count", "mean"),
    )
    .reset_index()
)

kiosk_summary["kiosk_id"] = kiosk_summary["kiosk_id"].fillna("Sem identificação")
kiosk_summary["abandonadas"] = kiosk_summary["sessoes"] - kiosk_summary["concluidas"]
kiosk_summary["taxa_conclusao"] = kiosk_summary["concluidas"] / kiosk_summary["sessoes"]

st.subheader("Sessões por totem")
st.caption(
    "Mostra quais totens foram mais utilizados. "
    "Pode indicar diferença de fluxo, posicionamento ou visibilidade no evento."
)

fig_sessions = px.bar(
    kiosk_summary.sort_values("sessoes"),
    x="sessoes",
    y="kiosk_id",
    orientation="h",
    text="sessoes",
)

fig_sessions.update_layout(
    xaxis_title="Sessões",
    yaxis_title="Totem",
)

st.plotly_chart(fig_sessions, use_container_width=True)

st.subheader("Taxa de conclusão por totem")
st.caption(
    "Ajuda a identificar se algum totem teve mais abandono que os demais."
)

fig_completion = px.bar(
    kiosk_summary.sort_values("taxa_conclusao"),
    x="taxa_conclusao",
    y="kiosk_id",
    orientation="h",
    text=kiosk_summary["taxa_conclusao"].map(lambda value: f"{value:.0%}"),
)

fig_completion.update_xaxes(tickformat=".0%")
fig_completion.update_layout(
    xaxis_title="Taxa de conclusão",
    yaxis_title="Totem",
)

st.plotly_chart(fig_completion, use_container_width=True)

st.subheader("Jogos mais indicados por totem")
st.caption(
    "Mostra a distribuição dos jogos indicados em cada totem. "
    "Pode ajudar a perceber diferenças de público ou posicionamento físico."
)

matches_by_kiosk = (
    filtered_sessions_df.dropna(subset=["result_game_name"])
    .groupby(["kiosk_id", "result_game_name"])
    .size()
    .reset_index(name="matches")
)

if matches_by_kiosk.empty:
    st.info("Não há dados de jogos indicados para os filtros selecionados.")
else:
    fig_games = px.bar(
        matches_by_kiosk,
        x="kiosk_id",
        y="matches",
        color="result_game_name",
        barmode="group",
    )

    fig_games.update_layout(
        xaxis_title="Totem",
        yaxis_title="Matches",
        legend_title="Jogo",
    )

    st.plotly_chart(fig_games, use_container_width=True)

st.subheader("Tabela por totem")
st.dataframe(kiosk_summary, use_container_width=True)
