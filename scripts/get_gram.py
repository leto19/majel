from jsgf import PublicRule, RootGrammar
import getpass
import os
import requests


def generate_prog_list():
    master_list = list()
    user = getpass.getuser()
    # get bash history
    with open("/home/%s/.bash_history" % user) as f:
        bash_list = f.readlines()

    for line in bash_list:
        split_line = line.split()
        if split_line != []:
            master_list.append(split_line[0])

    # get fish history (if it exists)
    fish_path = "/home/%s/.local/share/fish/fish_history" % user
    if os.path.exists(fish_path):
        with open(fish_path) as f:
            fish_list = f.readlines()

    for line in fish_list:
        if "- cmd:" in line:
            line_cleaned = line.strip("- cmd: ").strip("sudo").strip("\n").split()
            if line_cleaned != []:
                master_list.append(line_cleaned[0])
    # get majel history
    with open("/home/%s/year3/majel/majel_log.txt" % user) as f:
        majel_list = f.readlines()

    for line in majel_list:
        line_cleaned = line.split()
        if line_cleaned != []:
            master_list.append(line_cleaned[0])
    return (master_list)


def compare_prog_list(master_list, prog_list):
    master_dict = dict().fromkeys(prog_list, 0)
    for els in master_list:
        if els in master_dict.keys():
            master_dict[els] += 1
    sorted_dict = {k: v for k, v in sorted(master_dict.items(), key=lambda item: item[1], reverse=True)}

    out_list = list()
    for dict_el in sorted_dict:
        #print(dict_el, sorted_dict[dict_el])
        if sorted_dict[dict_el] >= 1:
            out_list.append(dict_el)
    return out_list


def create_grammar(word_list, name,gram_file):
    """
    read a list of programs in a text file ('progs.txt') and create
    a grammar file for that list,
    such that the speech can one of any of the programs
    """
    upp_list = list()
    grammar = RootGrammar(name="progs",case_sensitive=True)
    i = 0
    for lines in word_list:
        rule_name = "rule" + str(i)
        upp = lines.upper().strip()
        if upp.isalpha() is True:
            r = PublicRule(rule_name, upp, case_sensitive=True)
            grammar.add_rule(r)
            upp_list.append(upp)
            i = i+1

    with open(gram_file,'wt') as g:
        print(grammar.compile(),file=g)


def write_list_to_file(prog_list,filename):
    print(prog_list)
    with open(filename+".txt",'wt') as f:
        for e in prog_list:
            print(e,file =f)


def get_directory(path=os.getcwd()):
    """takes a directory path and returns a list containing the names of all directories
    it contains and all directories they contain (2 levels deep)
    """
    master_list = list()
    dirnames = [name for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))]
    master_list += dirnames
    for dirs in dirnames:
        fp = os.path.join(path, dirs)
        if os.access(fp, os.R_OK) and not dirs.startswith("."):
            #print(os.listdir(fp))
            fp_dirnames = [name for name in os.listdir(fp)
                           if os.path.isdir(os.path.join(fp, name))]
            master_list += fp_dirnames
    # print(master_list)
    return master_list


def get_dictionary(file_read, file_write="words.dict"):
    """takes a text file of a list of words(file_read) and returns
    a dictionary file (file_write) describing
    how to understand that word aloud.

    """
    url = "http://www.speech.cs.cmu.edu/cgi-bin/tools/logios/lextool.pl" 
    #url = 'https://httpbin.org/post'
    print("reading %s..." % file_read)
    files = {'wordfile': open(file_read, 'rb')}
    r = requests.post(url, files=files)  # get HTML responce of file upload
    for lines in r.text.split(">"):  # find download link
        if "<!-- DICT " in lines:
            dl_link = lines
    dl_link = dl_link.replace("<!-- DICT ", "")  # strip download link
    dl_link = dl_link.replace("  --", "")
    print(dl_link)
    dict_responce = requests.get(dl_link, allow_redirects=True)  # get dict file
    print("writing %s to file..." % file_write)
    open(file_write, 'wb').write(dict_responce.content)  # write contents of dict

def combine_dictionary(parent, child):
    with open(parent, 'a') as p:
        with open(child, 'rt') as c:
            p.write(c.read())

if __name__ == '__main__':  # get HTML responce of file upload
    with open("progs.txt", 'rt') as f:
        data = f.readlines()
    data = [s.replace("\n", "") for s in data]
    master = generate_prog_list()
    prog_list = compare_prog_list(master, data)
    write_list_to_file(prog_list,"progs_out")
    create_grammar(prog_list,"root","progs.gram")    
    get_dictionary("progs_out.txt","progs.dict")

    folder_list = get_directory("/home/g")
    write_list_to_file(folder_list, "folders_out")
    create_grammar(folder_list,"folders","folders.gram")
    get_dictionary("folders_out.txt", "folders.dict")

    combine_dictionary("progs.dict","folders.dict")