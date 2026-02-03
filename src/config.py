import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _resolve_optional_path(base_dir: Path, raw_value: str) -> Path | None:
    value = raw_value.strip()
    if not value:
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    return candidate


@dataclass(frozen=True)
class Config:
    base_dir: Path
    fish_api_key: str
    fish_reference_id: str
    assets_dir: Path
    output_dir: Path
    temp_dir: Path
    intro_music_path: Path | None
    outro_music_path: Path | None

    @classmethod
    def load(cls, base_dir: Path | None = None) -> "Config":
        load_dotenv()
        resolved_base = base_dir or Path.cwd()
        api_key = os.environ.get("FISH_API_KEY", "").strip()
        reference_id = os.environ.get("FISH_REFERENCE_ID", "").strip()
        intro_music = _resolve_optional_path(
            resolved_base, os.environ.get("INTRO_MUSIC_PATH", "")
        )
        outro_music = _resolve_optional_path(
            resolved_base, os.environ.get("OUTRO_MUSIC_PATH", "")
        )
        return cls(
            base_dir=resolved_base,
            fish_api_key=api_key,
            fish_reference_id=reference_id,
            assets_dir=resolved_base / "assets",
            output_dir=resolved_base / "output",
            temp_dir=resolved_base / "temp",
            intro_music_path=intro_music,
            outro_music_path=outro_music,
        )

    def validate(self) -> None:
        if not self.fish_api_key:
            raise ValueError("Missing FISH_API_KEY in environment.")
        if not self.fish_reference_id:
            raise ValueError("Missing FISH_REFERENCE_ID in environment.")
        if self.intro_music_path and not self.intro_music_path.exists():
            raise FileNotFoundError(f"Missing intro music: {self.intro_music_path}")
        if self.outro_music_path and not self.outro_music_path.exists():
            raise FileNotFoundError(f"Missing outro music: {self.outro_music_path}")

    @property
    def ASSETS_DIR(self) -> Path:
        return self.assets_dir

    @property
    def OUTPUT_DIR(self) -> Path:
        return self.output_dir

    @property
    def TEMP_DIR(self) -> Path:
        return self.temp_dir
