import requests
url = "http://www.speech.cs.cmu.edu/cgi-bin/tools/logios/lextool.pl"
#url = 'https://httpbin.org/post'
files = {'wordfile': open('progs.txt','rb')}
r = requests.post(url,files=files)
for lines in r.text.split(">"):
    if "<!-- DICT " in lines:
        dl_link = lines
print(dl_link)
dl_link = dl_link.replace("<!-- DICT ","")
dl_link = dl_link.replace("  --","")
print(dl_link)
r2 = requests.get(dl_link, allow_redirects=True)
#print(r2.content)
open('/home/g/year3/majel/languages/cmd2/progs1.dict', 'wb').write(r2.content)
