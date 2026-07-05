import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions
from src.filters import apply_sidebar_filters, filter_related_data


st.title("Sessões")
st.caption("Consulta detalhada das sessões registradas pelo FORJA Match.")

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

search = st.text_input(
    "Buscar por ID da sessão",
    placeholder="Digite parte do session_id",
    help="Permite localizar uma sessão específica pelo identificador.",
)

display_df = filtered_sessions_df.copy()

if search:
    display_df = display_df[
        display_df["session_id"].astype(str).str.contains(search, case=False, na=False)
    ]

st.subheader("Tabela de sessões")
st.caption("Tabela com as principais informações de cada sessão filtrada.")

columns_to_show = [
    "session_id",
    "kiosk_id",
    "event_id",
    "started_at",
    "finished_at",
    "completed",
    "duration_seconds",
    "answers_count",
    "result_game_name",
    "result_score",
    "app_version",
    "updated_at",
]

existing_columns = [column for column in columns_to_show if column in display_df.columns]

st.dataframe(
    display_df[existing_columns],
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("Inspecionar sessão")

selected_session_id = st.selectbox(
    "Selecione uma sessão",
    display_df["session_id"].dropna().tolist(),
    help="Mostra respostas e ranking da sessão selecionada.",
)

selected_answers = filtered_answers_df[
    filtered_answers_df["session_id"] == selected_session_id
]

selected_ranking = filtered_ranking_df[
    filtered_ranking_df["session_id"] == selected_session_id
]

tab_answers, tab_ranking = st.tabs(["Respostas", "Ranking"])

with tab_answers:
    if selected_answers.empty:
        st.info("Esta sessão não possui respostas registradas.")
    else:
        st.dataframe(selected_answers, use_container_width=True, hide_index=True)

with tab_ranking:
    if selected_ranking.empty:
        st.info("Esta sessão não possui ranking registrado.")
    else:
        st.dataframe(selected_ranking, use_container_width=True, hide_index=True)
