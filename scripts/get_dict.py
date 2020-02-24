import requests

def get_dict(file_read,file_write="words.dict"):
    """takes a text file of a list of words(file_read) and returns
    a dictionary file (file_write) describing how to understand that word aloud.

    """
    url = "http://www.speech.cs.cmu.edu/cgi-bin/tools/logios/lextool.pl" 
    #url = 'https://httpbin.org/post'
    print("reading %s..."%file_read)
    files = {'wordfile': open(file_read,'rb')}
    r = requests.post(url,files=files) #get HTML responce of file upload
    for lines in r.text.split(">"):#find download link
        if "<!-- DICT " in lines:
            dl_link = lines
    #print(dl_link) 
    dl_link = dl_link.replace("<!-- DICT ","") #strip download link
    dl_link = dl_link.replace("  --","") 
    print(dl_link)
    dict_responce = requests.get(dl_link, allow_redirects=True) #get dict file from link
    print("writing %s to file..."% file_write)
    open(file_write, 'wb').write(dict_responce.content) #write contents of dict to file 

get_dict("prog_list.txt","prog.dict")