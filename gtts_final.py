from gtts import gTTS
import shutil
import os
from pydub import AudioSegment
from pydub.generators import Sine


def replace_punctuation_with_words(text):
    text = text.replace(',', ' comma')
    text = text.replace('.', ' fullstop')
    text = text.replace('!', ' exclamation')
    text = text.replace('?', ' question')
    text = text.replace(':', ' colon')
    text = text.replace(';', ' semicolon')        
    return text

def audio_speedifyer(gap, count):

    # Create a 1-second blank audio segment
    blank_audio = AudioSegment.silent(duration=gap)  # 1000 milliseconds = 1 second

    # Export the blank audio segment to a file (optional)
    blank_audio.export("audio_holder/blank.mp3", format="mp3")
    done_audio = AudioSegment.empty()
    for i in range(count):
        audio1 = AudioSegment.from_mp3(f'audio_holder/segments_{i}_.mp3')
        audio2 = AudioSegment.from_mp3('audio_holder/blank.mp3')      
        result_audio = audio1 + audio2    
        done_audio= done_audio+result_audio
    done_audio.export("final.mp3", format="mp3")



language= "en"


raw_text="VIVE, sometimes referred to as HTC Vive, is a virtual reality brand of HTC Corporation. It consists of hardware like its titular virtual reality headsets and accessories, virtual reality software and services, and initiatives that promote applications of virtual reality in sectors like business and arts. The brand's first virtual reality headset, simply called HTC Vive, was introduced. HTC has also released accessories that integrate with the Vive and SteamVR, including sensors for motion capture and facial capture."


modified_text = replace_punctuation_with_words(raw_text)
res = modified_text.split() 

newpath = r'audio_holder'
if os.path.exists(newpath):
    shutil.rmtree(newpath)

os.makedirs(newpath)


count=0
for i in res: 
    speech = gTTS(lang= language, text=i, slow= True, tld="com.au")
    speech.save(f'audio_holder/segments_{count}_.mp3')
    count=count+1

count=count-1
print(count)


audio_speedifyer(500, count)








