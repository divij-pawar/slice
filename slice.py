from pydub import AudioSegment
from pydub.silence import split_on_silence


address = "audio/"
projectname = filename +".wav"
number_of_files = 37
num = 1
file_name = ""
seconds_req = 5 

names = []
for index in range (number_of_files):
    digit_len= len(str(num))
    for zeros in range (3-digit_len):
        file_name = file_name +'0'
    names.append(file_name+str(num)+projectname)
    num = num + 1
    file_name=""

for index in range (number_of_files):
    path = address + names[index]
    audio_file = AudioSegment.from_wav(path)
    print(audio_file,"\t",index+1)

for file_in_directory in range(number_of_files):
    path = address + names[file_in_directory]
    print(path)
    audio_segment = AudioSegment.from_wav(path)
    print("Average dB -> ",audio_segment.dBFS)

    a_chunks = split_on_silence(audio_segment, min_silence_len=400, silence_thresh=-36, keep_silence=250,seek_step=1)

    target_length = seconds_req * 1000
    output_chunks = [a_chunks[0]]
    for chunk in a_chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            # if the last output chunk is longer than the target length,
            # we can start a new one
            output_chunks.append(chunk)

    for i,chunk in enumerate(output_chunks):

        out_file = ".//splitAudio//"+names[file_in_directory]+"-part{0}.wav".format(i)
        print ("exporting", out_file)
        chunk.export(out_file, format="wav")