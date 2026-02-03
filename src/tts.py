from pathlib import Path
from typing import Dict, Iterable

import requests

from src.config import Config
from src.parser import ScriptItem


class FishAudioError(RuntimeError):
    pass


EMOTION_TAG_MAP = {
    "开心": "happy",
    "伤心": "sad",
    "愤怒": "angry",
    "平静": "calm",
    "嘲讽": "angry",
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "calm": "calm",
}


def apply_emotion_tag(text: str, emotion: str) -> str:
    if text.lstrip().startswith("("):
        return text
    tag = EMOTION_TAG_MAP.get(str(emotion).strip(), "calm")
    return f"({tag}) {text}"


def generate_audio(
    text: str, output_path: Path, config: Config, emotion: str = "calm"
) -> Path:
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {config.fish_api_key}",
        "Content-Type": "application/json",
        "model": "s1",
    }
    tagged_text = apply_emotion_tag(text, emotion)
    payload = {
        "text": tagged_text,
        "reference_id": config.fish_reference_id,
        "format": "mp3",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    if response.status_code != 200:
        raise FishAudioError(f"Fish Audio error {response.status_code}: {response.text}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    return output_path


def batch_process_audio(
    script_data: Iterable[ScriptItem], config: Config
) -> Dict[int, Path]:
    audio_map: Dict[int, Path] = {}
    for item in script_data:
        output_path = config.temp_dir / f"{item.item_id}_audio.mp3"
        if not output_path.exists():
            generate_audio(item.text, output_path, config, item.emotion)
        audio_map[item.item_id] = output_path
    return audio_map
