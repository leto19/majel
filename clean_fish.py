import sys
import os

with open(sys.argv[1],'rt') as f:
    data = f.readlines()

out_list = list()
for line in data:

    #print(line)
    #print(len(max(line.split())))

    if "- cmd:" in line and len(max(line.split(), key=len)) <=30:

        #turn command into speech-like input for building language 
        line = line.replace("- cmd: ", "" )        
        line = line.replace("/"," slash ")
        line = line.replace("*", " wildcard")
        #line = line.replace(">", " pipe to ")
        line = line.replace(".", " dot ")
        line = line.replace("-", " dash ")
        #line = line.replace("~/", "home")
        line = line.replace("|", "and")

        out_list.append(line)

with open(sys.argv[1].rstrip(".txt")+"_cleaned.txt","wt") as f:
    for e in out_list:
            print(e, file=f, end = "")
