import argparse
import sys
from pathlib import Path

from tqdm import tqdm

from src.config import Config
from src.parser import load_script
from src.tts import batch_process_audio
from src.utils import cleanup_temp, validate_asset_path
from src.video_processor import assemble_video, create_clip


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoSatire video generator")
    parser.add_argument("script", type=str, help="Path to script JSON")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temp audio")
    parser.add_argument(
        "--no-tts",
        action="store_true",
        help="Skip TTS and render video only (no audio)",
    )
    return parser.parse_args()


def resolve_output_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    suffix = base_path.suffix
    stem = base_path.stem
    parent = base_path.parent
    index = 1
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def main() -> None:
    args = parse_args()
    config = Config.load(Path.cwd())
    if not args.no_tts:
        config.validate()

    script_path = Path(args.script)
    try:
        script_items = load_script(script_path, config)
    except FileNotFoundError as exc:
        print(f"Asset validation failed: {exc}")
        sys.exit(1)
    final_clips = []
    if args.no_tts:
        for item in tqdm(script_items, desc="Processing clips"):
            video_path = validate_asset_path(item.emotion, item.angle, config)
            final_clips.append(create_clip(video_path, None))
    else:
        audio_map = batch_process_audio(script_items, config)
        for item in tqdm(script_items, desc="Processing clips"):
            video_path = validate_asset_path(item.emotion, item.angle, config)
            audio_path = audio_map[item.item_id]
            final_clips.append(create_clip(video_path, audio_path))

    output_path = resolve_output_path(config.output_dir / "output.mp4")
    assemble_video(
        final_clips,
        output_path,
        config.intro_music_path,
        config.outro_music_path,
    )

    if not args.keep_temp and not args.no_tts:
        cleanup_temp(config)

    print(f"Done! File saved to {output_path}")


if __name__ == "__main__":
    main()
