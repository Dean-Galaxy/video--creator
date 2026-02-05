import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.config import Config
from src.utils import normalize_laugh, validate_asset_path


@dataclass(frozen=True)
class ScriptItem:
    item_id: int
    angle: str
    emotion: str
    text: str
    laugh: str


def load_script(filepath: Path, config: Config) -> List[ScriptItem]:
    with filepath.open("r", encoding="utf-8") as handle:
        raw_data = json.load(handle)

    if not isinstance(raw_data, list):
        raise ValueError("Script JSON must be a list of items.")

    script_items: List[ScriptItem] = []
    for raw_item in raw_data:
        item_id = int(raw_item.get("id"))
        angle = str(raw_item.get("angle"))
        emotion = str(raw_item.get("emotion"))
        text = str(raw_item.get("text"))
        laugh = normalize_laugh(raw_item.get("laugh", "不笑"))

        validate_asset_path(emotion, angle, config)
        script_items.append(
            ScriptItem(
                item_id=item_id,
                angle=angle,
                emotion=emotion,
                text=text,
                laugh=laugh,
            )
        )

    return script_items
