from graphviz import Source
from graph_reader import read_graph
# from grammar_reader import read_grammar
from ebnf_norm_form import ebnf_bnf_normal_convertor
if __name__ == '__main__':
    # Algorithm 1: The standard CFL-reachability algorithm
    # input
    graph_file = input("Please Enter Graph File Name\n").strip()
    grammar_file = input("Please Enter Grammar File Name\n").strip()
    if graph_file == "" and grammar_file == "":
        graph_file = 'demo/ebnf_node.txt'
        grammar_file = 'demo/simple_grammar_example2.txt'
    
    g = read_graph(graph_file)
    print("The original graph:-----------------------")
    g.print_graph()
    start_symble, grammar = ebnf_bnf_normal_convertor('demo/simple_EBNF_example.txt')
    print("The grammar: ---------------------------")
    print(grammar)
    print("--"*10)
    # output
    output_set = set()
    # add E to W
    Worklist = g.output_edge()
    # add epilon production as edge to graph
    for left_variable in grammar.keys():
        for rule in grammar[left_variable]:
            if rule == ['ε']:
                for node in g.vertices.keys():
                    g.add_edge(node, node, left_variable)
                    Worklist.append([left_variable,node,node])
    print("Add epilon production as edge to graph","--"*10)
    g.print_graph()
    # Do the work in Worklist
    while Worklist != []:
        selected_edge = Worklist.pop()
        # X = Y
        for X, right_list in grammar.items():
            for right in right_list:
                if len(right) == 1 and right[0] == selected_edge[0]:
                    Y = right[0]
                    for pair in g.symbol_pair[Y]:
                        if not (g.check_edge(pair[0],pair[1],X)):
                            g.add_edge(pair[0],pair[1],X)
                            Worklist.append([X,pair[0],pair[1]])
        # X = YZ
        for X, right in grammar.items():
            for right_symbols in right:
                if len(right_symbols) == 2 and right_symbols[0] == selected_edge[0]:
                    Y = right_symbols[0]
                    Z = right_symbols[1]
                    if Z in g.symbol_pair:
                        for pair in g.symbol_pair[Z]:
                            j = selected_edge[2]
                            i = selected_edge[1]
                            k = pair[1]
                            if pair[0] == selected_edge[2]:
                                if not (g.check_edge(i,k,X)):
                                    print(selected_edge)
                                    print(i,j,k,X,Y,Z)
                                    g.add_edge(i,k,X)
                                    Worklist.append([X,i,k])
                                    g.print_graph()
        # X = ZY
        for X, right in grammar.items():
            for right_symbols in right:
                if len(right_symbols) == 2 and right_symbols[1] == selected_edge[0]:
                    Y = right_symbols[1]
                    Z = right_symbols[0]
                    for pair in g.symbol_pair[Z]:
                        j = selected_edge[2]
                        i = selected_edge[1]
                        k = pair[0]
                        if pair[1] == i:
                            if not (g.check_edge(k,j,X)):
                                g.add_edge(k,j,X)
                                Worklist.append([X,k,j])
    print("Ending graph: --------------------------")
    g.print_graph()
    print(g.output_set())
    g.dump_dot()

    with open('generated_file/dump_dot.dot','r') as f1:
        s = Source(f1.read(), filename="generated_file/test.gv", format="png")
        s.render()
