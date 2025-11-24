import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

def parse_args():
    parser = argparse.ArgumentParser(description="Slice audio files based on silence.")
    
    # Input/Output arguments
    parser.add_argument("input_path", help="Path to the input audio file or directory")
    parser.add_argument("--output", "-o", default="sliced_audio", help="Directory to save the clips (default: sliced_audio)")
    
    # Silence detection parameters
    parser.add_argument("--min-silence", type=int, default=500, help="Minimum length of silence (ms) to be used for a split (default: 500)")
    parser.add_argument("--thresh", type=int, default=-40, help="Silence threshold (dBFS). Lower = more sensitive (default: -40)")
    parser.add_argument("--keep-silence", type=int, default=100, help="Amount of silence (ms) to leave at beginning/end of each chunk (default: 100)")
    
    # Operational flags
    parser.add_argument("--dry-run", action="store_true", help="Calculate splits but do NOT save files. Useful for tuning parameters.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed processing info")

    return parser.parse_args()

def process_file(file_path, args):
    print(f"Processing: {file_path}")
    
    try:
        audio = AudioSegment.from_file(file_path)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return

    # Split audio logic
    chunks = split_on_silence(
        audio,
        min_silence_len=args.min_silence,
        silence_thresh=args.thresh,
        keep_silence=args.keep_silence
    )

    if not chunks:
        print(f"  [!] No silence found or file too short with current settings.")
        return

    # Dry Run Output
    if args.dry_run:
        print(f"  [DRY RUN] Would create {len(chunks)} clips:")
        for i, chunk in enumerate(chunks):
            print(f"    - Clip {i+1}: {len(chunk)/1000:.2f} seconds")
        return

    # Actual Export
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(args.output, base_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"  Exporting {len(chunks)} clips to '{output_dir}/'...")
    
    for i, chunk in enumerate(chunks):
        out_file = f"{base_name}_{i:03d}.wav"
        out_path = os.path.join(output_dir, out_file)
        chunk.export(out_path, format="wav")
        if args.verbose:
            print(f"    Saved {out_file}")

def main():
    args = parse_args()

    if os.path.isfile(args.input_path):
        process_file(args.input_path, args)
    elif os.path.isdir(args.input_path):
        # Process all wav/mp3 files in directory
        for filename in os.listdir(args.input_path):
            if filename.lower().endswith(('.wav', '.mp3', '.flac')):
                process_file(os.path.join(args.input_path, filename), args)
    else:
        print(f"Error: Input path '{args.input_path}' not found.")

if __name__ == "__main__":
    main()