from jsgf import PublicRule, RootGrammar
import getpass 
import os



def generate_prog_list():
    master_list = list()
    user = getpass.getuser()
    #get bash history
    with open("/home/%s/.bash_history" % user) as f:
        bash_list = f.readlines()

    for line in bash_list:
        split_line = line.split();
        if split_line != [] and split_line[0] not in master_list:
            print(split_line[0])
            master_list.append( split_line[0])  
    #get fish history (if it exists)

    fish_path = "/home/%s/.local/share/fish/fish_history" % user
    if os.path.exists(fish_path):
        with open(fish_path) as f:
            fish_list = f.readlines()

    for line in fish_list:
        if "- cmd:" in line:
            line_cleaned = line.strip("- cmd: ").strip("sudo").strip("\n").split()
            if line_cleaned != [] and split_line[0] not in master_list:
                master_list.append(line_cleaned)
    
    print(master_list)

    
def create_grammar():
    """
    read a list of programs in a text file ('progs.txt')and create a grammar file for that list,
    such that the speech can one of any of the programs
    """
    upp_list = list()
    with open("progs.txt",'rt') as f:
        data = f.readlines()
    grammar = RootGrammar(name="progs",case_sensitive=True)
    i = 0
    for lines in data:
        rule_name = "rule" + str(i)
        #print(rule_name)
        upp= lines.upper().strip()
        

        if upp.isalpha() == True:
            r = PublicRule(rule_name,upp,case_sensitive=True)
            #print(r.generate())
            #print(r)
            grammar.add_rule(r)
            upp_list.append(upp)

            i = i+1
    #print(grammar.compile())

    with open("progs.gram",'wt') as g:
        print(grammar.compile(),file=g)

    with open("prog_list.txt",'wt') as f:
        for e in upp_list:
            print(e,file=f)

if __name__ == '__main__':
    generate_prog_list()
    create_grammar()