# implementation of directed graph using Adjacency Matrix, with aphabetic label



class Vertex:
    def __init__(self, n):
        self.name = n

class Graph:
    vertices = {}
    edges = []
    edge_indices = {}
    symbol_pair = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            for row in self.edges:
                row.append([])
            self.edges.append([])
            for _ in range(len(self.edges)):
                self.edges[-1].append([])
            self.edge_indices[vertex.name] = len(self.edge_indices)
            return True
        else:
            return False
    
    def add_edge(self, u, v, label):
        if u in self.vertices and v in self.vertices:
            self.edges[self.edge_indices[u]][self.edge_indices[v]].append(label)
            if label in self.symbol_pair.keys():
                if (u,v) not in self.symbol_pair[label]:
                    self.symbol_pair[label].append((u,v))
            else:
                self.symbol_pair[label] = []
                self.symbol_pair[label].append((u,v))
            return True
        else:
            return False
            
    def print_graph(self):
        print('      ', end='')
        for v, i in sorted(self.edge_indices.items()):
            print(f'{v:9}', end='')
        print()
        for v, i in sorted(self.edge_indices.items()):
            print(v + ' |', end='')
            substr = ""
            for j in range(len(self.edges)):
                for k in self.edges[i][j]:
                    substr += str(k) 
                print(f'{substr:8}|', end='')
                substr = ""
            print(' ')    
    
    def output_edge(self):
        output_list = []
        for edge, pair_list in self.symbol_pair.items():
            for pair in pair_list:
                output_list.append([edge,pair[0],pair[1]])
        return output_list
    
    def check_edge(self, u, v, lable):
        if lable not in self.symbol_pair:
            return False
        if (u,v) in self.symbol_pair[lable]:
            return True
        return False
    
    def output_set(self):
        return self.symbol_pair["M"]

    def dump_dot(self):
        with open('generated_file/dump_dot.dot','w') as f:
            f.write('digraph CFG{\n')
            for node in self.vertices:
                f.write(f'\tn{node};\n')
            for symbol in self.symbol_pair:
                if symbol in 'MVaabarddbar':
                    for pair in self.symbol_pair[symbol]:
                        f.write(f'\tn{pair[0]}->n{pair[1]}[label="{symbol}"]\n')
            f.write('}')

# print(str(len(g.vertices)))
# V1 = Vertex('1')
# V2 = Vertex('2')
# g.add_vertex(V1)
# g.add_vertex(V2)
# print(g.vertices)
# g.add_edge(V1.name, V2.name, 'a')
# g.add_edge(V2.name, V1.name, 'b')
# g.print_graph()