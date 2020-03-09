"""
collection of setup functions for Majel
"""
from jsgf import PublicRule, RootGrammar,parser
import getpass
import os
import requests
import re

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

def get_filenames(path=os.getcwd()):
    files = [name for name in os.listdir(path)
                 if os.path.isfile(os.path.join(path, name))]
    ext = list()
    filenames = list()
    for f in files:
        if "." in f:
            if f.split(".")[1] not in ext:
                ext.append(f.split(".")[1])
            filenames.append(f.split(".")[0])
        else: #file has no extension
            filenames.append(f) 
    print(filenames, ext)
    return (filenames, ext)
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
    """
    takes a text file of a list of words(file_read) and returns
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


def add_to_grammar(grammar_path,file_path,gram_name):
    """
    loads a ``Grammar`` at grammar_path and tries to add rules to it 
    from the file in file_path then returns the new ``Grammar``
    """
    old_gram = parser.parse_grammar_file(grammar_path)
    with open(file_path,'rt') as f:
        word_list = f.readlines()
    #remove root rule from old grammar
    old_gram.remove_rule(old_gram.get_rule_from_name("root"))
    # get list of rules from old grammar
    old_rules = old_gram.rules
    new_gram = RootGrammar(name=gram_name, case_sensitive=True)
    # add existing rules to new grammar
    i = 0 
    old_rules_text = list()
    for rules in old_rules:
        exp = rules.expansion.text.upper()
        old_rules_text.append(exp)
        if exp not in word_list:
            rule_name = "rule" + str(i)
            r = PublicRule(rule_name,exp,case_sensitive=True)
            new_gram.add_rule(r)
            i += 1
    # add new rules to new grammar
    for lines in word_list:
        rule_name = "rule" + str(i)
        exp = lines.upper().strip()
        # print("upp is ",exp)
        if exp.isalpha() is True and exp not in old_rules_text:
            r = PublicRule(rule_name, exp, case_sensitive=True)
            new_gram.add_rule(r)
            i += 1

    # compile new grammar back to file
    new_gram.compile_to_file(grammar_path,compile_as_root_grammar=True)



def update_file_grammar_dictionary(p):
    print("this is happening now")
    (file_list,ext_list) = get_filenames(p)
    write_list_to_file(file_list, "/home/g/year3/majel/scripts/files_out")
    write_list_to_file(ext_list, "/home/g/year3/majel/scripts/exts_out")
    add_to_grammar(
        "/home/g/year3/majel/grammars/files.gram", "/home/g/year3/majel/scripts/files_out.txt", "files")
    add_to_grammar(
        "/home/g/year3/majel/grammars/exts.gram", "/home/g/year3/majel/scripts/exts_out.txt", "exts")
    get_dictionary("/home/g/year3/majel/scripts/files_out.txt",
                   "/home/g/year3/majel/scripts/files.dict")
    get_dictionary("/home/g/year3/majel/scripts/exts_out.txt",
                   "/home/g/year3/majel/scripts/exts.dict")
    master_path = "/home/g/year3/majel/languages/cmd2/master.dict"

    combine_files(
        master_path, "/home/g/year3/majel/scripts/exts.dict")
    combine_files(
        master_path, "/home/g/year3/majel/scripts/files.dict")
    os.remove("/home/g/year3/majel/scripts/files_out.txt")
    os.remove("/home/g/year3/majel/scripts/exts_out.txt")
    os.remove("/home/g/year3/majel/scripts/files.dict")
    os.remove("/home/g/year3/majel/scripts/exts.dict")
    
def update_folder_grammar_dictionary(p):
    #print(p)
    os.remove("/home/g/year3/majel/grammars/command.fsg")
    folder_list = get_directory(p)
    write_list_to_file(
        folder_list, "/home/g/year3/majel/scripts/folders_out")
    add_to_grammar(
        "/home/g/year3/majel/grammars/folders.gram","/home/g/year3/majel/scripts/folders_out.txt","folders")
    # use web service to create folder dictionary
    get_dictionary("/home/g/year3/majel/scripts/folders_out.txt",
                        "/home/g/year3/majel/scripts/folders.dict")
    master_path = "/home/g/year3/majel/languages/cmd2/master.dict"

    combine_files(
        master_path, "/home/g/year3/majel/scripts/folders.dict")
    os.remove("/home/g/year3/majel/scripts/folders.dict")
    os.remove("/home/g/year3/majel/scripts/folders_out.txt")

def combine_files(parent, child):
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
    #get_dictionary("/home/g/year3/majel/scripts/progs_out.txt",
    #               "/home/g/year3/majel/scripts/progs.dict")

    # gets folder names from the given directory
    folder_list = get_directory("/home/g/year3")

    # writes folder list to file
    write_list_to_file(folder_list, "/home/g/year3/majel/scripts/folders_out")

    # create grammar and writes to file
    create_grammar(folder_list, "folders",
                   "/home/g/year3/majel/grammars/folders.gram")

    #get file names and extensionsfrom the given directory:
    (file_list,ext_list) = get_filenames()
    print(file_list,ext_list)
    write_list_to_file(file_list,"/home/g/year3/majel/scripts/file_out")
    write_list_to_file(ext_list, "/home/g/year3/majel/scripts/exts_out")
    create_grammar(file_list, "files",
                   "/home/g/year3/majel/grammars/files.gram")
    create_grammar(ext_list, "exts",
                   "/home/g/year3/majel/grammars/exts.gram")

    
    # make sure that command control words are in the dictionary
    cmd_list = list()
    cmd_list.append("SLASH")
    cmd_list.append("DASH")
    cmd_list.append("DOT")
    cmd_list.append("EXIT")
    cmd_list.append("SUDO")
    cmd_list += ["A", "B", "C", "D", "E", "F",
                 "G", "H", "M", "O", "T", "V", "S"]
    write_list_to_file(cmd_list, "/home/g/year3/majel/scripts/cmd_out")
    # no need to create grammar here, already hand written 
    
    # combines all word lists into one
    print("combining word lists...")
    combine_files("/home/g/year3/majel/scripts/folders_out.txt",
                       "/home/g/year3/majel/scripts/progs_out.txt")
    combine_files("/home/g/year3/majel/scripts/folders_out.txt",
                       "/home/g/year3/majel/scripts/cmd_out.txt")
    combine_files("/home/g/year3/majel/scripts/folders_out.txt",
                  "/home/g/year3/majel/scripts/file_out.txt")
    combine_files("/home/g/year3/majel/scripts/folders_out.txt",
                  "/home/g/year3/majel/scripts/exts_out.txt")
    master_path = "/home/g/year3/majel/languages/cmd2/master.dict"
    # use web service to create dictionary
    print("getting dictionary...")
    get_dictionary("/home/g/year3/majel/scripts/folders_out.txt",master_path)
    print("done!")

    # remove temporary files
    os.remove("/home/g/year3/majel/scripts/folders_out.txt")
    os.remove("/home/g/year3/majel/scripts/progs_out.txt")
    os.remove("/home/g/year3/majel/scripts/cmd_out.txt")
    os.remove("/home/g/year3/majel/scripts/exts_out.txt")
    os.remove("/home/g/year3/majel/scripts/file_out.txt")

    os.remove("/home/g/year3/majel/scripts/progs.txt")

if __name__ == "__main__":
    setup_dict_grammar()
    #(file_list, ext_list) = get_filenames()
    #print(file_list, ext_list)
