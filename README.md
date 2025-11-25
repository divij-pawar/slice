# Slice: Audio Segmentation for NLP Datasets

**Slice** is a command-line utility designed to automatically segment long audio recordings into smaller clips based on voice activity.

It prepares raw audio for Natural Language Processing (NLP) and Speech-to-Text (STT) model training (like Whisper, Kaldi, or Wav2Vec2) by ensuring clips contain distinct speech segments and creating standard metadata manifests.

## Features

* **Robust Voice Activity Detection (VAD):** Uses WebRTC VAD to distinguish human speech from background noise, which is more accurate than simple energy-based silence detection.
* **Automatic Preprocessing:** Automatically converts audio to 16kHz Mono (16-bit), the standard format required by most ASR models.
* **Metadata Generation:** Outputs a `manifest.jsonl` file containing filenames and durations alongside the audio clips.
* **CLI Support:** Fully automatable via command line arguments.
* **Batch Processing:** Process single files or entire directories of audio at once.
* **Dry Run Mode:** Preview how audio will be split without writing files.

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
    Slice relies on `pydub` to load audio files, which requires FFmpeg.
    * **Mac:** `brew install ffmpeg`
    * **Linux:** `sudo apt-get install ffmpeg`
    * **Windows:** [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

## Usage

### Basic Command
Slice a single audio file using default settings. This will create a folder containing `.wav` clips and a `manifest.jsonl`.

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
You can tune the VAD sensitivity to fit different microphone qualities or background noise levels.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `input_path` | *Required* | Path to a file or directory. |
| `--output` | `sliced_audio` | Directory to save the result clips and manifest. |
| `--aggressiveness` | `2` | VAD aggressiveness level (0-3). 3 is the most strict at filtering non-speech. |
| `--padding` | `300` | Milliseconds of silence allowed around speech chunks. Higher values keep words from being cut off. |
| `--min-duration` | `1.0` | Minimum duration (in seconds) for a clip to be kept. Useful for filtering clicks/coughs. |
| `--dry-run` | `False` | If set, prints stats but does not save files. |
| `--verbose` | `False` | Prints detailed processing info for every clip saved. |

### Examples

**Noisy Audio:**
If the audio has significant background noise, increase the aggressiveness to strictly detect human voice:
```bash
python slice.py podcast.wav --aggressiveness 3
```
**Keep Short Utterances:**
To keep very short responses (like "Yes" or "No"), reduce the minimum duration:
```bash
python slice.py speech.wav --min-duration 0.5
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the MIT License. See `LICENSE` for more information.