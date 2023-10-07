from pydub import AudioSegment
from pydub.generators import Sine

def audio_speedifyer(gap, master_list):

    # Create a 1-second blank audio segment
    blank_audio = AudioSegment.silent(duration=gap)  # 1000 milliseconds = 1 second

    # Export the blank audio segment to a file (optional)
    blank_audio.export("audio_holder/blank.mp3", format="mp3")
    done_audio = AudioSegment.empty()
    for i in range(len(master_list)):
        audio1 = AudioSegment.from_mp3(f'audio_holder/segments_{i}_.mp3')
        audio2 = AudioSegment.from_mp3('audio_holder/blank.mp3')      
        result_audio = audio1 + audio2    
        done_audio= done_audio+result_audio
    done_audio.export("final.mp3", format="mp3")











