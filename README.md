# AutoSatire

AutoSatire is a CLI tool that assembles a satirical news video from a JSON script,
pre-recorded assets, and Fish Audio-generated voice audio.

## Directory Structure

```
/assets
   /开心
      特写.mp4
      全景.mp4
   /愤怒
      特写.mp4
/output
/temp
/src
```

## Asset Naming

Emotions:
愤怒、嘲讽、平静、伤心、开心

Angles:
全景、远景、中景、近景、特写、留白、右中景、左远景

TTS Emotion Mapping (Fish Audio):
平静->calm、嘲讽->angry、愤怒->angry、伤心->sad、开心->happy

## Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Create your `.env` file:

```
FISH_API_KEY=your_api_key_here
FISH_REFERENCE_ID=your_reference_id_here
INTRO_MUSIC_PATH=assets/bgm/intro.mp3
OUTRO_MUSIC_PATH=assets/bgm/outro.mp3
```

### Getting a Fish Audio API Key

- Sign up at https://fish.audio
- Navigate to the API Keys section to generate an API key.
- Copy the key into your `.env` file.

## Usage

```
python main.py script.json
```

Optional:

```
python main.py script.json --keep-temp
```

Skip TTS (render video without audio):

```
python main.py script.json --no-tts
```
