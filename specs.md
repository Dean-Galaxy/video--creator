Here is the comprehensive Product Requirements Document (PRD) for the **AutoSatire** project, compiled from our discussion.

This document serves as the single source of truth for the engineering implementation.

---

# Product Requirements Document (PRD): AutoSatire

**Version:** 1.0 (MVP)
**Status:** Approved for Development
**Date:** October 26, 2023

---

## 1. Project Overview

**AutoSatire** is a Python-based Command Line Interface (CLI) automation tool designed to streamline the production of "Daily Show" style satirical news videos.

The tool aims to solve the bottleneck of manual video editing by programmatically combining pre-recorded video assets (categorized by emotion and camera angle) with AI-generated voiceovers. It acts as an intelligent "rough cut" generator, taking a structured script and raw assets to produce a synchronized video track ready for final cosmetic touches (BGM/Captions) in external software.

---

## 2. Core Requirements

### 2.1 Functional Requirements

* **Script Ingestion**: The system must parse a standard JSON file containing the sequence of shots, emotions, and dialogue text.
* **Asset Resolution**: The system must automatically locate video files based on a specific directory structure (`/Emotion/Angle.mp4`).
* **Voice Synthesis**: The system must integrate with the **Fish Audio API** to generate high-quality, cloned voice audio for each script segment.
* **Temporal Alignment**:
* If **Audio Duration > Video Duration**: The video clip must loop to match the audio.
* If **Audio Duration < Video Duration**: The video clip must be hard-cut to match the audio.


* **Video Stitching**: The system must concatenate all processed segments into a single linear `.mp4` file.
* **No Lip Sync**: No lip-synchronization or facial animation processing is required.

### 2.2 Non-Functional Requirements

* **Performance**: Rendering time should be reasonable (Python `MoviePy` based).
* **Quality**: Output resolution and frame rate should match the input assets (target 1080p, 30fps).
* **Reliability**: The system must handle missing assets or API failures gracefully with clear error messages.
* **Security**: API keys must be stored in a separate configuration file, not hardcoded.

---

## 3. Core Features

### Feature A: The "Director" Parser

* Reads the input JSON script.
* Validates that requested angles/emotions exist in the local asset library before starting expensive rendering.

### Feature B: The "Voice" Generator (TTS)

* Iterates through script lines.
* Sends text to Fish Audio.
* Downloads and caches temporary audio files (`.mp3`).
* Calculates precise duration of generated audio.

### Feature C: The "Editor" Engine

* Loads the required video file (`.mp4`).
* **Logic Branch**:
* **Loop Mode**: Calculates how many times to repeat the 5s clip to cover the audio duration.
* **Cut Mode**: Trims the video stream to end exactly when the audio ends.


* Combines the processed video track with the generated audio track.

### Feature D: The Rendering Pipeline

* Concatenates all individual segments.
* Exports the final file to the output directory.
* Cleans up temporary audio files.

---

## 4. Core Components

### 4.1 Data Models

* **ScriptItem**: Object representing a single line of JSON (id, angle, emotion, text).
* **Config**: Singleton managing paths and API keys.

### 4.2 Module Structure

* `main.py`: Entry point and orchestration.
* `config.py`: Loads `config.json`.
* `tts_service.py`: Handles HTTP requests to Fish Audio.
* `video_processor.py`: Handles `MoviePy` logic (looping, cutting, stitching).
* `utils.py`: File I/O helpers and validation.

### 4.3 Directory Structure (User Facing)

```text
/AutoSatire_Root
  ├── config.json          # API Keys and Settings
  ├── script.json          # The script to render
  ├── /assets              # Video Source Files
  │     ├── /开心          # Folder name = Emotion
  │     │    ├── 特写.mp4  # File name = Angle
  │     │    └── 全景.mp4
  │     └── /愤怒
  │          └── ...
  ├── /output              # Final renders go here
  └── /temp                # Temporary audio files (auto-deleted)

```

---

## 5. App/User Flow

1. **Setup**: User places raw video files in `/assets` and fills `config.json` with API Key.
2. **Scripting**: User generates `script.json` (via external tool/AI) defining the flow.
3. **Execution**: User opens terminal and runs: `python main.py script.json`.
4. **Processing (System)**:
* [Step 1] Validate assets exist.
* [Step 2] Call Fish Audio for all audio lines (Show progress bar).
* [Step 3] Process video clips to match audio lengths.
* [Step 4] Render final `output.mp4`.


5. **Completion**: User retrieves the video from `/output` for final review or posting.

---

## 6. Tech Stack

* **Language**: Python 3.9+
* **Video Processing**: `MoviePy` (Wrapper around FFmpeg).
* *Why*: Excellent for programmatic editing, handling looping/concatenation easily.


* **HTTP Requests**: `requests`
* *Why*: Standard library for calling Fish Audio REST API.


* **Environment Management**: `python-dotenv` or standard `json` lib.
* **CLI UX**: `tqdm` (for progress bars) and `argparse` (for command line arguments).

---

## 7. Implementation Plan

### Phase 1: Environment & Asset Loader (Day 1)

* Set up Python virtual environment.
* Implement `config.json` loader.
* Implement `AssetValidator`: Scans the `/assets` folder and ensures mapped files exist.

### Phase 2: Audio Pipeline (Day 1-2)

* Implement `FishAudioClient`.
* Create a test script to send text and save `.mp3` locally.
* **Deliverable**: A function that takes text and returns a path to a downloaded audio file.

### Phase 3: Video Manipulation Logic (Day 2-3)

* Implement `MoviePy` logic for the "Loop vs Cut" rule.
* Create a unit test: Combine a 5s video with a 12s audio (verify loop) and a 2s audio (verify cut).

### Phase 4: Assembly & CLI (Day 3-4)

* Stitch Phase 2 and Phase 3 together.
* Add the main loop that iterates through the JSON list.
* Add progress bars (`tqdm`).

### Phase 5: Final Polish (Day 5)

* Code cleanup.
* Write `README.md` with instructions on folder naming.
* Dry run with a full script.

---

**Next Step**:
I am ready to act as the Lead Developer. Would you like me to write the **project directory structure** and the **`main.py` core logic** now?