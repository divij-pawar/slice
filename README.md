# Slice: Audio Segmentation for NLP Datasets

**Slice** is a command-line utility designed to automatically segment long audio recordings into smaller, sentence-level clips based on silence. 



It solves the problem of preparing raw audio for **Natural Language Processing (NLP)** and **Speech-to-Text (STT)** model training (like Whisper, Kaldi, or Wav2Vec2) by ensuring clips contain whole sentences without cutting words in half.

## Features

* **Smart Segmentation:** Uses dB-based silence detection to find natural pauses in speech.
* **CLI Support:** Fully automatable via command line arguments (no interactive prompts).
* **Batch Processing:** Process single files or entire directories of audio at once.
* **Dry Run Mode:** Preview how your audio will be split without writing any files (saves disk space while tuning).
* **Non-Destructive:** Keeps original files intact; saves clips to a new output directory.

## Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/divij-pawar/slice.git](https://github.com/divij-pawar/slice.git)
    cd slice
    ```

2.  **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install FFmpeg (Required)**
    Slice relies on `pydub`, which requires FFmpeg to handle audio files.
    * **Mac:** `brew install ffmpeg`
    * **Linux:** `sudo apt-get install ffmpeg`
    * **Windows:** [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

## Usage

### Basic Command
Slice a single audio file using default settings:

```bash
python slice.py audio/interview.wav
```

### Batch Process a Folder
Process every `.wav` or `.mp3` file in a folder:
```bash
python slice.py data/raw_recordings --output data/processed_dataset
```

### The "Dry Run" (Safe Mode)
Unsure about your settings? Use --dry-run to see the split timestamps without creating files:
```bash
python slice.py audio/interview.wav --dry-run
```

## Configuration / Arguments
You can tune the sensitivity to fit different microphone qualities or background noise levels.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `input_path` | *Required* | Path to a file (`speech.wav`) or directory (`/data`). |
| `--output` | `sliced_audio` | Where to save the result clips. |
| `--min-silence` | `500` | Minimum length of silence (in ms) required to trigger a split. |
| `--thresh` | `-40` | Silence threshold in dBFS. Lower values (e.g., -60) are more sensitive to quiet noise. |
| `--keep-silence` | `100` | How much silence (in ms) to leave at the start/end of each clip (prevents sounding chopped). |
| `--dry-run` | `False` | If set, prints stats but does not save files. |
| `--verbose` | `False` | Prints detailed processing info for every clip saved. |

### Examples

**Noisy Audio (High Threshold):**
If your audio has background buzz, raise the threshold so it isn't mistaken for speech:
```bash
python slice.py podcast.wav --thresh -30
```
**Fast Speech (Short Silence):**
If the speaker talks fast with short pauses, reduce the minimum silence duration:
```bash
python slice.py speech.wav --min-silence 300
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the MIT License. See `LICENSE` for more information.