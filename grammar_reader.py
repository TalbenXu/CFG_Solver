"""
G in this form:
start symble: first line
production rules: other line

example:
A
A = a
"""
def read_grammar(file_name):
    grammar = dict()
    with open(file_name,'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                # Read the first line as start_symble
                start_symble = lines[0].strip()
                continue
            left_symble, right_symble = lines[i].strip().split('=')
            right_symble = right_symble.strip()
            left_symble = left_symble.strip()
            if left_symble not in grammar:
                grammar[left_symble] = []
            add_up_list = []
            for symble in right_symble:
                add_up_list.append(symble)
            grammar[left_symble].append(add_up_list)
            start_symble, grammar = start_transform(start_symble, grammar)
    return start_symble, grammar

# For if RHS of the production contains the start symble
# Initiate the new Variable S0
def start_transform(start_symble, grammar):
    flag = False
    for keys in grammar:
        for rule in grammar[keys]:
            if start_symble in rule:
                flag = True
    if flag == True:
        grammar['S'] = [start_symble]
        start_symble = 'S'
    return start_symble, grammar

def Term_transfomr(start_symble, grammar):
    pass

def grammar_new(file_name):
    with open(file_name, 'r') as f:
        




