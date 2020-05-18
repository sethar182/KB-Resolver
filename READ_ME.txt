Hello, thanks for your interest in my code!

This goal of this project was to create an automated way of verifying
whether or not a logical sentence is entailed by a knowledge base. In other
words, I want to be able to know if a statement in the conjunctive normal
form holds true for every model of a knowledge base. This is done using
the resolution rule.

To run the program, I use python in the command line. A valid example is:
	py main3.py task1.in
	py main3.py anyInputFileInFolder.in
The input file is a simple text file that specifies the knowledge base
in the first N-1 lines, and the statement to be verified on the Nth line.
The program will output each resolution to the command line in the CNF
with brackets at the end of the line to indicate which lines were resolved
in the knowledge base.

The file tree.py is a simple data structure I created to determine if a
sentence already exists in the knowledge base. By using a tree structure
with each node representing a literal in the sentence, the statement
can be analyzed in O(log(N)) time, rather than O(N) time (where N is the
length of the knowledge base).