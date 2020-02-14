import sys
import os
import subprocess
import speech_recognition as sr
import pyaudio


mic = sr.Microphone(chunk_size=1024, sample_rate=44100)   
mic.list_microphone_names()

recog = sr.Recognizer()  # this is the object that recognises the speech
"""
    file = sr.AudioFile(sys.argv[1])  # the audio file
    with file as source:
        audio = recog.record(source, duration=int(sys.argv[2]), )
        size = source.DURATION
"""

with mic as source:
    print("listening...")
    #recog.adjust_for_ambient_noise(source)
    audio = recog.listen(source, phrase_time_limit=float(sys.argv[1]))
print("done!")
print("Using language EN-%s" % sys.argv[2])
#print("the length of the file is %s seconds\n" % int(size))
# print('Without: ' + str(recog.recognize_sphinx(audio, show_all=False)))
# print('With: ' + str(recog.recognize_sphinx(audio,
#                                             show_all=False, grammar='Boats.jsgf')))
# os.remove('Boats.fsg')

out = recog.recognize_sphinx(audio,language='en-'+sys.argv[2])
print("You said:\n%s" %out.lower())

"""
print("The first %s seconds of the file \"%s\" are:" %(sys.argv[2],sys.argv[1]))

print('\"%s\"' % out)
index = 0
for word in out.split():
    index+=1
    if word == sys.argv[4]:
        print('\n\"%s\" is found at word %s'% (sys.argv[4],index))
"""

out = out.lower()
process = subprocess.run(out.split())

if process.returncode != 0:
    print("there was a problem!")
else:
    exit()