# Slice

Slice is a python program to automatically cut audio files into smaller duration clips.
The program automatically avoids cutting in-between words to get clips with whole sentences, better for training Natural Language Processing models.

## Installation

pip install -r requirements.txt
## Usage
One command line argument for folder name
example:
```bash
$ python3 slice.py audio
```
Enter the wav file inside the directory
```bash
$ Enter Filename: speech
  Address: audio/speech.wav
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
