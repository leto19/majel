from jsgf import PublicRule, RootGrammar
    
def main():
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
    main()