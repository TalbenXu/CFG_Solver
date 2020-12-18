import re
def ebnf_file_reader(filename):
    search_pattern = re.compile(r'Start:([\s\S]*)Productions:([\s\S]*)')
    with open(filename, 'r', encoding="utf-8") as f:
        string = f.read()
    match_instance = search_pattern.search(string)
    if match_instance == None:
        raise Exception("The form of ebnf is not correct.")
    start_symbol, production_rules = match_instance.group(1).strip(), match_instance.group(2).split(';')
    return start_symbol, production_rules

def ebnf_grammar_loader(production_rules):
    # paser the string to dict datastructure
    grammar = dict()
    for rule in production_rules:
        _ = rule.split('->')
        head, LHS = _[0].strip(), _[1]
        if head not in grammar:
            grammar[head] = []
        for rule in LHS.split('|'):
            rule = rule.split()
            grammar[head].append(rule)
    return grammar

# Convert every repetition * or { E } to a fresh non-terminal X and add
# X = $\epsilon$ | X E
def ebnf_repetition_replace(grammar):
    return grammar

# Convert every option ? [ E ] to a fresh non-terminal X and add
# X = $\epsilon$ | E.
# (We can convert X = A [ E ] B. to X = A E B | A B.)
def ebnf_option_replace(grammar):
    return grammar

# Convert every group ( E ) to a fresh non-terminal X and add
# X = E.
def ebnf_group_replace(grammar):
    return grammar

def ebnf_bnf_convertor(filename):
    start_symbol, production_rules = ebnf_file_reader(filename)
    grammar = ebnf_grammar_loader(production_rules)
    grammar = ebnf_repetition_replace(grammar)
    grammar = ebnf_option_replace(grammar)
    grammar = ebnf_group_replace(grammar)
    return start_symbol, grammar

if __name__ == "__main__":
    print(ebnf_bnf_convertor('demo/simple_EBNF_example.txt'))