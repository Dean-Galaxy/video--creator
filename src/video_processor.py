from pathlib import Path
from typing import List, Optional

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips, vfx


def create_clip(video_path: Path, audio_path: Optional[Path]) -> VideoFileClip:
    video_clip = VideoFileClip(str(video_path))
    if audio_path is None:
        return video_clip

    audio_clip = AudioFileClip(str(audio_path))
    audio_duration = audio_clip.duration
    video_duration = video_clip.duration

    if audio_duration > video_duration:
        looped = video_clip.fx(vfx.loop, duration=audio_duration)
        video_clip = looped.set_duration(audio_duration)
    elif audio_duration < video_duration:
        video_clip = video_clip.subclip(0, audio_duration)

    return video_clip.set_audio(audio_clip)


def assemble_video(clips_list: List[VideoFileClip], output_path: Path) -> None:
    final_clip = concatenate_videoclips(clips_list, method="compose")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_clip.write_videofile(
        str(output_path), codec="libx264", audio_codec="aac", fps=30
    )
    final_clip.close()
