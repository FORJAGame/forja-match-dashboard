from __future__ import annotations

import pandas as pd


def parse_datetime(value):
    if not value:
        return pd.NaT

    return pd.to_datetime(value, errors="coerce", utc=True)


def normalize_sessions(sessions: list[dict]) -> pd.DataFrame:
    rows = []

    for session in sessions:
        started_at = parse_datetime(session.get("startedAt"))
        finished_at = parse_datetime(session.get("finishedAt"))

        duration_seconds = None
        if pd.notna(started_at) and pd.notna(finished_at):
            duration_seconds = (finished_at - started_at).total_seconds()

        result = session.get("result") or {}

        rows.append(
            {
                "session_id": session.get("id"),
                "kiosk_id": session.get("kioskId"),
                "event_id": session.get("eventId"),
                "event_name": session.get("eventName"),
                "started_at": started_at,
                "finished_at": finished_at,
                "completed": bool(session.get("completed")),
                "duration_seconds": duration_seconds,
                "answers_count": len(session.get("answers") or []),
                "result_game_id": result.get("gameId"),
                "result_game_name": result.get("gameName"),
                "result_score": result.get("score"),
                "app_version": session.get("appVersion"),
                "updated_at": parse_datetime(session.get("updatedAt")),
            }
        )

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df["date"] = df["started_at"].dt.date
    df["hour"] = df["started_at"].dt.hour
    df["weekday"] = df["started_at"].dt.day_name()

    return df


def normalize_answers(sessions: list[dict]) -> pd.DataFrame:
    rows = []

    for session in sessions:
        result = session.get("result") or {}

        for answer in session.get("answers") or []:
            direction = answer.get("direction")

            rows.append(
                {
                    "session_id": session.get("id"),
                    "kiosk_id": session.get("kioskId"),
                    "event_id": session.get("eventId"),
                    "card_id": answer.get("cardId"),
                    "card_text": answer.get("cardText"),
                    "direction": direction,
                    "accepted": direction == "right",
                    "answered_at": parse_datetime(answer.get("answeredAt")),
                    "result_game_id": result.get("gameId"),
                    "result_game_name": result.get("gameName"),
                }
            )

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df["date"] = df["answered_at"].dt.date
    df["hour"] = df["answered_at"].dt.hour

    return df


def normalize_ranking(sessions: list[dict]) -> pd.DataFrame:
    rows = []

    for session in sessions:
        result = session.get("result") or {}
        ranking = result.get("ranking") or []

        for index, game in enumerate(ranking, start=1):
            rows.append(
                {
                    "session_id": session.get("id"),
                    "kiosk_id": session.get("kioskId"),
                    "event_id": session.get("eventId"),
                    "game_id": game.get("gameId"),
                    "game_name": game.get("gameName"),
                    "score": game.get("score"),
                    "rank_position": index,
                    "is_winner": index == 1,
                }
            )

    return pd.DataFrame(rows)
