#!python3
import sys

from graph import Graph
from grammar import grammar
from solver import Solver

arg = ['demo/100KB.dot','demo/VM_Grammar.txt','Matrix','Cubic']

for i in range(1, len(sys.argv)):
    arg[i-1] = sys.argv[i]    

graph = Graph(arg[0],arg[2])
grammar = grammar(arg[1])
solver = Solver(arg[3])

solver.solve(graph, grammar)
print(f"The result of graph:{arg[0]} for grammar:{arg[1]} in DS:{arg[2]} by {arg[3]} algo has dump in {arg[0]}_solved")

