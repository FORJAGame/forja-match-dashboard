import plotly.express as px
import streamlit as st

from src.data_loader import load_firestore_sessions
from src.data_transform import normalize_sessions
from src.filters import apply_sidebar_filters


st.title("Jogos")
st.caption("Análise dos jogos mais indicados pelo FORJA Match.")

sessions = load_firestore_sessions()
sessions_df = normalize_sessions(sessions)
filtered_df = apply_sidebar_filters(sessions_df)

if filtered_df.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

ranking = (
    filtered_df["result_game_name"]
    .dropna()
    .value_counts()
    .reset_index()
)

ranking.columns = ["Jogo", "Matches"]

st.subheader("Ranking de jogos mais indicados")
st.caption("Mostra quais jogos apareceram mais vezes como resultado final.")

fig = px.bar(
    ranking,
    x="Matches",
    y="Jogo",
    orientation="h",
    text="Matches",
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

st.dataframe(ranking, use_container_width=True)
