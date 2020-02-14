#!/bin/bash
echo arg is $1
P=$@
echo P is $P
builtin cd $P
ls
     