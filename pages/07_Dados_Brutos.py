import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions


st.title("Dados brutos")
st.caption("Visualização dos dados simulados e normalizados.")

sessions = load_firestore_sessions()

sessions_df = normalize_sessions(sessions)
answers_df = normalize_answers(sessions)
ranking_df = normalize_ranking(sessions)

tab_raw, tab_sessions, tab_answers, tab_ranking = st.tabs(
    ["JSON bruto", "Sessões", "Respostas", "Ranking"]
)

with tab_raw:
    st.json(sessions)

with tab_sessions:
    st.dataframe(sessions_df, use_container_width=True)

with tab_answers:
    st.dataframe(answers_df, use_container_width=True)

with tab_ranking:
    st.dataframe(ranking_df, use_container_width=True)
