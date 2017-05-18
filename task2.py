import lab4, math
#(1) Load initial parameters from initial_probs.txt into a dictionary of the form d[spanish-word][english-word] = P(english-word|spanish-word)
def load_init():
	"""Load probabilities from initial_probs.txt into a dictionary."""
	d = {}
	f = open('initial_probs.txt')
	for line in f:
		s, e, p = line.strip().split('\t')
		if not s in d: d[s] = {}
		d[s][e] = float(p)
	f.close()
	return d

#(2) Load the data, i.e. phrase pairs from phrase_pairs.txt
def load_data():
	"""Load data from phrase_pairs.txt into a list."""
	phrase_pairs = []
	f = open('phrase_pairs.txt')
	for line in f:
		s, e = line.strip().split('\t')
		s = s.strip().split()
		e = e.strip().split()
		phrase_pairs.append((s, e))
	f.close()
	return phrase_pairs
#(3) Implement a function that estimates P(alignment|english, spanish) for each possible alignment for a given english-spanish phrase pair:
#(3-1) function arguments:
#(i) al: output from the alignment function(a list of lsts of word index pairs)
#(ii) e: the english phrase as a list of words
#(iii) s: the spanish phrase as a list of words
#(iv)d: the probability dictionary (e.g. the initial probs from (1))

#(3-2) psuedocode
#p_list = []
#for each alignment in al:
#	p_ae = 1.0 # P(a,e|s)
#	for each word_pair in each alignment: (indices)
#	 look up the work translation probability in d
# 	and multiply it to p_ae
#p_list.append(p_ae)
# sum the probabilities in p_list # P(*, e|s)
# divide the probabilities in p_list by the sum # p(a|e, s)
#(3-3) returns:
# p_list containing P(a|e,s)
def E (al, e, s, d):
	p_list = []
	for each_alignment in al:
		p_ae = 1.0
		for i, j  in each_alignment:
			p_ae *= d[s[i]][e[j]]
		p_list.append(p_ae)
	t = sum(p_list)
	for i in range(len(p_list)):
		p_list[i] /=t
	return p_list #pp #P of data point

#(4) Implement a function the updates a dict of (spanish-word, english-word) counts for each phrase-pair using the probabilities from (3) as fractional counts.

#(4-1) Arguments:
#(i) al: output from the alignment function (a list of lists of word index pairs)
# (ii) p_list: from (3)
# (iii) e: the english phrase as a list of words
# (iv) s: the spanish phrase as a list of words
#(v) fd: a frequency dict for the form fd[span][eng] = c(span,word) thus far

def M (al, p_list, e, s, fd):
	for k in range(len(al)):
		count = p_list[k] #corresponding word in p_list
		for i, j in al[k]:# for each word pair in each alignment
			fd[s[i]][e[j]] += count #increase frequency count
	return fd

#(5) Repeat E-M (followed by normalization) a lot.
#(5-1) Write a function the defines a single cycle of E-M
def EM (phrase_pairs, d):
	fd = {}
	lld = 0.0 #log liklihood of data
	for s in d:
		fd[s] = {}
		for e in d[s]:
			fd[s][e] = 0.0
	for s, e in phrase_pairs:
		al = lab4.exhaust_align(s,e) # use from lab 4 function that sets up alignment indices
		p_list = E(al, e, s, d)
		#pp = E(al, e, s, d)
		fd = M(al, p_list, e, s, fd)
		#lld += math.log(pdp)
	pd = {} #new word translation probabilities
	for s in fd:
		pd[s] = {}
		t = sum(fd[s].values()) #e.g c(*, s|la)
		for e in fd[s]:
			pd[s][e] = fd[s][e] / t
	return pd, lld

if __name__ == '__main__':
	d = load_init()
	print d['resto'] # before running EM
	phrase_pairs = load_data()
	prev_lld = -1e100
	threshold = 0.01
#Repeat EM 100 times
	for i in range(100):
		d,lld = EM(phrase_pairs, d)
		diff_lld = lld-prev_lld
		if diff_lld < threshold:
			break
		prev_lld = lld
	print i # the num of iterations
	print d['resto'] # after running EM
# Do it, run it, see what happens



