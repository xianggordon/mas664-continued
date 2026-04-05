import json
import uuid
from datetime import datetime
from pathlib import Path

STORAGE_PATH = Path("rubrics.json")


def _load() -> dict:
    if not STORAGE_PATH.exists():
        return {}
    with open(STORAGE_PATH, "r") as f:
        return json.load(f)


def _save(data: dict):
    with open(STORAGE_PATH, "w") as f:
        json.dump(data, f, indent=2)


def save_rubric(name: str, rubric: list[dict]) -> dict:
    data = _load()
    rubric_id = str(uuid.uuid4())
    record = {
        "id": rubric_id,
        "name": name,
        "rubric": rubric,
        "created_at": datetime.utcnow().isoformat(),
    }
    data[rubric_id] = record
    _save(data)
    return record


def list_rubrics() -> list[dict]:
    data = _load()
    return sorted(data.values(), key=lambda r: r["created_at"])


def get_rubric(rubric_id: str) -> dict | None:
    data = _load()
    return data.get(rubric_id)


def delete_rubric(rubric_id: str) -> bool:
    data = _load()
    if rubric_id not in data:
        return False
    del data[rubric_id]
    _save(data)
    return True
