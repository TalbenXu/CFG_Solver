"""
G in this form:
terminal: first line
variable: seconde line
start symble: third line
production rules: forth line

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
    return start_symble, grammar





