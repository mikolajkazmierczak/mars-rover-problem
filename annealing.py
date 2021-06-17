import math
import random
from utils import *


def main(settings):
	def annealing(na, t_current, DeltaE_avg, x_current, f_best):
		for i in range(N):
			print(f'Cycle: {i} with Temperature: {t_current}')
			for j in range(M):
				# trial points
				while True:
					temp = get_variables(*x_current)
					if constraint_capacity(robot.capacity, temp[1], samples) and \
						constraint_categories(samples, temp[1], CATEGORIES) and \
						constraint_range(robot.range, temp[0], distances_map):
						x_current = temp
						break
				
				DeltaE = abs(objective(samples, x_current[1])-f_best)
				if (objective(samples, x_current[1]) < f_best):
					if (i==0 and j==0): DeltaE_avg = DeltaE
					p = math.exp(-DeltaE/(DeltaE_avg * t_current))
					# determine whether to accept worse point
					if (random.random()<p):
						accept = True
					else:
						accept = False
				else:
					# accept higher objective function
					accept = True
				
				if (accept==True):
					x_best = x_current
					f_best = objective(samples, x_best[1])
					na += 1.0
					DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
					
			t_current = FRAC * t_current
			yield i+1, x_best, f_best

	# Config
	random.seed(42)

  # Constants
	# robot
	CAPACITY = settings['capacity']
	RANGE = settings['range']
  # map
	X = settings['x']
	Y = settings['y']
  # samples
	SAMPLES_N = settings['samplesN']
	VALUES_RANGE = (settings['valuesRangeStart'], settings['valuesRangeEnd'])
	CATEGORIES_N = settings['categoriesN']
	CATEGORIES = [random.randrange(*VALUES_RANGE) for _ in range(CATEGORIES_N)]
	MASS_RANGE = (settings['massRangeStart'], settings['massRangeEnd'])

	# Creating a Robot
	robot = Robot(CAPACITY, RANGE)
	# Generating a map of Mars
	mars_map = MarsMap(X,Y)
	# Generating the samples and mapping them onto the map
	samples = [Sample(i, CATEGORIES, MASS_RANGE) for i in range(SAMPLES_N)]
	for sample in samples:
		mars_map.push_sample(sample)
	# Calculating distances between all samples and every sample and the base
	distances_map = DistancesMap(SAMPLES_N,SAMPLES_N, samples)

	# Variables
	n = settings['annealing']['cycles']  # cycles
	m = settings['annealing']['trials']   # trials per cycle
	na = settings['annealing']['accepted']   # accepted solutions
	prob_start = settings['annealing']['probStart']  # accept the worse solution at the start
	prob_end = settings['annealing']['probEnd']  # accept the worse solution at the end
	t_start = -1.0/math.log(prob_start)     # init temperature
	t_end = -1.0/math.log(prob_end)         # final temperature
	frac = (t_end/t_start)**(1.0/(n-1.0))   # cycle reduction
	x_all = [create_first_list(SAMPLES_N)]  # init x
	x_current = x_all[0]
	x_best = x_all[0]
	f_best = objective(samples, x_current[1])
	f_all = [f_best]      
	t_current = t_start  # current temperature
	DeltaE_avg = 0.0     # DeltaE average

	# Annealing
	for i in range(n):
		print(f'Cycle: {i} with Temperature: {t_current}')
		for j in range(m):
			# trial points
			while True:
				temp = get_variables(*x_current)
				if constraint_capacity(robot.capacity, temp[1], samples) and \
					constraint_categories(samples, temp[1], CATEGORIES) and \
					constraint_range(robot.range, temp[0], distances_map):
					x_current = temp
					break

			DeltaE = abs(objective(samples, x_current[1])-f_best)
			if (objective(samples, x_current[1]) < f_best):
				if (i==0 and j==0): DeltaE_avg = DeltaE
				p = math.exp(-DeltaE/(DeltaE_avg * t_current))
				# determine whether to accept worse point
				if (random.random()<p):
					accept = True
				else:
					accept = False
			else:
				# accept higher objective function
				accept = True

			if (accept==True):
				x_best = x_current
				f_best = objective(samples, x_best[1])
				na = na + 1.0
				DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na

		x_all.append(x_best)
		f_all.append(f_best)
		masses = mass_vector(x_all, samples)
		distances = distance_vector(x_all, distances_map)
		yield i+1, f_all, masses, distances

		t_current = frac * t_current

	# Solution
	print(f'Best solution:\n{pretty_matrix(x_best[0])}')
	print(f'Best decisions:\n{x_best[1]}')
	print(f'Best objective: {str(f_best)}')
