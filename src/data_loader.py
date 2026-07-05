from datetime import datetime, timedelta, timezone


def load_mock_sessions() -> list[dict]:
    base_time = datetime(2026, 7, 1, 14, 0, tzinfo=timezone.utc)

    return [
        {
            "id": "session_001",
            "kioskId": "totem_01",
            "startedAt": base_time.isoformat(),
            "finishedAt": (base_time + timedelta(seconds=58)).isoformat(),
            "completed": True,
            "answers": [
                {
                    "cardId": "card_01",
                    "cardText": "Gosto de jogos rápidos, intensos e cheios de ação.",
                    "direction": "right",
                    "answeredAt": (base_time + timedelta(seconds=10)).isoformat(),
                },
                {
                    "cardId": "card_02",
                    "cardText": "Gosto de experiências calmas e atmosféricas.",
                    "direction": "left",
                    "answeredAt": (base_time + timedelta(seconds=20)).isoformat(),
                },
            ],
            "result": {
                "gameId": "punch-throw-score",
                "gameName": "Punch! Throw!! Score!!!",
                "score": 42,
                "ranking": [
                    {
                        "gameId": "punch-throw-score",
                        "gameName": "Punch! Throw!! Score!!!",
                        "score": 42,
                    },
                    {
                        "gameId": "beyond-the-train",
                        "gameName": "Beyond the Train",
                        "score": 31,
                    },
                ],
            },
            "appVersion": "mvp-1",
            "updatedAt": (base_time + timedelta(seconds=65)).isoformat(),
        },
        {
            "id": "session_002",
            "kioskId": "totem_02",
            "startedAt": (base_time + timedelta(hours=1)).isoformat(),
            "finishedAt": (base_time + timedelta(hours=1, seconds=75)).isoformat(),
            "completed": True,
            "answers": [
                {
                    "cardId": "card_03",
                    "cardText": "Curto jogos com história e mundo para explorar.",
                    "direction": "right",
                    "answeredAt": (base_time + timedelta(hours=1, seconds=12)).isoformat(),
                }
            ],
            "result": {
                "gameId": "beyond-the-train",
                "gameName": "Beyond the Train",
                "score": 38,
                "ranking": [
                    {
                        "gameId": "beyond-the-train",
                        "gameName": "Beyond the Train",
                        "score": 38,
                    },
                    {
                        "gameId": "ismalia",
                        "gameName": "Ismália",
                        "score": 29,
                    },
                ],
            },
            "appVersion": "mvp-1",
            "updatedAt": (base_time + timedelta(hours=1, seconds=80)).isoformat(),
        },
    ]
