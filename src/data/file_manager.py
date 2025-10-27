"""
Lectura/escritura de JSON segura (placeholder)
"""
import json
import os
from typing import Any, Dict

ASSETS_CONFIG = os.path.join("assets", "config")
ASSETS_DATA = os.path.join("assets", "data")

os.makedirs(ASSETS_CONFIG, exist_ok=True)
os.makedirs(ASSETS_DATA, exist_ok=True)

LEVELS_FILE = os.path.join(ASSETS_CONFIG, "levels.json")
SCORES_FILE = os.path.join(ASSETS_DATA, "scores.json")


def load_json(path: str, default: Any):
    try:
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read().strip()
            return json.loads(txt) if txt else default
    except json.JSONDecodeError:
        return default


def save_json(path: str, data: Any) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False
