import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
for voice in voices:
    print(f"Voice ID: {voice.id}")
    print(f"Name: {voice.name}")
    print(f"Languages: {voice.languages}\n")

