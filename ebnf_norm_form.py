import re
import copy
new_terminal_subscript = 0
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

def ebnf_bracket_match(rule, i_position):
    index = i_position
    while index >= 0:
        if rule[index] == "(":
            return index
        index -= 1
    return Exception("Ebnf form is not correct.")

def num_generator():
    global new_terminal_subscript
    new_terminal_subscript += 1
    return new_terminal_subscript

# Convert every repetition * or { E } to a fresh non-terminal X and add
# X = $\epsilon$ | X E
# Convert every option ? [ E ] to a fresh non-terminal X and add
# X = $\epsilon$ | E.
def ebnf_sign_replace(grammar, sign):
    if sign != "?" and sign != "*":
        raise Exception('Only accept ? or *')
    # select * position
    new_rule_checker = dict()
    for head in grammar:
        for rule in grammar[head]:
            i = 0
            while i < len(rule):
                if rule[i] == sign:
                    if i == 0:
                        raise Exception('Ebnf form is not correct!')
                    elif rule[i-1] != ")":
                        repetition_start = i-1
                    else:
                        repetition_start = ebnf_bracket_match(rule, i)
                    repetition = ' '.join(rule[repetition_start:i+1])
                    if repetition in new_rule_checker:
                        rule[repetition_start:i+1] = [new_rule_checker[repetition]]
                    else:
                        X = f'X{num_generator()}'
                        rule[repetition_start:i+1] = [X]
                        new_rule_checker[repetition] = X
                    i = repetition_start
                i += 1
    for repetition in new_rule_checker:
        new_nonterminal = new_rule_checker[repetition]
        if sign == '*':
            temp_list = [new_nonterminal]
        else:
            temp_list = []
        temp_list.extend(repetition[0:-1].split())
        grammar[new_nonterminal] = [['ε'],temp_list]
    return grammar

    new_rule_checker = dict()
    for head in grammar:
        for rule in grammar[head]:
            i = 0
            while i < len(rule):
                if rule[i] == "?":
                    if i == 0:
                        raise Exception('Ebnf form is not correct!')
                    elif rule[i-1] != ")":
                        repetition_start = i-1
                    else:
                        repetition_start = ebnf_bracket_match(rule, i)
                    repetition = ' '.join(rule[repetition_start:i+1])
                    if repetition in new_rule_checker:
                        rule[repetition_start:i+1] = [new_rule_checker[repetition]]
                    else:
                        X = f'X{num_generator()}'
                        rule[repetition_start:i+1] = [X]
                        new_rule_checker[repetition] = X
                    i = repetition_start
                i += 1
    for repetition in new_rule_checker:
        new_nonterminal = new_rule_checker[repetition]
        temp_list = []
        temp_list.extend(repetition[0:-1].split())
        grammar[new_nonterminal] = [['ε'],temp_list]
    return grammar

# Convert every group ( E ) to a fresh non-terminal X and add
# X = E.
def ebnf_group_replace(grammar):
    for head in grammar:
        for rule in grammar[head]:
            for element in rule:
                if element == '(' or element == ')':
                    rule.remove(element)
    return grammar

def check_head(grammar, rule):
    for in_head in grammar:
        for in_rule in grammar[in_head]:
            if rule in in_rule:
                return in_head
    return False   

def ebnf_BIN(grammar):
    new_grammar = dict()
    for head in grammar:
        for rule in grammar[head]:
            if len(rule) >= 3:
                long_rule = copy.copy(rule)
                first = long_rule.pop(0)
                rule.clear()
                rule.append(first)
                # check whether has this rule
                X = check_head(new_grammar,long_rule)
                if X == False:
                    X = check_head(grammar, long_rule)
                if X:
                    rule.append(X)
                    break
                else:
                    X = f'X{num_generator()}'
                    rule.append(X)
                new_grammar[X] = []
                temp = copy.copy(long_rule)
                if len(long_rule) == 2:
                    new_grammar[X].append(temp)
                    long_rule.clear()
                else:
                    first = long_rule.pop(0)
                    RHX = check_head(new_grammar,long_rule)
                    if RHX == False:
                        RHX = check_head(grammar,long_rule)
                    if RHX == False:
                        RHX = f'X{num_generator()}'
                    new_grammar[X].append([first, RHX])
                while len(long_rule) >= 2:
                    if len(long_rule) == 2:
                        new_grammar[RHX] = []
                        new_grammar[RHX].append(long_rule)
                        break
                    first = long_rule.pop(0)
                    print(f'long{long_rule}')
                    # check whether has this rule
                    X = RHX
                    RHX = check_head(new_grammar,long_rule[1:])
                    if RHX == False:
                        RHX = check_head(grammar,long_rule[1:])
                    if RHX == False:
                        RHX = f'X{num_generator()}'
                    temp_rule = [first,RHX]
                    new_grammar[X] = []
                    new_grammar[X].append(temp_rule)

    for new_head in new_grammar:
        grammar[new_head] = new_grammar[new_head]
    return grammar
                

def ebnf_bnf_normal_convertor(filename):
    start_symbol, production_rules = ebnf_file_reader(filename)
    grammar = ebnf_grammar_loader(production_rules)
    grammar = ebnf_sign_replace(grammar, '*')
    grammar = ebnf_sign_replace(grammar, '?')
    grammar = ebnf_group_replace(grammar)
    grammar = ebnf_BIN(grammar)
    return start_symbol, grammar

if __name__ == "__main__":
    print(ebnf_bnf_normal_convertor('demo/simple_EBNF_example.txt'))