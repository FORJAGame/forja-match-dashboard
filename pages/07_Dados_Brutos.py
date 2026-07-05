import json

import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_answers, normalize_ranking, normalize_sessions
from src.filters import apply_sidebar_filters, filter_related_data
from src.utils import make_json_serializable


st.title("Dados brutos")
st.caption(
    "Inspeção dos documentos originais e das tabelas normalizadas. "
    "Use esta página para investigar problemas ou conferir campos específicos."
)

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

valid_session_ids = set(filtered_sessions_df["session_id"].dropna())

filtered_raw_sessions = [
    session for session in sessions if session.get("id") in valid_session_ids
]

tab_raw, tab_sessions, tab_answers, tab_ranking = st.tabs(
    ["JSON bruto", "Sessões", "Respostas", "Ranking"]
)

with tab_raw:
    st.subheader("Documentos brutos")
    st.caption(
        "Mostra o documento original salvo no Firestore. "
        "Datas do Firestore são convertidas para texto no formato ISO."
    )

    if not filtered_raw_sessions:
        st.info("Nenhum documento bruto encontrado para os filtros selecionados.")
        st.stop()

    selected_session_id = st.selectbox(
        "Selecione uma sessão",
        [session.get("id") for session in filtered_raw_sessions],
    )

    selected_session = next(
        session
        for session in filtered_raw_sessions
        if session.get("id") == selected_session_id
    )

    serializable_session = make_json_serializable(selected_session)

    st.json(serializable_session)

    raw_json = json.dumps(
        serializable_session,
        ensure_ascii=False,
        indent=2,
    )

    st.download_button(
        "Baixar JSON desta sessão",
        data=raw_json,
        file_name=f"{selected_session_id}.json",
        mime="application/json",
    )

with tab_sessions:
    st.subheader("DataFrame de sessões")
    st.caption(
        "Tabela normalizada com uma linha por sessão. "
        "É a base principal para filtros, métricas e análises gerais."
    )

    st.dataframe(
        filtered_sessions_df,
        use_container_width=True,
        hide_index=True,
    )

with tab_answers:
    st.subheader("DataFrame de respostas")
    st.caption(
        "Tabela normalizada com uma linha por resposta dada aos cards."
    )

    if filtered_answers_df.empty:
        st.info("Nenhuma resposta encontrada para os filtros selecionados.")
    else:
        st.dataframe(
            filtered_answers_df,
            use_container_width=True,
            hide_index=True,
        )

with tab_ranking:
    st.subheader("DataFrame de ranking")
    st.caption(
        "Tabela normalizada com uma linha para cada jogo no ranking de cada sessão."
    )

    if filtered_ranking_df.empty:
        st.info("Nenhum ranking encontrado para os filtros selecionados.")
    else:
        st.dataframe(
            filtered_ranking_df,
            use_container_width=True,
            hide_index=True,
        )
