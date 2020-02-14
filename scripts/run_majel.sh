#!/bin/bash
echo "Listening..."
MYOUT=$(./majel.py)
echo $MYOUT
echo $MYOUT|bash 
