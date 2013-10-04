# cython: profile=True

from __future__ import division
import cython
cimport cython
import collections
import multiprocessing
from multiprocessing import Pool
import numpy as np
cimport numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import sys

from cpython cimport bool

def order_a(dict a):
	cdef list x, y
	cdef unsigned k, v
	x = []
	y = []
	for k,v in collections.OrderedDict(sorted(a.items())):
		x.append(k)
		y.append(v)
	return x, y

def get_normal01(double m, double s):
	cdef double x
	x = np.random.normal(m,s,1)
	while x > 1.0 or x < 0.0:
		x = np.random.normal(m,s,1)
	return x

def get_weibull01(double m=10):
	cdef double x
	x = np.random.weibull(m,1)
	while x > 1.0 or x < 0.0:
		x = np.random.weibull(m,1)
	return x

def run_simulation(list input):
	cdef unsigned int size, n_of_trials, trial, i
	cdef list competition_features, output
	cdef double ceiling, std
	cdef Challenge clg

	size = input[0]
	n_of_trials = input[1]
	competition_features = input[2]
	n_of_participants = competition_features[0]
	ceiling = competition_features[1]
	std = competition_features[2]
	if not size:
		return [0,[0]*(n_of_participants)]
	else:
		print "Computing size", size
		output = [0] * (n_of_participants)
		for trial in range(0,n_of_trials):	# trials
			clg = Challenge(n_of_participants, size, ceiling, std)
			for i in range(0,n_of_participants):
				if clg.expected_ranking[:i] == clg.simulated_ranking[:i]:
					output[i] += 1
		print "Finished size", size
		return [size, output]

cdef class Participant:

	cdef bytes ID
	cdef double avg_performance, avg_deviation, result
	cdef unsigned int n_of_samples

	def __init__(self, int ID, double avg_performance, double avg_deviation, unsigned int n_of_samples):
		self.ID = str(ID)
		self.avg_performance = avg_performance
		self.avg_deviation = avg_deviation
		self.n_of_samples = n_of_samples
		self.result = np.mean(np.random.binomial(n_of_samples, get_normal01(avg_performance, avg_deviation), n_of_samples)) / n_of_samples

	def __str__(self):
		return "{" + self.ID + ", " + str(self.avg_performance) + ", " + str(self.avg_deviation) + " | F1:" + str(round(self.result,4)) + "}"

cdef class Challenge:

	cdef unsigned int n_of_samples
	cdef double expected_variation_in_each_system
	cdef list participants, expected_ranking, simulated_ranking

	def __init__(self, unsigned int n_of_participants, unsigned int n_of_samples, double ceiling, double std):
		self.n_of_samples = n_of_samples
		self.expected_variation_in_each_system = std
		self.participants = [Participant(ID, get_weibull01(10)*ceiling, self.expected_variation_in_each_system, n_of_samples) for ID, p in enumerate(range(0, n_of_participants))]
		self.expected_ranking = [p.ID for p in sorted(self.participants, key=lambda participant:participant.avg_performance)]
		self.simulated_ranking = [p.ID for p in sorted(self.participants, key=lambda participant:participant.result)]

	def __str__(self):
		return str(self.participants) + "participants. " + str(self.n_of_samples) + " samples in the benchmark test set."

cdef class ChallengesSimulator:

	cdef unsigned int start, end, step, n_of_participants, n_trials
	cdef double top_score, std
	cdef list results

	def __init__(self, list range_of_sample_size=[1,3000,50], int n_of_trials=100, list competition_features=[21, 0.86, 0.0005], bool verbose=False):
		cdef unsigned int n_of_processes
		cdef list tasks

		self.start = range_of_sample_size[0]
		self.end = range_of_sample_size[1]
		self.step = range_of_sample_size[2]
		self.n_of_participants = competition_features[0]
		self.top_score = competition_features[1]
		self.std = competition_features[2]
		self.n_trials = n_of_trials
		n_of_processes = multiprocessing.cpu_count()*2
		tasks = [[size, n_of_trials, competition_features] for size in xrange(self.start,self.end,self.step)]
		pool = Pool(processes=n_of_processes)
		result = pool.map(run_simulation, tasks)
		self.results = dict(result)

	def show(self):
		cdef list x, y
		cdef unsigned int i
		cdef dict data
		if len(self.results) == 0:
			print 'No results.'
		else:
			x, y = order_a(self.results)

			# Plotting
			fig = plt.figure()
			ax = plt.subplot(111)
			colours = [plt.get_cmap('jet')(float(i)/(self.n_of_participants-1)) for i in range(0,self.n_of_participants)]
			random.shuffle(colours)
			for i in range(0,self.n_of_participants):
				color = colours[i]
				current_y = [n[i]/self.n_trials for n in y]
				data = dict()
				for id, e in enumerate(x): data[e] = current_y[id]
				data = collections.OrderedDict(sorted(data.items()))
				plt.plot(data.keys(), data.values(), '-', c=color, label='Top '+str(i+1))

			plt.xlabel('Test set size')
			plt.ylabel('p of expected rankings')
			plt.title('Challenge simulator ['+str(self.n_of_participants)+', '+str(self.top_score)+', '+str(self.std)+']')
			plt.xlim([0, self.end])
			plt.ylim([0, 1])
			plt.xticks(range(self.start,self.end+(self.step-1), self.step*2))
			plt.yticks(np.arange(0,1.01,0.1))
			plt.grid(True)
			ax.legend(loc=4)
			plt.show()

def main():
	cdef ChallengesSimulator tempEval3_sim

	tempEval3_sim = ChallengesSimulator(range_of_sample_size=[0,4000,25], n_of_trials=3000, competition_features=[21, 0.748, 0.0005], verbose=True)
	pickle.dump(tempEval3_sim, open('dump.dat','w'))
	tempEval3_sim.show()

	#tempEval3 = Competition(21, 2000000, 0.7, 0.0)
	#for p in tempEval3.participants:
	#	print p


if __name__=="__main__":
	main()