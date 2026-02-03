from pathlib import Path

from src.video_processor import create_clip


def main() -> None:
    video_path = Path("assets/开心/右中景.mp4")
    audio_path = Path("temp/1_audio.mp3")
    output_path = Path("output/test_output.mp4")

    clip = create_clip(video_path, audio_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clip.write_videofile(str(output_path), codec="libx264", audio_codec="aac", fps=30)
    clip.close()


if __name__ == "__main__":
    main()
