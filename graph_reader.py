# Graph Reader for graph txt file 
# into memory and display

# text file format in each line represent a directed edge
# like "1,2,a"
# 1 outbound node, 2 inbound node, with label a edge

# memory representation using adjeceny list
# assume graph is not dense

# display using pydot 

# File Reading get the file Object
# for simpilicity only read the essential part of the dot file
# the essential part of the dot file means all the informaiton can be read from the my text format
import re
from class_graph import *

def read_dot_file(filename):
    edge_pattern = re.compile(r'(\w+)\s*->\s*(\w+)\s*\[.*color=(.*)\]')
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
                        if label == "red":
                            label = 'd'
                            g.add_edge(node_2,node_1,label+'bar')
                        elif label == "black" or label == "purple":
                            label = 'a'
                            g.add_edge(node_2,node_1,label+'bar')
                        g.add_edge(node_1,node_2,label)
                else:
                    match = node_pattern.search(line)
                    if match != None:
                        node = match.group(1)
                        node_i = Vertex(node)
                        g.add_vertex(node_i)
    return g

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

    


