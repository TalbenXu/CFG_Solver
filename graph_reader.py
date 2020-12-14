# Graph Reader for graph txt file 
# into memory and display

# text file format in each line represent a directed edge
# like "1,2,a"
# 1 outbound node, 2 inbound node, with label a edge

# memory representation using adjeceny list
# assume graph is not dense

# display using pydot 

# File Reading get the file Object
from class_graph import *
from dot_graph_reader import read_dot_file
def read_graph(file_name):
    suffix = file_name.split('.')[-1]
    if suffix == 'txt':
        g = Graph()
        with open(file_name,'r') as f:
            for line in f.readlines():
                node1_name, node2_name, edge = line.strip().split(',')
                node1_name = node1_name.strip()
                node2_name = node2_name.strip()
                edge = edge.strip()
                if node1_name not in g.vertices:
                    node1 = Vertex(node1_name)
                    g.add_vertex(node1)
                if node2_name not in g.vertices:
                    node2 = Vertex(node2_name)
                    g.add_vertex(node2)
                g.add_edge(node1_name,node2_name,edge)
        return g
    else:
        return read_dot_file(file_name)

    


