import os, sys

with open(sys.argv[1],'rt') as f:
    data = f.read()

data = data.splitlines()
out = list()
for lines in data:
    lines = lines.replace("/", " ")
    #print(lines)
    out.append(lines)

with open(sys.argv[1].rstrip(".txt")+"_cleaned.txt","wt") as f:
    for e in out:
        #print(e)
        print(e, file=f)
        