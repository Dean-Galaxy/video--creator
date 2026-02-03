Here is the detailed implementation plan for **AutoSatire**. This plan follows a linear dependency graph, meaning you can start at Task 1.1 and work your way down without hitting blockers.

---

# 📅 AutoSatire Implementation Plan

## Phase 1: Foundation & Configuration

**Goal:** Establish the project structure, manage dependencies, and handle sensitive configuration (API keys) securely.

### Task 1.1: Project Skeleton & Environment Setup

**Context:** Initialize the Git repository, set up the Python virtual environment, and install core libraries (`moviepy`, `requests`, `python-dotenv`, `tqdm`).
**Dependencies:** `None`

* [x] Initialize git repository (`git init`) and create `.gitignore` (exclude `venv`, `.env`, `__pycache__`, `/output`, `/temp`).
* [x] Create virtual environment (`python -m venv venv`) and activate it.
* [x] Create `requirements.txt` with initial dependencies:
```text
moviepy==1.0.3
requests
python-dotenv
tqdm

```


* [x] Create the folder structure:
```text
/assets
/output
/temp
/src

```


* [x] Create a `src/__init__.py` to make the source directory a package.

### Task 1.2: Configuration Manager

**Context:** We need a robust way to load API keys and paths. Hardcoding keys is a security risk. We will use a `.env` file for secrets and a `config.py` module to serve them to the app.
**Dependencies:** `1.1`

* [x] Create a `.env.template` file containing `FISH_API_KEY=` and `FISH_REFERENCE_ID=`.
* [x] Create a real `.env` file (and ensure it is git-ignored).
* [x] Create `src/config.py`.
* [x] Implement a `Config` class in `src/config.py` that reads env vars using `os.environ` or `dotenv`.
* [x] Add default path constants to `Config` class (`ASSETS_DIR`, `OUTPUT_DIR`, `TEMP_DIR`).
* [x] Write a quick `test_config.py` to assert that keys are loaded correctly.

---

## Phase 2: Input Handling & Asset Validation

**Goal:** Ensure the system refuses to run if the script is malformed or if video files are missing, saving time and API credits.

### Task 2.1: Asset Validator Logic

**Context:** The script will ask for "开心/特写". We need a utility that checks if `/assets/开心/特写.mp4` actually exists before we start processing.
**Dependencies:** `1.2`

* [x] Create `src/utils.py`.
* [x] Implement `validate_asset_path(emotion, angle)` function.
* [x] The function should construct the path: `Config.ASSETS_DIR / emotion / angle.mp4`.
* [x] Return `True` if file exists, `False` (or raise `FileNotFoundError`) if not.

### Task 2.2: JSON Script Parser

**Context:** Load the "director's script" and validate its schema.
**Dependencies:** `2.1`

* [x] Create a sample `script.json` in the root with 2-3 test scenes.
* [x] Create `src/parser.py`.
* [x] Implement `load_script(filepath)` which reads the JSON file.
* [x] Add a validation loop: Iterate through every item in the loaded script and call `validate_asset_path` from Task 2.1.
* [x] If any asset is missing, print a friendly error listing *exactly* which file is missing and exit the program.

---

## Phase 3: The Audio Pipeline (Fish Audio)

**Goal:** Convert text into audio files. This is the cost-incurring part, so we need caching or temp file management.

### Task 3.1: Fish Audio Client Wrapper

**Context:** Direct API calls to Fish Audio text-to-speech endpoint.
**Dependencies:** `1.2`

* [x] Create `src/tts.py`.
* [x] Define `generate_audio(text, output_path)` function.
* [x] Construct the HTTP POST request to `https://api.fish.audio/v1/tts`.
* [x] Include headers: `xi-api-key` (from Config) and `Content-Type: application/json`.
* [x] Handle the response: If 200 OK, write the binary content to `output_path`. If 401/400, raise a descriptive exception.

### Task 3.2: Audio Generation Loop

**Context:** Orchestrate the generation for the whole script and manage filenames.
**Dependencies:** `3.1`, `2.2`

* [x] In `src/tts.py`, create a `batch_process_audio(script_data)` function.
* [x] Iterate through the script items. For each item (e.g., ID 1), generate a filename like `temp/1_audio.mp3`.
* [x] Call `generate_audio` for each item.
* [x] **Optimization**: Check if `temp/1_audio.mp3` already exists. If yes, skip API call (saves money during testing).
* [x] Return a list of paths to the generated audio files mapped to their script IDs.

---

## Phase 4: Video Processing Core (MoviePy)

**Goal:** The mathematical logic of aligning video duration to audio duration.

### Task 4.1: The "Clip Maker" Function

**Context:** This is the core logic. It takes one video file and one audio file, and outputs a single `VideoFileClip` object that is perfectly synced.
**Dependencies:** `1.1`

* [x] Create `src/video_processor.py`.
* [x] Import `VideoFileClip`, `AudioFileClip`, `vfx` from `moviepy.editor`.
* [x] Define `create_clip(video_path, audio_path)`.
* [x] Load audio and get duration: `audio_duration`.
* [x] Load video (`video_clip`).
* [x] **Logic Branch**:
* If `audio_duration > video_duration`: Use `vfx.loop` to loop video. Set video duration to `audio_duration`.
* If `audio_duration < video_duration`: Use `.subclip(0, audio_duration)` to cut video.


* [x] Set the audio of the video clip to the loaded audio (`video.set_audio(audio)`).
* [x] Return the processed `VideoFileClip` object.

### Task 4.2: Unit Testing the Logic

**Context:** Verify Task 4.1 works without running the full app.
**Dependencies:** `4.1`

* [x] Create a standalone script `test_render.py`.
* [ ] Manually point it to one dummy video and one dummy audio.
* [ ] Run `create_clip` and write the result to `test_output.mp4`.
* [ ] Manually verify: Does the video stop exactly when audio stops? (Yes/No).

---

## Phase 5: Assembly & Orchestration

**Goal:** Tie the Parser, TTS, and Video Processor together into a pipeline.

### Task 5.1: The Stitching Engine

**Context:** Combine the list of processed clips into one final movie.
**Dependencies:** `4.1`

* [x] In `src/video_processor.py`, add `assemble_video(clips_list, output_path)`.
* [x] Use `moviepy.editor.concatenate_videoclips(clips_list)`.
* [x] Write the result using `.write_videofile(output_path, codec="libx264", audio_codec="aac")`.
* [x] Ensure `fps` is set (e.g., `fps=30`) during write to prevent sync drift.

### Task 5.2: Main Application Logic

**Context:** The `main.py` entry point that calls everything in order.
**Dependencies:** `2.2`, `3.2`, `5.1`

* [x] Create `main.py` in root.
* [x] **Step 1**: Load Config & Script (Task 2.2).
* [x] **Step 2**: Generate/Get Audio for all lines (Task 3.2).
* [x] **Step 3**: Initialize an empty list `final_clips`.
* [x] **Step 4**: Loop through script items:
* Determine video path (Task 2.1).
* Determine audio path (from Step 2).
* Call `create_clip` (Task 4.1).
* Append result to `final_clips`.


* [x] **Step 5**: Call `assemble_video` (Task 5.1).
* [x] **Step 6**: Print "Done! File saved to..."

---

## Phase 6: UX & Cleanup

**Goal:** Make it usable and tidy.

### Task 6.1: Progress Bars & CLI Args

**Context:** Users need to know the script is working, not frozen.
**Dependencies:** `5.2`

* [x] Use `argparse` in `main.py` to allow specifying script file: `python main.py my_script.json`.
* [x] Wrap the main processing loop in `tqdm` to show a progress bar (e.g., "Processing Clip 3/10").

### Task 6.2: Temporary File Cleanup

**Context:** `temp/` will fill up with mp3s. We should offer to clean it.
**Dependencies:** `3.2`

* [x] In `src/utils.py`, add `cleanup_temp()` function.
* [x] Call this at the very end of `main.py`.
* [x] (Optional) Add a `--keep-temp` flag to CLI to skip cleanup for debugging.

### Task 6.3: Documentation

**Context:** Help the user understand how to name folders.
**Dependencies:** `All`

* [x] Write `README.md`.
* [x] Include the specific directory structure diagram:
```
/assets
   /Happy
      Close.mp4

```


* [x] document how to get the Fish Audio API Key.