class Node:
	def __init__(self, data):
		self.children = []
		self.data = data

	def printNode(self):
		outString = ''
		for c in self.children:
			outString += '[' + c.data + '] '
		print('{}: {}'.format(self.data, outString.rstrip(' ')))

	def getChild(self, data):
		# returns specific child based on contents
		for c in self.children:
			if c.data == data:
				return c
		return '-1'

	def getChildrenData(self):
		# returns list of children's data
		dataList = []
		for c in self.children:
			dataList.append(c.data)
		return dataList

	def notInChildren(self, atom):
		# returns True/False if children is in self's children
		for c in self.children:
			if c.data == atom:
				return False
		return True

	def insert(self, clause):
		# receives list of strings sep by space
		currNode = self
		for atom in clause:
			# if atom not in currNode.getChildrenData():
			if currNode.notInChildren(atom):
				currNode.children.append(Node(atom))
				currNode = currNode.getChild(atom)
			else:
				currNode = currNode.getChild(atom)
		# mark end of clause, it exists at this level
		currNode.children.append(Node('end'))

	def containsClause(self, clause):
		# returns True/False if clause exists in tree
		# must be passed the root node, returns true if all atoms
		# traversed and 'end' exists at that level

		currNode = self
		for atom in clause:
			if currNode.notInChildren(atom):
				return False
			else:
				currNode = currNode.getChild(atom)

		if currNode.notInChildren('end'):
			return False
		else:
			return True
