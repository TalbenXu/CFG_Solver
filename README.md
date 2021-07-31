# CFG_Solver

Aim: Provide mutiliple solutions for CFG Reachability Problem

## File Input

Provide to the CFGR.py file arg[[Dot input], [Grammar Txt], [Matrix(data structure), [Cubic(work list Algorithm])]

### Graph:

Dot file(as demo/mini.dot.dot)
or simple suggestive txt(as demo/mini 1.txt in demo, each line node,node,label)
Grammar:
suggestive txt(as demo/simple_grammar_example.dot in demo,' 'space separete, ; delimite except last line)

demo ( contain simple example input )
generated_file( contain dot file and png)

(Grammar Solver will do)
Turn EBNF to Normal Form
Algorithm:

1. convert \* to X = XE | e
2. convert ? to X = E | e
3. Bin transformation

EBNF: Representation Rule

Terminals:  
   dbar d abar a  
Variables:  
   M V  
Start:  
   M  
Productions:  
   M -> dbar V d;  
   V -> ( M ? abar ) \* M ? ( a M ?)

# Current Working:  
 Currently speed is low, next step while abstract the ds_structure and solver and adjust the internal representation

the idea file structure
input(dir)(five dot file 1MB 2MB 4MB 8MB 16MB)
output(dir) (dot source)

CFGR.py (driver program using certain combination of solver and structure)
solver.py (overall class containing differenct instance)
graph.py( overall class containing different graph)
grammar.py (turn CFG to caronical form)

Goal:
for 1MB file speed need to be at 2mins
for 2MB file speed need to be at 8mins
for 4MB file speed need to be at 10hrs
for 8MB file speed need to run at cloudlab (in cubic time complexity)
for 16MB file speed need to run at cloudlab (in cubic time complexity)

1. Two matrix predecesesor decenser ( or other structure good in certain usage add lookup)
2. Numpy or Tenserflow optimzation 
3. Cython using compile method
4. cloud run


