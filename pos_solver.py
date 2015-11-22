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
from bisect import bisect
import math
from collections import Counter, defaultdict

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
        self.prob_start_s = {}

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
        start_s = Counter()

        for index, line in enumerate(data):
            line = zip(*line)
            for word, typ in line:
                all_s[typ] += 1
                all_ws[(word, typ)] += 1
                all_w[word] += 1

            for (w1, t1), (w2, t2) in zip(line, line[1:]):
                all_ss[(t1,t2)] += 1
            start_s[line[0][1]] += 1

        all_s_count = sum(all_s.values())
        start_s_count = sum(start_s.values())
        all_w_count = sum(all_w.values())

        self.prob_w = {k: v/float(all_w_count) for k,v in all_w.iteritems()}
        self.prob_s = {k: v/float(all_s_count) for k,v in all_s.iteritems()}
        self.prob_s1_s2 = {(t1,t2):float(v)/all_s[t1] for (t1, t2), v in all_ss.iteritems()}
        self.prob_w_s = {(w,t):float(v)/all_s[t] for (w,t), v in all_ws.iteritems()}

        self.prob_s_w1 = {(t,w):float(v)/all_w[w] for (w,t), v in all_ws.iteritems()}
        self.prob_s_w2 = {(t,w):(v * self.prob_s[t]) / self.prob_w[w]
                             for (w,t), v in self.prob_w_s.iteritems()}

        self.prob_start_s = {t: v/float(start_s_count) for t,v in start_s.iteritems()}

        print "----"
        print [x for x in self.prob_s_w2 if 
                        int(self.prob_s_w1[x]*1000) != int(self.prob_s_w2[x]*1000)][:10]
        print "---"

    # Functions for each algorithm.
    #
    def naive(self, sentence):
        res = [max([s for s in self.prob_s.keys()], key=lambda x: self.prob_s_w1.get((x, w), 0)) for w in sentence]
        return [[res], []]

    def mcmc(self, sentence, sample_count):
      #  return [ [ ["noun"] * len(sentence) ] * sample_count, [] ]
        dict=[]
        temp_dict={}
        for i in range(0,len(sentence)):
            temp_dict[i]=self.prob_s.keys()[random.choice(range(0,len(self.prob_s)))] 
        dict.append(temp_dict)
        for sample in range(1,sample_count):
            prev_sample= dict[sample-1]
            next_sample={}
            for i in range(0,len(sentence)):
                if sentence[i] not in self.prob_w:
                    next_sample[i]="noun"
                    self.prob_w_s
                elif i == 0:
                    next_sample[i] = self.calc_weight(1,sentence[i],prev_sample[i+1])
                elif i == len(sentence)-1:
                    next_sample[i] = self.calc_weight(prev_sample[i-1],sentence[i],1)
                else:
                    next_sample[i] = self.calc_weight(prev_sample[i-1],sentence[i],prev_sample[i+1])
            dict.append(next_sample)
        return [ dict[1920:], [] ]

    def calc_weight(self,prev_sample,word,next_sample):
        #import pdb;pdb.set_trace()
        available_choices = []
        for speech in self.prob_s.keys():
            if prev_sample == 1:
                value = self.prob_w_s.get((word,speech),self.calc_dummy_word(word,speech))*self.prob_s1_s2.get((next_sample,speech),self.calc_dummy(next_sample,speech))
            elif next_sample == 1:
                value = self.prob_w_s.get((word,speech),self.calc_dummy_word(word,speech))*self.prob_s1_s2.get((speech,prev_sample),self.calc_dummy(speech,prev_sample))
            elif prev_sample !=1 and next_sample != 1:
                value = self.prob_w_s.get((word,speech),self.calc_dummy_word(word,speech))*self.prob_s1_s2.get((next_sample,speech),self.calc_dummy(next_sample,speech))*self.prob_s1_s2.get((speech,prev_sample),self.calc_dummy(speech,prev_sample))
            available_choices.append([speech,value])
        return self.weightedChoice(available_choices)
    def calc_dummy(self,next_sample,speech):
            value = self.prob_s1_s2.get((speech,next_sample),0)*self.prob_s.get((next_sample),0)/self.prob_s.get((speech),0)
            return value
    def calc_dummy_word(self,word,speech):
            value = self.prob_s_w1.get((speech,word),0)*self.prob_w.get((word),0)/self.prob_s.get((speech),0)
            return value
    def weightedChoice(self,choices):
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
                total += w
                cum_weights.append(total)
        x = random.random()*total
        i = bisect(cum_weights, x)
        return values[i]

    def best(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]

    def max_marginal(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

    def viterbi(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]
        l = math.log
        t1 = defaultdict(dict)
        t2 = defaultdict(dict)
        t = len(sentence)
        MIN = 0.00001

        all_states = self.prob_s.keys()
#        import pdb; pdb.set_trace()
        for i, s in enumerate(all_states):
            t1[i][0] = l(self.prob_start_s.get(s, MIN)) + \
                            l(self.prob_w_s.get((sentence[0], s), MIN))
            t2[i][0] = 0

        for i in range(1,t):
            for j, s in enumerate(all_states):
                maxItem = (-1e10, -1)
                for k, new_state in enumerate(all_states):
                    prevProb = t1[k][i-1]
                    transProb = self.prob_s1_s2.get((new_state, s), MIN)
                    emissProb = self.prob_w_s.get((sentence[j], s), MIN)
                    curProb = prevProb + l(transProb) + l(emissProb)
                    curItem = curProb, k
                    if curItem > maxItem:
                        maxItem = curItem
                t1[j][i], t2[j][i] = maxItem
        print t1
        print t2

        z = [0] * t
        z[t-1] = max(range(len(all_states)), key=lambda k: t1[k][len(sentence)-1])
        result = [all_states[z[t-1]]]
        for i in range(t-1, 0, -1):
            z[i-1] = t2[z[i]][i]
            result = [all_states[z[i-1]]] + result

        return [[result], []]


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
            return self.mcmc(sentence, 2000)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print "Unknown algo!"

