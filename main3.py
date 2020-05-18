"""
Main knowledge base reasoning solver
"""
import sys
import time
from tree import Node

def negateAtom(atom):
	"""
	Negates a single atom
	"""

	if '~' in atom:
		atom = atom.strip('~')
	else:
		atom = '~' + atom

	return atom

def notInKB(clause, kb):
	"""
	Determines if the clause or its logical equivalent is already in the kb
	"""

	# check if ordered contents of clause equivalent to another in kb
	sclause = sorted(clause)
	for clause2 in kb:
		if sclause == sorted(clause2):
			return False

	return True

def generateClause(kb, cl1, cl2, atom, root):
	"""
	Generates new clause by removing atom from clause 1 (cl1) and
	its negation from clause 2 (cl2). Checks for redundant literals,
	and if clause evaluates to true (contains a and ~a)
	"""

	# adds non-redundant literals to clause
	clause = cl1.copy()
	clause.remove(atom)
	for literal in cl2:
		if literal not in clause:
			clause.append(literal)
		# check if clause evaluates to true
		if negateAtom(literal) in clause:
			return []
	clause.remove(negateAtom(atom))

	# clause valid, but is it in kb?
	if root.containsClause(sorted(clause)):
		return []
	else:
		root.insert(sorted(clause))
		return clause

def contraExists(atomi, atomj):
	"""
	Determines if contradiction exists between given literals/atoms
	"""

	# negate atom i and compare to atom j
	if negateAtom(atomi) == atomj:
		return True
	else:
		return False

def resolution(kb, iter, root):
	"""
	Find two clauses to use resolution (~a V b... and a V c...)
	repeat until unable to produce clauses (fail, False),
	or contradiction is produced (a and ~a chosen, valid, True)
	"""

	# for each clause i, 1...n
	for i, clausei in enumerate(kb):
		# for each previous clause j, 1...i
		for j in range(i):
			clausej = kb[j]
			# if clauses i and j are single atoms, check for contradiction
			if len(clausei) == 1 and len(clausej) == 1:
				if contraExists(clausei[0], clausej[0]):
					print('{}. Contradiction {{{}, {}}}'.format(iter, i+1, j+1))
					return True
			else:
				# compare clause i and j, check for opposing literals
				for atomi in clausei:
					if negateAtom(atomi) in clausej:
						# generate new clause from i and j
						newClause = generateClause(kb, clausei, clausej, atomi, root)
						# if valid clause generated, add to kb
						if len(newClause) > 0:
							kb.append(newClause)
							print('{}. {} {{{}, {}}}'.format(iter,
						 		' '.join(newClause).rstrip(' '), i+1, j+1))
							iter += 1

	# no contradiction, no more clauses in kb
	return False

def negate(clause):
	"""
	Negates CNF clause using DeMorgan's Law, returns literal
	or list of literals to be added to knowledge base
	"""

	# negate each atom
	for i, a in enumerate(clause):
		clause[i] = [negateAtom(a)]

	# return atoms, add each to kb
	return clause

def solve(arg):
	"""
	Main solving function
	"""

	# read in all cnf clauses to knowledge base
	inFile = open(arg, 'r')
	kb = []
	for cnf in inFile:
		kb.append(cnf.strip('\n').split(' '))
	inFile.close()

	# define clause to be tested
	clause = kb.pop(len(kb) - 1)

	##### resolution rule #####

	# negate clause, apply DeMorgan's Law
	literals = negate(clause)

	# add literals of negated clause to kb
	for l in literals:
		kb.append(l)

	# create tree to search for existing clauses
	root = Node('root')

	# print current kb
	iter = 1
	for c in kb:
		print('{}. {} {{}}'.format(iter, ' '.join(c).rstrip(' ')))
		root.insert(sorted(c))
		iter += 1

	# perform resulution on knowledge base
	success = resolution(kb, iter, root)
	#print(root.containsClause(test))

	return success

if __name__ == '__main__':
	"""
	Main function called when 'kbsolver.py' is called
	from the command line.
	"""

	# validate argument length
	if len(sys.argv) < 2:
		raise Exception("No input file specified.")
	if len(sys.argv) > 2:
		raise Exception("Too many arguments found.")

	# validate file type
	inFile = sys.argv[1]
	inFileSep = inFile.split('.')
	if inFileSep[len(inFileSep)-1] != 'in':
		raise Exception('Input file is an invalid file type (must be .in). Inputted:', inFile)

	# pass file name to solver
	start_time = time.time()
	solution = solve(inFile)

	# print valid if solution == true
	if solution:
		print('Valid')
	else:
		print('Fail')

	print("--- %s seconds ---" % (time.time() - start_time))

	pass
