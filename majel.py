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

def get_generic_command(lang,gram):
    if len(sys.argv) == 2: #use audio file
        audio_file = sr.AudioFile(sys.argv[1])
        with audio_file as source:
            audio = recog.record(source)
    else: #use mic 
        mic = sr.Microphone(chunk_size=1024, sample_rate=44100)
        with mic as source:
            #recog.adjust_for_ambient_noise(source)
            #time.sleep(0.5)
            #print("listening...")

            audio = recog.listen(source,phrase_time_limit=3)
    #print("done!")    

    try:
        #print("working...")
        out = recog.recognize_sphinx(audio,language=lang,grammar=gram)
        #show_possible(out)
    except sr.UnknownValueError:
        out = ("didn't quite get that")
        exit()
    #return out.hyp().hypstr.lower().split()
    return out.lower().split()
 
def show_possible(decoder):
    #print("Best 10 hypothesis:")
    for best, i in zip(decoder.nbest(),range(10)):
        print(best.hypstr,best.score)
        
def run_command(command):
    """
    if command[0] == "cd":
        
        d = "--working-directory="+os.getcwd()+"/"+"".join(command[1:])
        d = replace_space_with_slash(d)
        #print(d)
        process = subprocess.Popen(["gnome-terminal",d])
        #time.sleep(1)
        #os.kill(os.getppid(), signal.SIGHUP)
        
        d = os.getcwd()+"/"
        #d = replace_space_with_slash(d)
        d = "\"" +d 
        #print(d)
        d+="".join(command[1:]) + "\""

        #print("d after:",d)
        process = subprocess.call(["./cd.sh",d],shell=False)
    """
    try:
        #process = subprocess.run(command)
        full_command = command + [">","/dev/tty"]
        #print(full_command)
        process = subprocess.run(full_command)
        exit()
    except FileNotFoundError:
        #print("not a valid command!")
        exit()
   
    
def replace_space_with_slash(path):
    path = path.replace("/", "\"/\"") + "\""
    #path = re.sub("./.","\"/\" ",path)
    path = path[1:-2]
    return path
    

def word_to_character(phrase):
    for n,i in enumerate(phrase):
        #print(i,n)
        if i =="slash":
            phrase[n] = phrase[n-1] + "/" + phrase[n+1]
            phrase.pop(n+1)
            phrase.pop(n-1)
        if i == "dot":
            phrase[n] = phrase[n-1] + "." + phrase[n+1]
            #print(phrase[n])
            phrase.pop(n+1)
            phrase.pop(n-1)
        
        if i == "dash":
            phrase[n] = "-"+phrase[n+1] + " "
            phrase.pop(n+1)
    
    return phrase
    
if __name__ == "__main__":
    l = ("./languages/acoustic-model","./languages/cmd1/cmd1.lm","./languages/cmd2/cmd2.dict")
    gram = "./grammars/command.jsgf"
    command_words = str()
    while "exit" not in command_words:
        command_words  = get_generic_command(l,gram);
        #command_words = ["ls","dash", "a","slash","home"]
        #print("You said:\n%s" % command_words)  
        command_words.append(" ") 
        command_words = word_to_character(command_words)
        #print("running command:\n%s" % command_words)
        print("--------------------------------------------------------------------------")
        #run_command(command_words)
        print(" ".join(command_words))

