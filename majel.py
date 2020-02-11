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
            print("listening...")

            audio = recog.listen(source,phrase_time_limit=3)
    #print("done!")    

    try:
        print("working...")
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
    
    if command[0] == "cd":
        os.chdir(command[1])
        os.listdir()
    try:
        process = subprocess.run(command)
        
    except FileNotFoundError:
        print("not a valid command!")
        
   
    
def replace_space_with_slash(path):
    path = path.replace("/", "\"/\"") + "\""
    #path = re.sub("./.","\"/\" ",path)
    path = path[1:-2]
    return path
    

def word_to_character(phrase):
    phrase = " ".join(phrase)
    phrase = phrase.replace("dash","-")
    phrase = phrase.replace("dot",".")
    phrase = phrase.replace("slash","/")
    
    print(phrase)
    phrase = phrase.split()
    for n,i in enumerate(phrase):
        print(n,i)
        if i == "-":
            phrase[n+1] = "-" + phrase[n+1]
            phrase.pop(n)
        if i == "/":
            phrase[n+1] = "/" + phrase[n+1]
            phrase.pop(n)
    prev_word = "test"
    print("\n-------")
    print(phrase)
    while more_than_one_starting_slash(phrase):
        for index,word in enumerate(phrase):
            print("word is ", word, "at index", index)
            print("prev_word is", prev_word)
            if prev_word[0]== "/" and word[0] == "/":
                new_word = prev_word +"/" + word[1:]
                print("new word is ",new_word)
                phrase[index] = new_word
                phrase.pop(prev_index)
                prev_word = new_word
            else:
                prev_word = word
                prev_index = index
        print(phrase)
    return phrase
    

def more_than_one_starting_slash(phrase):
    flag = 0
    for words in phrase:
        if words[0] is "/":
            flag +=1
    if flag > 1:
        return True
    else:
        return False

if __name__ == "__main__":

    l = ("./languages/acoustic-model","./languages/cmd1/cmd1.lm","./languages/cmd2/cmd2.dict")
    gram = "./grammars/command.jsgf"
    command_words = str()
    """
    command_words = ["ls","dash", "a","slash","home","slash","g","slash","Downloads"]
    #print("You said:\n%s" % command_words)  
    command_words = word_to_character(command_words)
    #print("running command:\n%s" % command_words)
    run_command(command_words)
    """
    

    while "exit" not in command_words:
        command_words  = get_generic_command(l,gram);
        print("You said:\n%s" % command_words)  
        command_words = word_to_character(command_words)
        print("running command:\n%s" % command_words)
        print("--------------------------------------------------------------------------")
        run_command(command_words)
        #print(" ".join(command_words))

    