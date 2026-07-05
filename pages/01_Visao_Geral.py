import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions
from src.filters import apply_sidebar_filters, filter_related_data
from src.metrics import calculate_completion_rate, get_peak_hour, get_top_game

st.title("Visão geral")
st.caption("Resumo dos dados coletados pelo FORJA Match.")

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
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

total_sessions = len(filtered_sessions_df)
completed_sessions = int(filtered_sessions_df["completed"].sum())
completion_rate = calculate_completion_rate(filtered_sessions_df)
total_answers = len(filtered_answers_df)
average_duration = filtered_sessions_df["duration_seconds"].mean()
top_game = get_top_game(filtered_sessions_df)
peak_hour = get_peak_hour(filtered_sessions_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sessões totais",
    total_sessions,
    help="Quantidade de vezes em que a experiência foi iniciada no período filtrado.",
)

col2.metric(
    "Sessões concluídas",
    completed_sessions,
    help="Sessões em que o visitante chegou até a tela final de resultado.",
)

col3.metric(
    "Taxa de conclusão",
    f"{completion_rate:.1%}",
    help="Percentual de sessões finalizadas em relação ao total de sessões iniciadas.",
)

col4.metric(
    "Respostas",
    total_answers,
    help="Quantidade total de respostas dadas aos cards no período filtrado.",
)

col5, col6, col7 = st.columns([1, 2, 3])

col5.metric(
    "Tempo médio",
    f"{average_duration:.0f}s",
    help="Tempo médio entre o início da sessão e a conclusão da experiência.",
)

col6.metric(
    "Jogo mais indicado",
    top_game,
    help="Jogo que mais apareceu como resultado final do match no período filtrado.",
)

col7.metric(
    "Horário de pico",
    peak_hour,
    help="Horário com maior quantidade de sessões iniciadas.",
)
