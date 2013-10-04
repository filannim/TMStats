from __future__ import division
import numpy as np
import sys

from participant import ChallengesSimulator

def main():
	
	computing_power = round(np.float(sys.argv[2]),2)
	start = 0
	end = 6000
	step = 25
	trials = 10000

	participants_range = range(1, 31)
	ceilings_range = [round(np.float(e/100),2) for e in range(30,101,5)]
	stds_range = [round(np.float(e),4) for e in [0.0001, 0.0002, 0.0005, 0.001, 0.005]]

	epoch = 1
	epochs = len(participants_range)*len(ceilings_range)*len(stds_range)

	for participants in participants_range:
		for ceiling in ceilings_range:
			for std in stds_range:
				print '%4.0f/%4.0f: Computing [%3.0f, %6.0f, %3.0f], %6.0f, [%2.0f, %3.2f, %4.3f] ...' % (epoch, epochs, start, end, step, trials, participants, ceiling, std), 
				c = ChallengesSimulator([start, end, step], trials, [participants, ceiling, std], computing_power)
				c.store()
				del c
				epoch += 1
				print 'finished.'

if __name__ == '__main__':
	main()

