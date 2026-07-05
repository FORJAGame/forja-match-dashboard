import pandas as pd
import streamlit as st


def apply_sidebar_filters(sessions_df: pd.DataFrame) -> pd.DataFrame:
    """Aplica filtros globais sobre o DataFrame de sessões."""

    if sessions_df.empty:
        st.sidebar.info("Nenhum dado disponível para filtrar.")
        return sessions_df

    st.sidebar.header("Filtros")

    filtered_df = sessions_df.copy()

    if "date" in filtered_df.columns:
        available_dates = sorted(filtered_df["date"].dropna().unique())

        if available_dates:
            selected_range = st.sidebar.date_input(
                "Intervalo de datas",
                value=(available_dates[0], available_dates[-1]),
                help="Filtra as sessões pela data de início.",
            )

            if isinstance(selected_range, tuple) and len(selected_range) == 2:
                start_date, end_date = selected_range

                filtered_df = filtered_df[
                    (filtered_df["date"] >= start_date)
                    & (filtered_df["date"] <= end_date)
                ]

    if "kiosk_id" in filtered_df.columns:
        kiosks = sorted(filtered_df["kiosk_id"].dropna().unique())

        selected_kiosks = st.sidebar.multiselect(
            "Totens",
            kiosks,
            default=kiosks,
            help="Filtra os dados por totem.",
        )

        if selected_kiosks:
            filtered_df = filtered_df[filtered_df["kiosk_id"].isin(selected_kiosks)]
        else:
            return filtered_df.iloc[0:0]

    if "result_game_name" in filtered_df.columns:
        games = sorted(filtered_df["result_game_name"].dropna().unique())

        selected_games = st.sidebar.multiselect(
            "Jogos indicados",
            games,
            default=games,
            help="Filtra as sessões pelo jogo que apareceu como resultado final.",
        )

        if selected_games:
            filtered_df = filtered_df[
                filtered_df["result_game_name"].isin(selected_games)
            ]
        else:
            return filtered_df.iloc[0:0]

    completion_options = {
        "Todas": None,
        "Concluídas": True,
        "Abandonadas": False,
    }

    selected_completion = st.sidebar.radio(
        "Status da sessão",
        list(completion_options.keys()),
        help="Permite visualizar apenas sessões concluídas ou abandonadas.",
    )

    selected_value = completion_options[selected_completion]

    if selected_value is not None:
        filtered_df = filtered_df[filtered_df["completed"] == selected_value]

    st.sidebar.caption(f"{len(filtered_df)} sessões encontradas.")

    return filtered_df


def filter_related_data(
    filtered_sessions_df: pd.DataFrame,
    answers_df: pd.DataFrame,
    ranking_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filtra respostas e rankings usando as sessões filtradas."""

    if filtered_sessions_df.empty:
        return answers_df.iloc[0:0], ranking_df.iloc[0:0]

    valid_session_ids = set(filtered_sessions_df["session_id"].dropna())

    filtered_answers_df = answers_df[
        answers_df["session_id"].isin(valid_session_ids)
    ]

    filtered_ranking_df = ranking_df[
        ranking_df["session_id"].isin(valid_session_ids)
    ]

    return filtered_answers_df, filtered_ranking_df
