from pathlib import Path
from typing import List, Optional

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    VideoFileClip,
    afx,
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
    max_music_duration = 5.0
    fade_duration = 1.0
    final_clip = concatenate_videoclips(clips_list, method="compose")
    created_audio_clips: List[AudioFileClip] = []
    audio_layers = []
    if final_clip.audio:
        audio_layers.append(final_clip.audio)

    if intro_audio_path:
        intro_audio = AudioFileClip(str(intro_audio_path))
        created_audio_clips.append(intro_audio)
        intro_duration = min(
            intro_audio.duration or 0, max_music_duration, final_clip.duration or 0
        )
        if intro_duration > 0:
            intro_clip = intro_audio.subclip(0, intro_duration)
            intro_clip = intro_clip.volumex(0.5)
            intro_clip = intro_clip.fx(afx.audio_fadeout, min(fade_duration, intro_duration))
            audio_layers.append(intro_clip.set_start(0))

    if outro_audio_path:
        outro_audio = AudioFileClip(str(outro_audio_path))
        created_audio_clips.append(outro_audio)
        outro_duration = min(
            outro_audio.duration or 0, max_music_duration, final_clip.duration or 0
        )
        if outro_duration > 0:
            outro_clip = outro_audio.subclip(0, outro_duration)
            outro_clip = outro_clip.volumex(0.5)
            outro_clip = outro_clip.fx(afx.audio_fadein, min(fade_duration, outro_duration))
            start_time = max(0, (final_clip.duration or 0) - outro_duration)
            audio_layers.append(outro_clip.set_start(start_time))

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
