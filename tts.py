from gtts import gTTS

def text_to_speech():
    text = input("Enter the sentence to convert to TTS: ")

    tts = gTTS(text=text, lang='en')
    filename = "output.mp3"

    tts.save(filename)
    print(f"TTS conversion complete! Saved as: {filename}")

if __name__ == "__main__":
    text_to_speech()
