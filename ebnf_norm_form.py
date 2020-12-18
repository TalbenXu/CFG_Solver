import re
def ebnf_file_reader():
    search_pattern = re.compile(r'Start:([\s\S]*)Productions:([\s\S]*)')
    with open('demo/simple_EBNF_example.txt', 'r', encoding="utf-8") as f:
        string = f.read()
    match_instance = search_pattern.search(string)
    if match_instance == None:
        raise Exception("The form of ebnf is not correct.")
    start_symbol, production_rules = match_instance.group(1).strip(), match_instance.group(2).split(';')
    return start_symbol, production_rules

def ebnf_grammar_loader(start_symbol, production_rules):
    # paser the string to dict datastructure
    grammar = dict()
    for rule in production_rules:
        _ = rule.split('->')
        head, LHS = _[0].strip(), _[1].split()
        if head not in grammar:
            grammar[head] = []
        grammar[head].append(LHS)
    print(grammar)

if __name__ == "__main__":
    ebnf_grammar_loader(*ebnf_file_reader())