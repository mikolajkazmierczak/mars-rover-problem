import math
import random
import matplotlib.pyplot as plt
from utils import pretty_matrix, mass_vector, distance_vector, create_first_list
from main import Robot, Sample, MarsMap, DistancesMap,\
  constraint_capacity, constraint_categories,\
	constraint_range,	objective, get_variables


# Config
random.seed(42)

# Constants
# robot
CAPACITY = 50
RANGE = 150
# map
X, Y = 50, 50
# samples
SAMPLES_N = 20
VALUES_RANGE = (1,10)
CATEGORIES_N = 2
CATEGORIES = [random.randrange(*VALUES_RANGE) for _ in range(CATEGORIES_N)]
MASS_RANGE = (1,10)

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
n = 100  # cycles
m = 50   # trials per cycle
na = 1   # accepted solutions
prob_start = 0.7  # accept the worse solution at the start
prob_end = 0.001  # accept the worse solution at the end
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
	t_current = frac * t_current

# Solution
print(f'Best solution:\n{pretty_matrix(x_best[0])}')
print(f'Best decisions:\n{x_best[1]}')
print(f'Best objective: {str(f_best)}')


# Plotting
masses = mass_vector(x_all, samples)
distances = distance_vector(x_all, distances_map)
fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(f_all,'r.-')
ax1.legend(['Objective'])
ax2 = fig.add_subplot(312)
ax2.plot(masses,'g.-')
ax2.legend(['Masa'])
ax3 = fig.add_subplot(313)
ax3.plot(distances,'b.-')
ax3.legend(['Dystans'])
plt.show()
