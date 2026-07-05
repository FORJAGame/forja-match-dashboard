from __future__ import annotations

import firebase_admin
import streamlit as st
from firebase_admin import credentials, firestore


@st.cache_resource
def get_firestore_client():
    if not firebase_admin._apps:
        service_account_info = dict(st.secrets["firebase_service_account"])
        credential = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(credential)

    return firestore.client()


def get_sessions_collection_name() -> str:
    return st.secrets.get("firestore", {}).get("collection_name", "sessions")
