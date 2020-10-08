from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys

filename = input('Enter Filename: ')
#address = sys.argv[1]+"/"+filename+".wav" #Final address of the wav file
foldername = "audio"
address = foldername+"/"+filename+".wav" #Final address of the wav file
seconds_req = input('Duration of clips in seconds: ') # duration of clips in seconds
print("\nAddress: "+address+"\nSeconds requested:"+seconds_req)

audio_file = AudioSegment.from_wav(address)
print("Audio file: ",audio_file)
print("Audio file average dB: ",audio_file.dBFS)

#paramteres for splitting on silence
a_chunks = split_on_silence(audio_file, min_silence_len=1000, silence_thresh=-32, keep_silence=250,seek_step=1)
#length parameters for splitting audio files
target_length = seconds_req * 1000
#outputting the audio chunks as audio segments
output_chunks = [a_chunks[0]]
for chunk in a_chunks[1:]:
    if int(len(output_chunks[-1])) < int(target_length):
        output_chunks[-1] += chunk
    else:
        # if the last output chunk is longer than the target length,
        # we can start a new one
        output_chunks.append(chunk)
#outputting files of the correct audio length
for i,chunk in enumerate(output_chunks):

    out_file = foldername+"/"+filename+"-part{}.wav".format(i)
    print ("exporting", out_file)
    chunk.export(out_file, format="wav")