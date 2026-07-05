from __future__ import annotations

from datetime import date, datetime
from typing import Any

import pandas as pd


def make_json_serializable(value: Any) -> Any:
    """Converte objetos do Firestore/Pandas em estruturas compatíveis com JSON."""

    if value is None:
        return None

    if isinstance(value, dict):
        return {
            str(key): make_json_serializable(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [make_json_serializable(item) for item in value]

    if isinstance(value, tuple):
        return [make_json_serializable(item) for item in value]

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return None

        return value.isoformat()

    if pd.isna(value) if not isinstance(value, (list, dict, tuple)) else False:
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value
