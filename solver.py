from graphviz import Source

class Solver:
    def __init__(self, mode):
        self.mode = mode

    def solve(self, graph, grammar):
        if self.mode == "Cubic":
            self.__cubic_solve(graph, grammar)
    
    def __cubic_solve(self, graph, grammar):
        Worklist = graph.output_edge()
        for left_variable in grammar.keys():
            for rule in grammar[left_variable]:
                if rule == ['ε']:
                    for node in graph.get_vertice():
                        graph.add_edge(node, node, left_variable)
                        Worklist.append([left_variable,node,node])
        while Worklist != []:
            selected_edge = Worklist.pop()
            for X, right_list in grammar.items():
                for right in right_list:
                    if len(right) == 1 and right[0] == selected_edge[0]:
                        Y = right[0]
                        for pair in graph.symbol_pair_l(Y):
                            if not (graph.check_edge(pair[0],pair[1],X)):
                                graph.add_edge(pair[0],pair[1],X)
                                Worklist.append([X,pair[0],pair[1]])
            for X, right in grammar.items():
                for right_symbols in right:
                    if len(right_symbols) == 2 and right_symbols[0] == selected_edge[0]:
                        Y = right_symbols[0]
                        Z = right_symbols[1]
                        if Z in graph.symbol_pair():
                            for pair in graph.symbol_pair_l(Z):
                                j = selected_edge[2]
                                i = selected_edge[1]
                                k = pair[1]
                                if pair[0] == selected_edge[2]:
                                    if not (graph.check_edge(i,k,X)):
                                        # print(selected_edge)
                                        # print(i,j,k,X,Y,Z)
                                        graph.add_edge(i,k,X)
                                        Worklist.append([X,i,k])
            for X, right in grammar.items():
                for right_symbols in right:
                    if len(right_symbols) == 2 and right_symbols[1] == selected_edge[0]:
                        Y = right_symbols[1]
                        Z = right_symbols[0]
                        for pair in graph.symbol_pair_l(Z):
                            j = selected_edge[2]
                            i = selected_edge[1]
                            k = pair[0]
                            if pair[1] == i:
                                if not (graph.check_edge(k,j,X)):
                                    graph.add_edge(k,j,X)
                                    Worklist.append([X,k,j])
        graph.dump_dot()
