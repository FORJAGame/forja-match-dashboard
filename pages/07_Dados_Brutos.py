import streamlit as st

from src.data_loader import load_mock_sessions


st.title("Dados brutos")
st.caption("Visualização inicial dos documentos simulados.")

sessions = load_mock_sessions()

st.json(sessions)
