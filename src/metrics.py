import pandas as pd


def calculate_completion_rate(sessions_df: pd.DataFrame) -> float:
    if sessions_df.empty:
        return 0.0

    total_sessions = len(sessions_df)

    if total_sessions == 0:
        return 0.0

    completed_sessions = sessions_df["completed"].sum()

    return completed_sessions / total_sessions


def get_top_game(sessions_df: pd.DataFrame) -> str:
    if sessions_df.empty or "result_game_name" not in sessions_df:
        return "Sem dados"

    valid_games = sessions_df["result_game_name"].dropna()

    if valid_games.empty:
        return "Sem dados"

    return valid_games.value_counts().index[0]


def get_peak_hour(sessions_df: pd.DataFrame) -> str:
    if sessions_df.empty or "hour" not in sessions_df:
        return "Sem dados"

    valid_hours = sessions_df["hour"].dropna()

    if valid_hours.empty:
        return "Sem dados"

    hour = int(valid_hours.value_counts().index[0])

    return f"{hour:02d}h"
