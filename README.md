
# Majel(WIP) - Voice command for CLI

A program that allows users to speak command line inputs aloud and have them executed by the system. This would be useful in particular for file system navigation; often user friendly directory and file names with spaces are difficult to access in command line. The project will also in part be an attempt to introduce a 'natural language' way of interacting with the terminal; the input of the speech "Execute My Script" is much more intuitive and descriptive of what the user wants to happen compared typing "./myscript.sh".   

A vastly limited set of possible 'words' in the language of commands as well as more structured  grammar should mean that this program works much faster and more accurately than existing systems such as Google Assistant, Siri or Cortana. Additionally, the program will be fully functional offline, and will not use calls to internet based APIs. 

I have some early demo and proof of concept code here: https://github.com/leto19/majel

## Links

* [SpeechRecognition](<https://pypi.org/project/SpeechRecognition/>)
  * [documentation](<https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst>) 
* [PocketSphinx-Python](<https://github.com/bambocher/pocketsphinx-python>)
  * [documentation](<https://cmusphinx.github.io/wiki/>) 
* [JSGF for grammar](<http://www.gavo.t.u-tokyo.ac.jp/~kuenishi/java/sphinx4/edu/cmu/sphinx/jsapi/JSGFGrammar.html>)
* [PyAudio](<http://people.csail.mit.edu/hubert/pyaudio/#downloads>)
