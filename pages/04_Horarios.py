import plotly.express as px
import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions
from src.filters import apply_sidebar_filters, filter_related_data


st.title("Horários")
st.caption("Análise dos períodos de maior atividade no FORJA Match.")

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

sessions_by_hour = (
    filtered_sessions_df.groupby("hour", dropna=False)
    .agg(
        sessoes=("session_id", "count"),
        concluidas=("completed", "sum"),
        tempo_medio=("duration_seconds", "mean"),
    )
    .reset_index()
    .dropna(subset=["hour"])
)

sessions_by_hour["hour"] = sessions_by_hour["hour"].astype(int)
sessions_by_hour["hora"] = sessions_by_hour["hour"].map(lambda value: f"{value:02d}h")
sessions_by_hour["taxa_conclusao"] = (
    sessions_by_hour["concluidas"] / sessions_by_hour["sessoes"]
)

answers_by_hour = (
    filtered_answers_df.groupby("hour", dropna=False)
    .agg(respostas=("session_id", "count"))
    .reset_index()
    .dropna(subset=["hour"])
)

if not answers_by_hour.empty:
    answers_by_hour["hour"] = answers_by_hour["hour"].astype(int)
    answers_by_hour["hora"] = answers_by_hour["hour"].map(lambda value: f"{value:02d}h")

st.subheader("Sessões por horário")
st.caption(
    "Mostra em quais horários mais pessoas iniciaram a experiência. "
    "Ajuda a identificar períodos de maior movimento no evento."
)

fig_sessions = px.line(
    sessions_by_hour.sort_values("hour"),
    x="hora",
    y="sessoes",
    markers=True,
)

fig_sessions.update_layout(
    xaxis_title="Horário",
    yaxis_title="Sessões iniciadas",
)

st.plotly_chart(fig_sessions, use_container_width=True)

st.subheader("Taxa de conclusão por horário")
st.caption(
    "Mostra se as pessoas estavam concluindo a experiência em cada faixa horária."
)

fig_completion = px.bar(
    sessions_by_hour.sort_values("hour"),
    x="hora",
    y="taxa_conclusao",
    text=sessions_by_hour["taxa_conclusao"].map(lambda value: f"{value:.0%}"),
)

fig_completion.update_yaxes(tickformat=".0%")
fig_completion.update_layout(
    xaxis_title="Horário",
    yaxis_title="Taxa de conclusão",
)

st.plotly_chart(fig_completion, use_container_width=True)

if not answers_by_hour.empty:
    st.subheader("Respostas por horário")
    st.caption(
        "Mostra em quais horários os visitantes mais interagiram com os cards."
    )

    fig_answers = px.bar(
        answers_by_hour.sort_values("hour"),
        x="hora",
        y="respostas",
        text="respostas",
    )

    fig_answers.update_layout(
        xaxis_title="Horário",
        yaxis_title="Respostas",
    )

    st.plotly_chart(fig_answers, use_container_width=True)

st.subheader("Tabela por horário")
st.dataframe(
    sessions_by_hour.sort_values("hour"),
    use_container_width=True,
)
