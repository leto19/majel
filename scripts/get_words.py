import os, sys

with open(sys.argv[1],'rt') as f:
    data = f.readlines()


out = set()
for lines in data:
    #print(lines)
    for words in lines.split():
        #print(words)
        out.add(words)

with open(sys.argv[1].rstrip(".txt")+"_words.txt","wt") as f:
    for e in out:
        #print(e)
        print(e, file=f) 