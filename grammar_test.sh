#!/bin/bash
pocketsphinx_continuous -jsgf grammars/command.jsgf -inmic yes -hmm ./languages/acoustic-model/ -dict ./languages/cmd2/cmd2.dict
