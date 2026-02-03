from pathlib import Path
from typing import List, Optional

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    VideoFileClip,
    concatenate_videoclips,
    vfx,
)


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


def assemble_video(
    clips_list: List[VideoFileClip],
    output_path: Path,
    intro_audio_path: Optional[Path] = None,
    outro_audio_path: Optional[Path] = None,
) -> None:
    final_clip = concatenate_videoclips(clips_list, method="compose")
    created_audio_clips: List[AudioFileClip] = []
    audio_layers = []
    if final_clip.audio:
        audio_layers.append(final_clip.audio)

    if intro_audio_path:
        intro_audio = AudioFileClip(str(intro_audio_path))
        created_audio_clips.append(intro_audio)
        audio_layers.append(intro_audio.set_start(0))

    if outro_audio_path:
        outro_audio = AudioFileClip(str(outro_audio_path))
        created_audio_clips.append(outro_audio)
        start_time = max(0, final_clip.duration - outro_audio.duration)
        audio_layers.append(outro_audio.set_start(start_time))

    if audio_layers:
        final_audio = CompositeAudioClip(audio_layers)
        final_clip = final_clip.set_audio(final_audio)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        final_clip.write_videofile(
            str(output_path), codec="libx264", audio_codec="aac", fps=30
        )
    finally:
        final_clip.close()
        for clip in created_audio_clips:
            clip.close()
