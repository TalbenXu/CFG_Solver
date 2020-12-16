# Read all to as tuple in list
import re
production = []
with open('demo/simple_EBNF_example.txt', 'r') as f:
    # get production rule part get more familiar with grammar_read
    for line in f.readlines():
        if 