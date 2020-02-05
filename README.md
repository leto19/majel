
# Majel(WIP) - Voice command for CLI

This is my testing for my third year project

Need method of testing that the input is a valid command for CLI before running

Interface with system- paste into Terminal?

Challenge seems to be in designing of grammar - talk to Richard?

Also in recognising user defined file/folder names eg

> "ceedee year two slash coursework" -> ```cd year2/coursework```

perhaps define custom language? If format of input is ALWAYS
> ```<KEYWORD> <VARIABLE>``` (```cd year2```)

or

 > ```sudo <KEYWORD> <VARIABLE>``` (```sudo rm pictures```)

could use custom 'bash' language  for keyword(s) then use english for rest. Limiting scope of language may also speed up processing?

Or could simply write to string from input and perform all analysis of input from there.

## Links

* [SpeechRecognition](<https://pypi.org/project/SpeechRecognition/>)
  * [documentation](<https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst>) 
* [PocketSphinx-Python](<https://github.com/bambocher/pocketsphinx-python>)
  * [documentation](<https://cmusphinx.github.io/wiki/>) 
* [JSGF for grammar](<http://www.gavo.t.u-tokyo.ac.jp/~kuenishi/java/sphinx4/edu/cmu/sphinx/jsapi/JSGFGrammar.html>)
* [PyAudio](<http://people.csail.mit.edu/hubert/pyaudio/#downloads>)
