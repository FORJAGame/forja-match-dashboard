import streamlit as st

from src.data_loader import load_mock_sessions
from src.data_transform import normalize_answers, normalize_sessions
from src.metrics import calculate_completion_rate, get_peak_hour, get_top_game


st.title("Visão geral")
st.caption("Resumo dos dados coletados pelo FORJA Match.")

sessions = load_mock_sessions()
sessions_df = normalize_sessions(sessions)
answers_df = normalize_answers(sessions)

total_sessions = len(sessions_df)
completed_sessions = int(sessions_df["completed"].sum()) if not sessions_df.empty else 0
completion_rate = calculate_completion_rate(sessions_df)
total_answers = len(answers_df)
average_duration = sessions_df["duration_seconds"].mean() if not sessions_df.empty else 0
top_game = get_top_game(sessions_df)
peak_hour = get_peak_hour(sessions_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sessões totais",
    total_sessions,
    help="Quantidade de vezes em que a experiência foi iniciada no período analisado.",
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
    help="Quantidade total de respostas dadas aos cards.",
)

col5, col6, col7 = st.columns([1, 2, 1])

col5.metric(
    "Tempo médio",
    f"{average_duration:.0f}s",
    help="Tempo médio entre o início da sessão e a conclusão da experiência.",
)

col6.metric(
    "Jogo mais indicado",
    top_game,
    help="Jogo que mais apareceu como resultado final do match.",
)

col7.metric(
    "Horário de pico",
    peak_hour,
    help="Horário com maior quantidade de sessões iniciadas.",
)
