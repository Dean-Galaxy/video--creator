import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    base_dir: Path
    fish_api_key: str
    fish_reference_id: str
    assets_dir: Path
    output_dir: Path
    temp_dir: Path

    @classmethod
    def load(cls, base_dir: Path | None = None) -> "Config":
        load_dotenv()
        resolved_base = base_dir or Path.cwd()
        api_key = os.environ.get("FISH_API_KEY", "").strip()
        reference_id = os.environ.get("FISH_REFERENCE_ID", "").strip()
        return cls(
            base_dir=resolved_base,
            fish_api_key=api_key,
            fish_reference_id=reference_id,
            assets_dir=resolved_base / "assets",
            output_dir=resolved_base / "output",
            temp_dir=resolved_base / "temp",
        )

    def validate(self) -> None:
        if not self.fish_api_key:
            raise ValueError("Missing FISH_API_KEY in environment.")
        if not self.fish_reference_id:
            raise ValueError("Missing FISH_REFERENCE_ID in environment.")

    @property
    def ASSETS_DIR(self) -> Path:
        return self.assets_dir

    @property
    def OUTPUT_DIR(self) -> Path:
        return self.output_dir

    @property
    def TEMP_DIR(self) -> Path:
        return self.temp_dir
