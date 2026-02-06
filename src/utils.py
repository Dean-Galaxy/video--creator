from pathlib import Path

from src.config import Config

EMOTION_NAMES = {"愤怒", "嘲讽", "平静", "伤心", "开心", "震惊", "害怕", "动作"}
ANGLE_NAMES = {"全景", "远景", "中景", "近景", "特写", "留白", "右中景", "左远景"}
LAUGH_NAMES = {"不笑", "小笑", "大笑", "爆笑"}


def normalize_emotion(emotion: str) -> str:
    value = str(emotion).strip()
    if value not in EMOTION_NAMES:
        allowed = "、".join(sorted(EMOTION_NAMES))
        raise ValueError(f"Unknown emotion: {value}. Allowed: {allowed}")
    return value


def normalize_angle(angle: str) -> str:
    value = str(angle).strip()
    if value not in ANGLE_NAMES:
        allowed = "、".join(sorted(ANGLE_NAMES))
        raise ValueError(f"Unknown angle: {value}. Allowed: {allowed}")
    return value


def normalize_laugh(laugh: str) -> str:
    value = str(laugh).strip()
    if value not in LAUGH_NAMES:
        allowed = "、".join(sorted(LAUGH_NAMES))
        raise ValueError(f"Unknown laugh type: {value}. Allowed: {allowed}")
    return value


def resolve_laugh_audio_path(laugh: str, config: Config) -> Path | None:
    value = normalize_laugh(laugh)
    if value == "不笑":
        return None
    return config.laugh_dir / f"{value}.mp3"


def resolve_laugh_video_path(laugh: str, angle: str, config: Config) -> Path | None:
    value = normalize_laugh(laugh)
    if value == "不笑":
        return None
    angle_value = normalize_angle(angle)
    asset_dir = config.assets_dir / value
    candidates = sorted(asset_dir.glob(f"{angle_value}.*"))
    if not candidates:
        expected = asset_dir / f"{angle_value}.*"
        raise FileNotFoundError(f"Missing laugh video: {expected}")
    return candidates[0]


def validate_asset_path(emotion: str, angle: str, config: Config) -> Path:
    normalized_emotion = normalize_emotion(emotion)
    if normalized_emotion == "动作":
        normalized_angle = str(angle).strip()
    else:
        normalized_angle = normalize_angle(angle)
    asset_dir = config.assets_dir / normalized_emotion
    candidates = sorted(asset_dir.glob(f"{normalized_angle}.*"))
    if not candidates:
        expected = asset_dir / f"{normalized_angle}.*"
        raise FileNotFoundError(f"Missing asset: {expected}")
    return candidates[0]


def cleanup_temp(config: Config) -> None:
    if not config.temp_dir.exists():
        return
    for item in config.temp_dir.iterdir():
        if item.is_file():
            item.unlink()
