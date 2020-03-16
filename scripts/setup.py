"""
collection of setup functions for Majel
"""
from jsgf import PublicRule, RootGrammar,parser
import getpass
import os
import requests
import re
from configparser import ConfigParser
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
    with open("%s/majel_log.txt" % path) as f:
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
        print("upp is",upp)
        if upp != "" and upp != "{" and upp != "}" and upp != "." and upp[0] != "_":
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
        if len(f) <=20:
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
    for dirs in dirnames:
        if dirs[0] != "." and dirs[0] != "_":
            master_list.append(dirs)

    """
    for dirs in dirnames:
        print("dirs is ",dirs)
        fp = os.path.join(path, dirs)
    
        if os.access(fp, os.R_OK) and not dirs.startswith("."):
            fp_dirnames = [name for name in os.listdir(fp)
                           if os.path.isdir(os.path.join(fp, name))]
            master_list += fp_dirnames
    
    """
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
        print("upp is ",exp)
        if exp not in old_rules_text and exp != "" and exp != "{" and exp != "}" and exp != ".":
            r = PublicRule(rule_name, exp, case_sensitive=True)
            new_gram.add_rule(r)
            i += 1

    # compile new grammar back to file
    new_gram.compile_to_file(grammar_path,compile_as_root_grammar=True)

def convert_underscores(word):
    letter_list = list(word)
    #print(letter_list)
    for i,char in enumerate(letter_list):
        print(i,char)
        if char == "_":
            letter_list[i] = " UNDERSCORE "
    final_word = "".join(letter_list)
    return final_word
def update_file_grammar_dictionary(p):
   
    (file_list,ext_list) = get_filenames(p)
    write_list_to_file(file_list, "%s/scripts/files_out" % path)
    write_list_to_file(ext_list, "%s/scripts/exts_out"% path)
    add_to_grammar(
        "%s/grammars/files.gram", "%s/scripts/files_out.txt" % path, "files")
    add_to_grammar(
        "%s/grammars/exts.gram" % path, "%s/scripts/exts_out.txt" % path, "exts")
    all_list = file_list + ext_list
    write_list_to_file(all_list, "%s/scripts/all_out" % path)

    get_dictionary("%s/scripts/all_out.txt" % path,
                   "%s/scripts/all.dict" % path)
  
    master_path = "%s/languages/cmd2/master.dict" % path

    combine_files(
        master_path, "%s/scripts/all.dict"% path)
    
    os.remove("%s/scripts/files_out.txt" % path)
    os.remove("%s/scripts/exts_out.txt" % path)
    os.remove("%s/scripts/all_out.txt" % path)
    if os.path.exists("%s/scripts/all.dict" % path):
        os.remove("%s/scripts/all.dict" % path)


def read_cfg():
    cfg = ConfigParser()
    cfg.read('/home/g/year3/majel/scripts/config.ini')
    global timeout,path
    timeout = cfg.getint('general','timeout')
    path = cfg.get('installation', 'location')

def get_path():
    cfg = ConfigParser()

    cfg.read('/home/g/year3/majel/scripts/config.ini')
    return cfg.get('installation', 'location')

def update_folder_grammar_dictionary(p):
    #print(p)
    os.remove("%s/grammars/command.fsg" % path)
    folder_list = get_directory(p)
    #print("FOLDER_LIST", folder_list)

    write_list_to_file(
        folder_list, "%s/scripts/folders_out" % path)
    add_to_grammar(
        "%s/grammars/folders.gram" % path,"%s/scripts/folders_out.txt" % path,"folders")
    # use web service to create folder dictionary
    get_dictionary("%s/scripts/folders_out.txt" % path,
                        "%s/scripts/folders.dict" % path)
    master_path = "%s/languages/cmd2/master.dict" % path

    combine_files(
        master_path, "%s/scripts/folders.dict" % path)
    os.remove("%s/scripts/folders.dict" % path)
    os.remove("%s/scripts/folders_out.txt" % path)

def update_alias_grammar_dictionary():
    if os.path.exists("%s/grammars/command.fsg" % path):
        os.remove("%s/grammars/command.fsg" % path)
    alias_list = get_alias()
    write_list_to_file(
        alias_list, "%s/scripts/alias_out" % path)
    add_to_grammar(
        "%s/grammars/alias.gram" % path, "%s/scripts/alias_out.txt", "alias" % path)
    # use web service to create folder dictionary
    get_dictionary("%s/scripts/alias_out.txt" % path,
                        "%s/scripts/alias.dict" % path)
    master_path = "%s/languages/cmd2/master.dict" % path

    combine_files(
        master_path, "%s/scripts/alias.dict" % path)
    os.remove("%s/scripts/alias.dict" % path)
    os.remove("%s/scripts/alias_out.txt" % path)




def combine_files(parent, child):
    with open(parent, 'a') as p:
        with open(child, 'rt') as c:
            p.write(c.read())



def update_all(p=os.curdir):
    update_folder_grammar_dictionary(p)
    update_file_grammar_dictionary(p)
    update_alias_grammar_dictionary()

def get_alias():
    path = get_path()
    with open("%s/alias.txt" % path, "r") as f:
        lines = f.readlines()
    a = list()
    for l in lines:
        a.append(l.split()[0])
    return a
def setup_dict_grammar():
    """
    create grammar and dictionary files for most commonly used
    programs and current directory.
    """
    path = get_path()
    # exercute script that populates a file progs.txt
    os.system('%s/scripts/compgen.sh' % path)

    # get content of progs.txt
    with open("%s/scripts/progs.txt" % path, 'rt') as f:
        data = f.readlines()
    # formatting
    data = [s.replace("\n", "") for s in data]
    # use cmd history files to get the most common commands used

    master = generate_prog_list()
    # returns list of most common programs
    prog_list = compare_prog_list(master, data)
    # writes program list to file
    write_list_to_file(prog_list, "%s/scripts/progs_out" % path)

    # creates grammar and writes to file
    create_grammar(prog_list, "progs", "%s/grammars/progs.gram" % path)

    alias_list = get_alias()
    write_list_to_file(alias_list,"%s/scripts/alias_out" % path)
    create_grammar(alias_list, "alias", "%s/grammars/alias.gram" % path)

    # use web service to create program dictionary
    #get_dictionary("%s/scripts/progs_out.txt",
    #               "%s/scripts/progs.dict")

    # gets folder names from the given directory
    folder_list = get_directory("/home/g/year3")
    
    # writes folder list to file
    write_list_to_file(folder_list, "%s/scripts/folders_out" % path)

    # create grammar and writes to file
    create_grammar(folder_list, "folders",
                   "%s/grammars/folders.gram" % path)

    #get file names and extensionsfrom the given directory:
    (file_list,ext_list) = get_filenames()
    print(file_list,ext_list)
    write_list_to_file(file_list, "%s/scripts/file_out" % path)
    write_list_to_file(ext_list, "%s/scripts/exts_out" % path)
    create_grammar(file_list, "files",
                   "%s/grammars/files.gram" % path)
    create_grammar(ext_list, "exts",
                   "%s/grammars/exts.gram" % path)

    
    # make sure that command control words are in the dictionary
    cmd_list = list()
    cmd_list.append("SLASH")
    cmd_list.append("DASH")
    cmd_list.append("DOT")
    cmd_list.append("EXIT")
    cmd_list.append("SUDO")
    cmd_list.append("CAPITAL")
    cmd_list.append("UPPER")
    cmd_list.append("LOWER")
    cmd_list.append("EXECUTE")

    cmd_list += ["A", "B", "C", "D", "E", "F",
                 "G", "H", "M", "O", "T", "V", "S"]
    write_list_to_file(cmd_list, "%s/scripts/cmd_out" % path)
    # no need to create grammar here, already hand written 
    
    # combines all word lists into one
    print("combining word lists...")
    combine_files("%s/scripts/folders_out.txt" % path,
                       "%s/scripts/progs_out.txt" % path)
    combine_files("%s/scripts/folders_out.txt" % path,
                  "%s/scripts/cmd_out.txt" % path)
    combine_files("%s/scripts/folders_out.txt" % path,
                  "%s/scripts/file_out.txt" % path)
    combine_files("%s/scripts/folders_out.txt" % path,
                  "%s/scripts/exts_out.txt" % path)
    combine_files("%s/scripts/folders_out.txt" % path,
                  "%s/scripts/alias_out.txt" % path)
    master_path = "%s/languages/cmd2/master.dict" % path
    # use web service to create dictionary
    print("getting dictionary...")
    get_dictionary("%s/scripts/folders_out.txt"% path,master_path)
    print("done!")

    # remove temporary files
    os.remove("%s/scripts/folders_out.txt" % path)
    os.remove("%s/scripts/progs_out.txt" % path)
    os.remove("%s/scripts/cmd_out.txt" % path)
    os.remove("%s/scripts/exts_out.txt" % path)
    os.remove("%s/scripts/file_out.txt" % path)
    os.remove("%s/scripts/alias_out.txt" % path)

    os.remove("%s/scripts/progs.txt" % path)

path = get_path()
if __name__ == "__main__":
    setup_dict_grammar()
    #(file_list, ext_list) = get_filenames()
    #print(file_list, ext_list)
    #print(convert_underscores("file_name"))
