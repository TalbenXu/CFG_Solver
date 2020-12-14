# for simpilicity only read the essential part of the dot file
# the essential part of the dot file means all the informaiton can be read from the my text format
import re
from class_graph import *

def read_dot_file(filename):
    edge_pattern = re.compile(r'(\w+)\s*->\s*(\w+)\s*\[.*label="(.*)"')
    node_pattern = re.compile(r'(\w+)')
    with open(filename, 'r') as f:
        g = Graph()
        lines = f.readlines()
        line_1 = lines[0]
        line_2 = lines[-1]
        line_1 = line_1.split('{')[1]
        line_2 = line_2.split('}')[0]
        lines[0] = line_1
        lines[-1] = line_2
        for line in lines:
            if ('=' in line and "[" in line) or ("=" not in line and "[" not in line):
                if "->" in line:
                    match = edge_pattern.search(line)
                    if match != None:
                        node_1, node_2, label = match.group(1), match.group(2), match.group(3)
                        node_i1 = Vertex(node_1)
                        node_i2 = Vertex(node_2)
                        g.add_vertex(node_i1)
                        g.add_vertex(node_i2)
                        g.add_edge(node_1,node_2,label)
                else:
                    match = node_pattern.search(line)
                    if match != None:
                        node = match.group(1)
                        node_i = Vertex(node)
                        g.add_vertex(node_i)
    return g



                    


