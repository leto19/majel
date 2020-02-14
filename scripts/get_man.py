import sys
import os
import subprocess as sp
import re
with open(sys.argv[1],'rt') as f:
    data = f.read()

data = data.split() 
prog_opt_dict = dict()
args_dict = dict()
for line in data:
    #print(line)
    try:
        process = sp.Popen(['man'],stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT)
        man =  sp.check_output(["man",line])
        man_words = man.decode('utf-8')
        args = re.findall(r"-+\w+", man_words)
        for a in args:
            if a not in args_dict:
                args_dict[a] = 1
            else:
                args_dict[a] +=1
    except sp.CalledProcessError:
        print("non zero exit")
sorted_args = {k: v for k, v in sorted(args_dicitem[1])}da item: item[1])}t.items(),reverse=True, key=lambda item: item[1])}

with open(sys.argv[1].rstrip(".txt")+"_args_sorted.txt","wt") as f:
    for x,y in sorted_args.items():
        print(x,":",y, file = f, end ="")