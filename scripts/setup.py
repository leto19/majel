"""
collection of setup functions for Majel
"""
from jsgf import PublicRule, RootGrammar
import getpass
import os
import requests


def generate_prog_list():
    """
    use cmd history files to get a list of programs
    """
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
            line_cleaned = line.strip(
                "- cmd: ").strip("sudo").strip("\n").split()
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
    sorted_dict = {k: v for k, v in sorted(
        master_dict.items(), key=lambda item: item[1], reverse=True)}

    out_list = list()
    for dict_el in sorted_dict:
        if sorted_dict[dict_el] >= 1:
            out_list.append(dict_el)
    return out_list


def create_grammar(word_list, name, gram_file):
    """
    read a list of programs in a text file ('progs.txt') and create
    a grammar file for that list,
    such that the speech can one of any of the programs
    """
    upp_list = list()
    grammar = RootGrammar(name=name, case_sensitive=True)
    i = 0
    for lines in word_list:
        rule_name = "rule" + str(i)
        upp = lines.upper().strip()
        if upp.isalpha() is True:
            r = PublicRule(rule_name, upp, case_sensitive=True)
            grammar.add_rule(r)
            upp_list.append(upp)
            i = i+1

    with open(gram_file, 'wt') as g:
        print(grammar.compile(), file=g)


def write_list_to_file(prog_list, filename):
    print(prog_list)
    with open(filename+".txt", 'wt') as f:
        for e in prog_list:
            print(e, file=f)


def get_directory(path=os.getcwd()):
    """takes a directory path and returns a
    list containing the names of all directories
    it contains and all directories they contain (2 levels deep)
    """
    master_list = list()
    dirnames = [name for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))]
    master_list += dirnames
    for dirs in dirnames:
        fp = os.path.join(path, dirs)
        if os.access(fp, os.R_OK) and not dirs.startswith("."):
            fp_dirnames = [name for name in os.listdir(fp)
                           if os.path.isdir(os.path.join(fp, name))]
            master_list += fp_dirnames
    return master_list


def get_dictionary(file_read, file_write="words.dict"):
    """takes a text file of a list of words(file_read) and returns
    a dictionary file (file_write) describing
    how to understand that word aloud.

    """
    url = "http://www.speech.cs.cmu.edu/cgi-bin/tools/logios/lextool.pl"
    print("reading %s..." % file_read)
    files = {'wordfile': open(file_read, 'rb')}
    r = requests.post(url, files=files)  # get HTML responce of file upload
    for lines in r.text.split(">"):  # find download link
        if "<!-- DICT " in lines:
            dl_link = lines
    dl_link = dl_link.replace("<!-- DICT ", "")  # strip download link
    dl_link = dl_link.replace("  --", "")
    #print(dl_link)
    dict_responce = requests.get(
        dl_link, allow_redirects=True)  # get dict file
    print("writing %s to file..." % file_write)
    open(file_write, 'wb').write(
        dict_responce.content)  # write contents of dict


def combine_dictionary(parent, child):
    with open(parent, 'a') as p:
        with open(child, 'rt') as c:
            p.write(c.read())


def setup_dict_grammar():
    """
    create grammar and dictionary files for most commonly used
    programs and current directory.
    """
    # exercute script that populates a file progs.txt
    os.system('/home/g/year3/majel/scripts/compgen.sh')

    # get content of progs.txt
    with open("/home/g/year3/majel/scripts/progs.txt", 'rt') as f:
        data = f.readlines()
    # formatting
    data = [s.replace("\n", "") for s in data]
    # use cmd history files to get the most common commands used

    master = generate_prog_list()
    # returns list of most common programs

    prog_list = compare_prog_list(master, data)
    # writes program list to file
    write_list_to_file(prog_list, "/home/g/year3/majel/scripts/progs_out")

    # creates grammar and writes to file
    create_grammar(prog_list, "progs", "/home/g/year3/majel/grammars/progs.gram")

    # use web service to create program dictionary
    get_dictionary("/home/g/year3/majel/scripts/progs_out.txt",
                   "/home/g/year3/majel/scripts/progs.dict")

    # gets folder names from the given directory
    folder_list = get_directory("/home/g/year3")

    # make sure that command control words are in the dictionary
    # - maybe find a more elegant way of doing this, seperate dict probably.
    folder_list.append("SLASH")
    folder_list.append("DASH")
    folder_list.append("DOT")
    folder_list.append("EXIT")
    folder_list.append("SUDO")
    folder_list += ["A", "B", "C", "D", "E", "F", "G", "H", "M" ,"O","T","V","S"]

    # writes folder list to file
    write_list_to_file(folder_list, "/home/g/year3/majel/scripts/folders_out")

    # create grammar and writes to file
    create_grammar(folder_list, "folders",
                   "/home/g/year3/majel/grammars/folders.gram")

    # use web service to create folder dictionary
    get_dictionary("/home/g/year3/majel/scripts/folders_out.txt",
                   "/home/g/year3/majel/scripts/folders.dict")

    print("combining dictionaries...")
    # combines program and folder dictionaries 
    combine_dictionary(
        "/home/g/year3/majel/scripts/progs.dict", "/home/g/year3/majel/scripts/folders.dict")

    # combines program and master dictionaries
    master_path = "/home/g/year3/majel/languages/cmd2/master.dict"
    combine_dictionary(master_path, "/home/g/year3/majel/scripts/progs.dict")
    print("done!")

    # remove temporary files
    os.remove("/home/g/year3/majel/scripts/folders_out.txt")
    os.remove("/home/g/year3/majel/scripts/progs_out.txt")
    os.remove("/home/g/year3/majel/scripts/progs.dict")
    os.remove("/home/g/year3/majel/scripts/folders.dict")
    os.remove("/home/g/year3/majel/scripts/progs.txt")

if __name__ == "__main__":
    setup_dict_grammar()
