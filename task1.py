'''Implement an algorithm that calcluates edit distance between two strings
(1) Remember to prefix each string with a null symbol (e.g. as -> #as)
(2) Implement the table as a 2D list (list inside a list)
NB: In class, the table went from bottom left to top-right
Here, imagine it goes from top left to bottom right
(2-1) Each (sub-) list is a row in the table
(2-2) Initialize each row with zeros
(2-3) Converting the lists into numpy.arrays makes things a bit easier

(3) Update the first row: 0, 1, 2, ...
(4) Update the first column: 0, 1, 2, ..

(5) For other cells, say table[i, j]
table[i,j] = minimum of the following three alternatives:
(i) table [i -1, j-1] + sub(y[i] , x[j]) where sub = 1 if different, sub= 0 if same where x and y are the two strings(x) is column. (y) is row
(ii) table [i -1, j] +1
(iii) table [i, j - 1] + 1
(6) return the value in the bottom right cell'''

import sys, numpy

def med(x, y):
	x = '#'+x
	y = '#'+y
	lx = len(x)
	ly = len(y)
	table = []
	for i in range(ly): # need as many rows as number of letters in y
		zeros = [0]*lx
		table.append(zeros)
	for i in range(1, lx):
		table[0][i] = table[0][i-1] + 1 #look to the prev value and add 1
	for i in range(1, ly):
		table[i][0] = table[i-1][0] + 1
	for i in range(1, ly): # different rows
		for j in range(1, lx): # different columns
			sub = table[i-1][j-1] + int(y[i] != x[j]) #boolean into integer check if same
			ins = table[i-1][j] + 1
			dlt = table[i][j-1] + 1
			cost = min([sub, ins, dlt])
			table[i][j] = cost
	print table
	return table[ly-1][lx-1]

def med_numpy(x, y):
	x = '#'+x; lx = len(x)
	y = '#'+y; ly = len(y)
	table = numpy.zeros( (ly, lx) )
	table[0, :] = numpy.linspace(0, lx-1, lx)
	table[:, 0] = numpy.linspace(0, ly-1, ly)
	for i in range(1, ly):
		for j in range(1, lx):
			sub = table[i-1, j-1] + int(y[i] != x[j])
			ins = table[i-1, j] + 1
			dlt = table[i, j-1] + 1
			table[i, j] = min([sub, ins, dlt])
	print table
	return table[ly-1, lx-1]

if __name__ == '__main__':
	x, y = sys.argv[1:3]
#	print med(x, y)
	print med_numpy(x, y)
