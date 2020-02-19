import requests

def get_dict(file_read,file_write):
    url = "http://www.speech.cs.cmu.edu/cgi-bin/tools/logios/lextool.pl"
    #url = 'https://httpbin.org/post'
    files = {'wordfile': open(file_read,'rb')}
    r = requests.post(url,files=files)
    for lines in r.text.split(">"):
        if "<!-- DICT " in lines:
            dl_link = lines
    print(dl_link)
    dl_link = dl_link.replace("<!-- DICT ","")
    dl_link = dl_link.replace("  --","")
    print(dl_link)
    r2 = requests.get(dl_link, allow_redirects=True)
    open(file_write, 'wb').write(r2.content)

get_dict("prog_list.txt","prog.dict")