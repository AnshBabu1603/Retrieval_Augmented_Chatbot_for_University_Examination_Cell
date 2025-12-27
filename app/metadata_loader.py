
import json
from pathlib import Path


def load_metadata(metadata_path: Path) -> dict:
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)

