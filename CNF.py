"""
G in this form:
start symble: first line
production rules: other line

example:
A
A = a
"""
# -*- coding: utf-8 -*-
#IT's assumed that starting variable is the first typed
import sys
import re
import itertools

left, right = 0, 1

K, V, Productions = [],[],[]
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]


left, right = 0, 1

def union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list

def loadModel(modelPath):
	file = open(modelPath).read()
	K = (file.split("Variables:\n")[0].replace("Terminals:\n","").replace("\n",""))
	V = (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n","").replace("\n",""))
	P = (file.split("Productions:\n")[1])

	return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)
#Make production easy to work with
def cleanProduction(expression):
	result = []
	#remove spaces and explode on ";"
	rawRulse = expression.replace('\n','').split(';')
	
	for rule in rawRulse:
		#Explode evry rule on "->" and make a couple
		leftSide = rule.split(' -> ')[0].replace(' ','')
		rightTerms = rule.split(' -> ')[1].split(' | ')
		for term in rightTerms:
			result.append( (leftSide, term.split(' ')) )
	return result

def cleanAlphabet(expression):
	return expression.replace('  ',' ').split(' ')

def seekAndDestroy(target, productions):
	trash, ereased = [],[]
	for production in productions:
		if target in production[right] and len(production[right]) == 1:
			trash.append(production[left])
		else:
			ereased.append(production)
			
	return trash, ereased
 
def setupDict(productions, variables, terms):
	result = {}
	for production in productions:
		#
		if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
			result[production[right][0]] = production[left]
	return result


def rewrite(target, production):
	result = []
	#get positions corresponding to the occurrences of target in production right side
	#positions = [m.start() for m in re.finditer(target, production[right])]
	positions = [i for i,x in enumerate(production[right]) if x == target]
	#for all found targets in production
	for i in range(len(positions)+1):
 		#for all combinations of all possible lenght phrases of targets
 		for element in list(itertools.combinations(positions, i)):
 			#Example: if positions is [1 4 6]
 			#now i've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
 			#erease position corresponding to the target in production right side
 			tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
 			if tadan != []:
 				result.append((production[left], tadan))
	return result

def dict2Set(dictionary):
	result = []
	for key in dictionary:
		result.append( (dictionary[key], key) )
	return result

def pprintRules(rules):
	for rule in rules:
		tot = ""
		for term in rule[right]:
			tot = tot +" "+ term
		print(rule[left]+" -> "+tot)

def prettyForm(rules):
	dictionary = {}
	for rule in rules:
		if rule[left] in dictionary:
			dictionary[rule[left]] += ' | '+' '.join(rule[right])
		else:
			dictionary[rule[left]] = ' '.join(rule[right])
	result = ""
	for key in dictionary:
		result += key+" -> "+dictionary[key]+"\n"
	return result

def isUnitary(rule, variables):
	if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
		return True
	return False

def isSimple(rule):
	if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
		return True
	return False


for nonTerminal in V:
	if nonTerminal in variablesJar:
		variablesJar.remove(nonTerminal)

#Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def START(productions, variables):
	variables.append('S0')
	return [('S0', [variables[0]])] + productions
#Remove rules containing both terms and variables, like A->Bc, replacing by A->BZ and Z->c–––––––––––TERM
def TERM(productions, variables):
	newProductions = []
	#create a dictionari for all base production, like A->a, in the form dic['a'] = 'A'
	dictionary = setupDict(productions, variables, terms=K)
	for production in productions:
		#check if the production is simple
		if isSimple(production):
			#in that case there is nothing to change
			newProductions.append(production)
		else:
			for term in K:
				for index, value in enumerate(production[right]):
					if term == value and not term in dictionary:
						#it's created a new production vaiable->term and added to it 
						dictionary[term] = variablesJar.pop()
						#Variables set it's updated adding new variable
						V.append(dictionary[term])
						newProductions.append( (dictionary[term], [term]) )
						
						production[right][index] = dictionary[term]
					elif term == value:
						production[right][index] = dictionary[term]
			newProductions.append( (production[left], production[right]) )
			
	#merge created set and the introduced rules
	return newProductions

#Eliminate non unitry rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def BIN(productions, variables):
	result = []
	for production in productions:
		k = len(production[right])
		#newVar = production[left]
		if k <= 2:
			result.append( production )
		else:
			newVar = variablesJar.pop(0)
			variables.append(newVar+'1')
			result.append( (production[left], [production[right][0]]+[newVar+'1']) )
			i = 1
#TODO
			for i in range(1, k-2 ):
				var, var2 = newVar+str(i), newVar+str(i+1)
				variables.append(var2)
				result.append( (var, [production[right][i], var2]) )
			result.append( (newVar+str(k-2), production[right][k-2:k]) ) 
	return result
	

#Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def DEL(productions):
	newSet = []
	#seekAndDestroy throw back in:
	#        – outlaws all left side of productions such that right side is equal to the outlaw
	#        – productions the productions without outlaws 
	outlaws, productions = seekAndDestroy(target='e', productions=productions)
	#add new reformulation of old rules
	for outlaw in outlaws:
		#consider every production: old + new resulting important when more than one outlaws are in the same prod.
		for production in productions + [e for e in newSet if e not in productions]:
			#if outlaw is present in the right side of a rule
			if outlaw in production[right]:
				#the rule is rewrited in all combination of it, rewriting "e" rather than outlaw
				#this cycle prevent to insert duplicate rules
				newSet = newSet + [e for e in  rewrite(outlaw, production) if e not in newSet]

	#add unchanged rules and return
	return newSet + ([productions[i] for i in range(len(productions)) 
							if productions[i] not in newSet])

def unit_routine(rules, variables):
	unitaries, result = [], []
	#controllo se una regola è unaria
	for aRule in rules:
		if isUnitary(aRule, variables):
			unitaries.append( (aRule[left], aRule[right][0]) )
		else:
			result.append(aRule)
	#altrimenti controllo se posso sostituirla in tutte le altre
	for uni in unitaries:
		for rule in rules:
			if uni[right]==rule[left] and uni[left]!=rule[left]:
				result.append( (uni[left],rule[right]) )
	
	return result

def UNIT(productions, variables):
	i = 0
	result = unit_routine(productions, variables)
	tmp = unit_routine(result, variables)
	while result != tmp and i < 1000:
		result = unit_routine(tmp, variables)
		tmp = unit_routine(result, variables)
		i+=1
	return result

def STBDU_transformation(modelPath):
	K, V, Productions = loadModel( modelPath )
	Productions = START(Productions, variables=V)
	Productions = TERM(Productions, variables=V)
	Productions = BIN(Productions, variables=V)
	Productions = DEL(Productions)
	Productions = UNIT(Productions, variables=V)
	return Productions

if __name__ == '__main__':
	if len(sys.argv) > 1:
		modelPath = str(sys.argv[1])
	else:
		modelPath = 'model.txt'
	

	print( prettyForm(Productions) )
	print( len(Productions) )
	open('out.txt', 'w').write(	prettyForm(Productions) )



def read_grammar(file_name):
    grammar = dict()
    start_symble, Production = 'S0', grammar_new(file_name)
    print(Production)
    for rule in Production:
        LHS = rule[0]
        RHS = rule[1]
        if LHS not in grammar:
            grammar[LHS] = []
        grammar[LHS].append(RHS)

    # with open(file_name,'r') as f:
    #     lines = f.readlines()
    #     for i in range(len(lines)):
    #         if i == 0:
    #             # Read the first line as start_symble
    #             start_symble = lines[0].strip()
    #             continue
    #         left_symble, right_symble = lines[i].strip().split('=')
    #         right_symble = right_symble.strip()
    #         left_symble = left_symble.strip()
    #         if left_symble not in grammar:
    #             grammar[left_symble] = []
    #         add_up_list = []
    #         for symble in right_symble:
    #             add_up_list.append(symble)
    #         grammar[left_symble].append(add_up_list)
    #         start_symble, grammar = start_transform(start_symble, grammar)
    return start_symble, grammar

# For if RHS of the production contains the start symble
# Initiate the new Variable S0
def start_transform(start_symble, grammar):
    flag = False
    for keys in grammar:
        for rule in grammar[keys]:
            if start_symble in rule:
                flag = True
    if flag == True:
        grammar['S'] = [start_symble]
        start_symble = 'S'
    return start_symble, grammar

def Term_transfomr(start_symble, grammar):
    pass

def grammar_new(file_name):
    return STBDU_transformation(file_name)

    # grammar = dict()
    # with open(file_name, 'r') as f:
    #     for line in f.readlines():
    #         line = line.strip()
    #         key = line.split(' ')[0]
    #         rule = li
    #         grammar[line.split(" ")]
    # pass




