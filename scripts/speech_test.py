import pocketsphinx
import speech_recognition as sr
import sys

def display_speech(audio_raw = sys.argv[1]):
    print(sys.argv[1])
    recog = sr.Recognizer()
    if sys.argv[1] == "mic":
        mic = sr.Microphone(chunk_size=1024, sample_rate=44100)

        with mic as source:
            print("listening...")
            audio = recog.listen(source, phrase_time_limit=float(sys.argv[2]))
    else:
        audio_file = sr.AudioFile(audio_raw)
        with audio_file as source:
            audio = recog.record(source,duration=float(sys.argv[2]))

    out = recog.recognize_sphinx(audio,language="en-US")
    print(out)

display_speech()
