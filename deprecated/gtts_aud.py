from gtts import gTTS

language= "en"

text= "VIVE, sometimes referred to as HTC Vive, is a virtual reality brand of HTC Corporation. It consists of hardware like its titular virtual reality headsets and accessories, virtual reality software and services, and initiatives that promote applications of virtual reality in sectors like business and arts. The brand's first virtual reality headset, simply called HTC Vive, was introduced. HTC has also released accessories that integrate with the Vive and SteamVR, including sensors for motion capture and facial capture."

# text= "VIVE, sometimes"
speech = gTTS(lang= language, text=text, slow= True, tld="com")
speech.save("new.mp3")

# ====================================================================================


from pydub import AudioSegment

# Load the MP3 file
input_file = "new.mp3"
audio = AudioSegment.from_mp3(input_file)

# Adjust the speed (change the factor as needed)
speedup_factor = 1.25  # Increase speed by 50%
speeded_audio = audio.speedup(playback_speed=speedup_factor)

# Save the modified audio as a new MP3 file
output_file = "output.mp3"
speeded_audio.export(output_file, format="mp3")

print(f"Speeded audio saved as {output_file}")

