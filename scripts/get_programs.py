from jsgf import PublicRule, RootGrammar
    
def main():
    with open("progs.txt",'rt') as f:
        data = f.readlines()
    grammar = RootGrammar(name="progs")
    i = 0
    for lines in data:
        rule_name = "rule" + str(i)
        #print(rule_name)
        r = PublicRule(rule_name,lines)
        grammar.add_rule(r)
        i = i+1

    print(grammar.compile())



if __name__ == '__main__':
    main()