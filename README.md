# CFG_Solver

Provide mutiliple solutions for CFG Reachability Problem

## File Input

### Graph:

Dot file(as demo/simple_dot_example.dot.dot)
or simple suggestive txt(as demo/simple_txt_example 1.txt in demo, each line node,node,label)
Grammar:
suggestive txt(as demo/simple_grammar_example.dot in demo,' 'space separete, ; delimite except last line)

demo ( contain simple example input )
generated_file( contain dot file and png)

# current working

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
