from pydub import AudioSegment
from pydub.silence import split_on_silence

address = "audio/" #folder name
projectname = filename +".wav"  #naming for filename
NUMBER_OF_FILES = 37 # number of files in folder (to be added as a cli input in future)
num = 1 # cli input
file_name = "" 
seconds_req = 5 # number in seconds u want the clips to be of duration

names = [] #this block is for adding the wav file names to the names list
for index in range (NUMBER_OF_FILES):
    digit_len= len(str(num)) #0
    for zeros in range (3-digit_len):
        file_name = file_name +'0'
    names.append(file_name+str(num)+projectname)
    num = num + 1
    file_name=""

#this block is for printing the found files in the directory as audio segments
for index in range (NUMBER_OF_FILES): 
    path = address + names[index]
    audio_file = AudioSegment.from_wav(path)
    print(audio_file,"\t",index+1)


for file_in_directory in range(NUMBER_OF_FILES):
    path = ADDRESS + names[file_in_directory]
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