import os
import argparse
import collections
import contextlib
import json
import wave
import webrtcvad
from pydub import AudioSegment

# --- VAD Helper Classes ---
class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from pydub AudioSegment."""
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)  # 2 bytes per sample
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    
    # Get raw data
    raw_data = audio.raw_data
    
    while offset + n < len(raw_data):
        yield Frame(raw_data[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n

def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
    """
    Filters out non-voiced audio frames.
    Uses a ring buffer to keep a small amount of silence around speech 
    to avoid cutting off the start/end of words.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    triggered = False

    voiced_frames = []

    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []

    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])

# --- Main Logic ---

def preprocess_audio(audio):
    """
    Standardize audio for NLP: 16kHz, Mono, 16-bit.
    """
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2) # 16-bit
    return audio

def process_file(file_path, args):
    print(f"Processing: {file_path}")
    
    try:
        # Load and Preprocess
        audio = AudioSegment.from_file(file_path)
        audio = preprocess_audio(audio)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return

    # VAD Setup
    vad = webrtcvad.Vad(args.aggressiveness) # 0-3 (3 is most aggressive at filtering noise)
    frames = frame_generator(30, audio, 16000)
    segments = vad_collector(16000, 30, args.padding, vad, frames)

    # Prepare Output
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(args.output, base_name)
    
    if not args.dry_run:
        os.makedirs(output_dir, exist_ok=True)
        manifest_path = os.path.join(output_dir, "manifest.jsonl")
        manifest_file = open(manifest_path, "w")

    print(f"  Analysing speech segments...")
    
    segment_count = 0
    for i, segment_bytes in enumerate(segments):
        # Create AudioSegment from raw bytes
        clip = AudioSegment(
            data=segment_bytes,
            sample_width=2,
            frame_rate=16000,
            channels=1
        )
        
        duration = len(clip) / 1000.0
        
        # Filter too short clips (often noise artifacts)
        if duration < args.min_duration:
            continue

        segment_count += 1
        filename = f"{base_name}_{i:04d}.wav"
        
        if args.dry_run:
            print(f"    [Dry Run] Clip {i}: {duration:.2f}s")
        else:
            # Save Audio
            clip_path = os.path.join(output_dir, filename)
            clip.export(clip_path, format="wav")
            
            # Write Metadata
            meta = {"path": filename, "duration": duration, "text": ""}
            manifest_file.write(json.dumps(meta) + "\n")
            
            if args.verbose:
                print(f"    Saved {filename} ({duration:.2f}s)")

    if not args.dry_run:
        manifest_file.close()
        print(f"  Done. Saved {segment_count} clips and manifest to {output_dir}/")

def parse_args():
    parser = argparse.ArgumentParser(description="Slice audio using Robust VAD for NLP.")
    
    parser.add_argument("input_path", help="Path to input file or directory")
    parser.add_argument("--output", "-o", default="sliced_audio", help="Output directory")
    
    # VAD Parameters
    parser.add_argument("--aggressiveness", type=int, choices=[0, 1, 2, 3], default=2, 
                        help="How aggressive to filter silence. 3 is most aggressive. (Default: 2)")
    parser.add_argument("--padding", type=int, default=300, 
                        help="Milliseconds of silence to allow around speech (Default: 300)")
    parser.add_argument("--min-duration", type=float, default=1.0, 
                        help="Minimum clip duration in seconds to keep (Default: 1.0)")
    
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print details")

    return parser.parse_args()

def main():
    args = parse_args()
    if os.path.isfile(args.input_path):
        process_file(args.input_path, args)
    elif os.path.isdir(args.input_path):
        for filename in os.listdir(args.input_path):
            if filename.lower().endswith(('.wav', '.mp3', '.flac', '.m4a')):
                process_file(os.path.join(args.input_path, filename), args)

if __name__ == "__main__":
    main()