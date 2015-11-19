###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math
from collections import Counter

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        self.prob_s = {}
        self.prob_s1_s2 = {}
        self.prob_w_s = {}
        self.prob_w = {}

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    #
    def train(self, data):
        all_s = Counter()
        all_ss = Counter()
        all_ws = Counter()
        all_w = Counter()

        for line in data:
            line = zip(*line)
            for word, typ in line:
                all_s[typ] += 1
                all_ws[(word, typ)] += 1
                all_w[word] += 1

            for (w1, t1), (w2, t2) in zip(line, line[1:]):
                all_ss[(t1,t2)] += 1
        all_s_count = sum(all_s.values())
#	import pdb;pdb.set_trace()
        all_w_count = sum(all_w.values())
        self.prob_w = {k: v/float(all_w_count) for k,v in all_w.iteritems()}
        self.prob_s = {k: v/float(all_s_count) for k,v in all_s.iteritems()}
        self.prob_s1_s2 = {(t1,t2):float(v)/all_s[t1] for (t1, t2), v in all_ss.iteritems()}
        self.prob_w_s = {(w,t):float(v)/all_s[t] for (w,t), v in all_ws.iteritems()}

        self.prob_s_w1 = {(t,w):float(v)/all_w[w] for (w,t), v in all_ws.iteritems()}
        self.prob_s_w2 = {(t,w):(v * self.prob_s[t]) / self.prob_w[w]
                             for (w,t), v in self.prob_w_s.iteritems()}
        print "----"
	print [x for x in self.prob_s_w2 if 
                        int(self.prob_s_w1[x]*1000) != int(self.prob_s_w2[x]*1000)][:10]
	print "---"
    # Functions for each algorithm.
    #
    def naive(self, sentence):
	print "Naive------------------"
        return [ [ [ "noun" ] * len(sentence)], [] ]

    def mcmc(self, sentence, sample_count):
	dict=[]
	temp_dict={}
	for i in range(0,len(sentence)):
		temp_dict[i]=self.prob_s.keys()[random.choice(range(0,len(self.prob_s)))] 
	dict.append(temp_dict)
	for sample in range(1,sample_count-1):
		prev_sample=dict[sample-1]
		next_dict={}
		for i in range(0,len(sentence)):
			next_dict[i]=
	return [ [ temp_dict ] * sample_count, [] ]

    def best(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]

    def max_marginal(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

    def viterbi(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 5)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print "Unknown algo!"

