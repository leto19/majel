#!/bin/bash
pocketsphinx_continuous -allphone phonetic.lm -jsgf grammars/command.gram -inmic yes -hmm ./languages/acoustic-model/ -dict ./languages/cmd2/master.dict
