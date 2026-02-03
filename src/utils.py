from pathlib import Path

from src.config import Config

EMOTION_NAMES = {"愤怒", "嘲讽", "平静", "伤心", "开心"}
ANGLE_NAMES = {"全景", "远景", "中景", "近景", "特写", "留白", "右中景", "左远景"}


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


def validate_asset_path(emotion: str, angle: str, config: Config) -> Path:
    normalized_emotion = normalize_emotion(emotion)
    normalized_angle = normalize_angle(angle)
    asset_path = config.assets_dir / normalized_emotion / f"{normalized_angle}.mp4"
    if not asset_path.exists():
        raise FileNotFoundError(f"Missing asset: {asset_path}")
    return asset_path


def cleanup_temp(config: Config) -> None:
    if not config.temp_dir.exists():
        return
    for item in config.temp_dir.iterdir():
        if item.is_file():
            item.unlink()
