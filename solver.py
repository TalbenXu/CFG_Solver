

class Solver:
    def __init__(self, mode):
        self.mode = mode

    def solve(self, graph, grammar):
        if self.mode == "Cubic":
            self.__cubic_solve(graph, grammar)
    
    def __cubic_solve(self, graph, grammar):
        # each edge in worklist stand by [(edge, node, node)]
        Worklist = graph.output_edge()
        for nullable_variable in grammar.epsilon:
            for node in graph.get_vertice():
                graph.add_edge(node, node, nullable_variable)
                Worklist.append([nullable_variable,node,node])
        while Worklist != []:
            selected_edge = Worklist.pop()
            for X, right_list in grammar.items():
                # X: key: variable right_list : list of all right handside of production
                for right in right_list:
                    # X = Y
                    if len(right) == 1 and right[0] == selected_edge[0]:
                        Y = right[0]
                        for pair in graph.symbol_pair_l(Y):
                            # O(n) for graph.symbol_pair_l return list of node pair
                            if not graph.new_check_edge(pair[0],pair[1],X):
                                # O(m) m stand for len(varibale, terminal) 
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
                                    if not (graph.new_check_edge(i,k,X)):
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
                                if not (graph.new_check_edge(k,j,X)):
                                    graph.add_edge(k,j,X)
                                    Worklist.append([X,k,j])
        graph.dump_dot()
