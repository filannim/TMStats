from __future__ import division
import collections
import multiprocessing
from multiprocessing import Pool
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cPickle
import random
random.seed(390)
import sys


def get_normal01(m,s):
	x = np.random.normal(m,s,1)
	while x > 1.0 or x < 0.0:
		x = np.random.normal(m,s,1)
	return x

def get_weibull01(m=10):
	x = np.random.weibull(m,1)
	while x > 1.0 or x < 0.0:
		x = np.random.weibull(m,1)
	return x

def run_simulation(input):
	size, n_of_trials, competition_features = input
	n_of_participants = competition_features[0]
	ceiling = competition_features[1]
	std = competition_features[2]
	if size == 0:
		return [0,[0]*(n_of_participants)]
	else:
		dumper = Dumper()
		dumped = dumper.get(size, n_of_trials, competition_features);
		del dumper
		if dumped:
			print "Dumped size", size
			return [size, dumped]
		else:
			print "Computing size", size
			output = [0] * (n_of_participants)
			for trial in range(0,n_of_trials):	# trials
				clg = Challenge(n_of_participants, size, ceiling, std)
				for i in range(0,n_of_participants):
					if clg.expected_ranking[:i+1] == clg.simulated_ranking[:i+1]:
						output[i] += 1
			print "Finished size", size
			return [size, output]

class Dumper(object):

	def __init__(self):
		with open('temp.mem','r') as source:
			self.db = cPickle.load(source)

	def get(self, size, n_of_trials, competition_features):
		try:
			index = ' '.join([str(size),str(n_of_trials),str(competition_features[0]),str(competition_features[1]),str(competition_features[2])])
			output = self.db[index]
			return output
		except:
			return None

	def store(self, size, n_of_trials, competition_features, output):
		index = ' '.join([str(size),str(n_of_trials),str(competition_features[0]),str(competition_features[1]),str(competition_features[2])])
		self.db[index] = output
			
	def close(self):
		with open('temp.mem','w') as source:
			cPickle.dump(self.db, source)

class Participant(object):

	def __init__(self, ID, avg_performance, avg_deviation, n_of_samples):
		self.ID = ID
		self.avg_performance = avg_performance
		self.avg_deviation = avg_deviation
		self.n_of_samples = n_of_samples
		self.result = np.mean(np.random.binomial(n_of_samples, get_normal01(avg_performance, avg_deviation), n_of_samples)) / n_of_samples

	def __str__(self):
		return "{" + self.ID + ", " + str(self.avg_performance) + ", " + str(self.avg_deviation) + " | F1:" + str(round(self.result,4)) + "}"

class Challenge(object):

	def __init__(self, n_of_participants, n_of_samples, ceiling, std):
		self.n_of_samples = n_of_samples
		self.expected_variation_in_each_system = std
		self.participants = [Participant(str(ID), get_weibull01(10)*ceiling, self.expected_variation_in_each_system, n_of_samples) for ID, p in enumerate(range(0, n_of_participants))]
		self.expected_ranking = [p.ID for p in sorted(self.participants, key=lambda participant:participant.avg_performance)]
		self.simulated_ranking = [p.ID for p in sorted(self.participants, key=lambda participant:participant.result)]

	def __str__(self):
		return str(self.participants) + "participants. " + str(self.n_of_samples) + " samples in the benchmark test set."

class ChallengesSimulator(object):

	def __init__(self, range_of_sample_size=[1,3000,50], n_of_trials=100, competition_features=[21, 0.86, 0.0005], computing_power=2.00, verbose=False):
		self.start = range_of_sample_size[0]
		self.end = range_of_sample_size[1]
		self.step = range_of_sample_size[2]
		self.n_of_participants = competition_features[0]
		self.top_score = competition_features[1]
		self.std = competition_features[2]
		self.n_trials = n_of_trials
		n_of_processes = int(multiprocessing.cpu_count()*computing_power)
		tasks = [[size, n_of_trials, competition_features] for size in xrange(self.start,self.end,self.step)]
		pool = Pool(processes=n_of_processes)
		result = pool.map(run_simulation, tasks)
		self.results = dict(result)

	def store(self):
		if len(self.results) == 0:
			print 'No results.'
		else:
			x = []
			y = []
			dumper = Dumper()
			for k,v in sorted(self.results.iteritems(), key=lambda (k,v): (v,k)):
				x.append(k)
				y.append(v)
				dumper.store(k, self.n_trials, [self.n_of_participants,self.top_score,self.std], v)
			dumper.close()

	def show(self):
		if len(self.results) == 0:
			print 'No results.'
		else:
			x = []
			y = []
			dumper = Dumper()
			for k,v in sorted(self.results.iteritems(), key=lambda (k,v): (v,k)):
				x.append(k)
				y.append(v)
			self.store()

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
			plt.title('Challenge simulator ['+str(self.n_of_participants)+', '+str(self.top_score)+', '+str(self.std)+', '+str(self.n_trials)+']')
			plt.xlim([self.start, self.end])
			plt.ylim([0, 1])
			if int((self.end-self.start)/20) >= 1:
				plt.xticks(range(self.start,self.end+(self.step-1), int((self.end-self.start)/20)))
			else:
				plt.xticks(range(self.start,self.end+(self.step-1), 1))
			plt.yticks(np.arange(0,1.01,0.05))
			plt.grid(True)
			ax.legend(loc=4,prop={'size':10})
			plt.show()

def main():
	
	start, end, step, trials, participants = [int(inp) for inp in sys.argv[1:6]]
	ceiling, std = [float(inp) for inp in sys.argv[6:8]]
	computing_power = float(sys.argv[8])
	c = ChallengesSimulator([start, end, step], trials, [participants, ceiling, std], computing_power)
	c.show()

	#tempEval3_sim = ChallengesSimulator(
	#	range_of_sample_size=[0,5000,25], 
	#	n_of_trials=10000, 
	#	competition_features=[21, 0.748, 0.0005], 
	#	verbose=True
	#	)
	#tempEval3_sim.show()

if __name__=="__main__":
	main()