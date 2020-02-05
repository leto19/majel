#!/usr/bin/env python3
import sys
import os
import subprocess
import speech_recognition as sr
import pyaudio
from contextlib import contextmanager
import signal
import time
import re
from ctypes import *


recog = sr.Recognizer()  # this is the object that recognises the speech
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)
# Initialize PyAudio
p = pyaudio.PyAudio()
p.terminate()

def get_command():
    mic = sr.Microphone(chunk_size=1024, sample_rate=44100)
    lang = ("./languages/en-CL2/acoustic-model","./languages/en-CL3/4953.lm","./languages/en-CL3/4953.dic")   
    with mic as source:
        print("listening...")
        audio = recog.listen(source, phrase_time_limit=float(sys.argv[1]))
    print("done!")    
    try:
        out = recog.recognize_sphinx(audio,language=lang)
    except sr.UnknownValueError:
        print("didn't quite get that")
        exit()
    if "cancel" not in out.lower().split():

        return out.lower().split()
    else:
        exit()      



def get_generic_command(lang):

    if len(sys.argv) == 3: #use audio file
        audio_file = sr.AudioFile(sys.argv[2])
        with audio_file as source:
            audio = recog.record(source)
    else: #use mic 
        mic = sr.Microphone(chunk_size=1024, sample_rate=44100)
        with mic as source:
            recog.adjust_for_ambient_noise(source)
            time.sleep(0.5)
            print("listening...")

            audio = recog.listen(source)
    print("done!")    

    try:
        out = recog.recognize_sphinx(audio,language=lang,grammar='grammars/command.jsgf')
        #show_possible(out)
    except sr.UnknownValueError:
        print("didn't quite get that")
        exit()
    #return out.hyp().hypstr.lower().split()
    return out.lower().split()
 
def show_possible(decoder):
    print("Best 10 hypothesis:")
    for best, i in zip(decoder.nbest(),range(10)):
        print(best.hypstr,best.score)
def run_command(command):
    if command[0] == "cd":
        """
        d = "--working-directory="+os.getcwd()+"/"+"".join(command[1:])
        d = replace_space_with_slash(d)
        print(d)
        process = subprocess.Popen(["gnome-terminal",d])
        #time.sleep(1)
        #os.kill(os.getppid(), signal.SIGHUP)
        """
        d = os.getcwd()+"/"
        #d = replace_space_with_slash(d)
        d = "\"" +d 
        print(d)
        d+="".join(command[1:]) + "\""

        print("d after:",d)
        process = subprocess.call(["./cd.sh",d],shell=False)

    try:
        process = subprocess.Popen(command)
    except FileNotFoundError:
        print("not a valid command!")
        exit()
   
    exit()
    
def replace_space_with_slash(path):
    path = path.replace("/", "\"/\"") + "\""
    #path = re.sub("./.","\"/\" ",path)
    path = path[1:-2]
    return path
    

def word_to_character(phrase):
    for n,i in enumerate(phrase):
        if i == " " or i =="slash":
            phrase[n] = "/"
        if i == "dot":
            phrase[n] ="."
        if i == "dash":
            phrase[n] = "-"+phrase[n+1]
            phrase.pop(n+1)
    return phrase


#l = ("./languages/acoustic-model","./languages/fish3/fish3.lm","./languages/fish3/fish3.dic")
l = ("./languages/acoustic-model","./languages/cmd1/cmd1.lm","./languages/cmd1/cmd1.dic")

#command_words = ['cd','dot','dot']
command_words  = get_generic_command(l);
print("You said:\n%s" % command_words)   
command_words = word_to_character(command_words)
print("running command:\n",command_words)
print("--------------------------------------------------------------------------")
run_command(command_words)


"""
if "arguments" in command_words:
    print("which arguments?")
    args = get_args()

    args = ("-" + s  for s in args)
    #print("you said:\n%s"% args)
    command_words.remove("arguments")
    command_words += args


if "file" in command_words:
    print("for what?")
    f = get_files()
    f = word_to_character(f)
    print("f: ",f)
    f_all = "".join(f)
    print("f_all:", f_all)
    command_words.remove("file")
    command_words.append(f_all)
print("command is:", command_words,"\n--------------------------------------------------------")
run_command(command_words)
"""