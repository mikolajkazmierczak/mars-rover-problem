from utils import pretty_matrix, mass_vector, distance_vector
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy
from main import Robot, Sample, MarsMap, DistancesMap, \
  constraint_capacity, constraint_categories, constraint_comeback, \
  constraint_range, constraint_row_col_sum, objective


random.seed(1)


def get_column(path, n):
    return [path[i][n] for i in range(len(path))]
    

def get_index(vector):
    return [i for i, el in enumerate(vector) if el]


def create_first_list(x):
    decisions = [0 for _ in range(x)]
    path = [[0 for _ in range(x+1)] for _ in range(x+1)]

    for i in range(x//20 + 1):
        path[i][i+1] = 1
        decisions[i] = 1
    path[(x//20)+1][0] = 1
    return path, decisions


def get_variables(path, decisions):    
    new_decisions = copy.deepcopy(decisions)
    new_path = copy.deepcopy(path)
    rand_id = random.randint(0,len(decisions)-1)
    
    if decisions[rand_id] == 0: 
        new_decisions[rand_id] = 1
        change = True
        id_replacement = random.choice(get_index(decisions))+1
    else: 
        new_decisions[rand_id] = 0
        change = False
        id_replacement = random.choice(get_index(new_decisions))+1
    if change:
        new_path[id_replacement][rand_id+1] = 1
        new_path[id_replacement][get_index(path[id_replacement])[0]] = 0
        new_path[rand_id+1][get_index(path[id_replacement])[0]] = 1
    else:
        new_path[rand_id+1][get_index(path[rand_id+1])[0]] = 0
        new_path[get_index(get_column(path, rand_id+1))[0]][id_replacement] = 1
        new_path[get_index(get_column(path, rand_id+1))[0]][rand_id+1] = 0

    if constraint_comeback(new_path) and constraint_row_col_sum(new_path):
        return new_path, new_decisions
    else:
        return get_variables(path, decisions)

##################################################
# Config and creating data
##################################################
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


robot = Robot(CAPACITY, RANGE)

mars_map = MarsMap(X,Y)

samples = [Sample(i, CATEGORIES, MASS_RANGE) for i in range(SAMPLES_N)]
for sample in samples:
  mars_map.push_sample(sample)

distances_map = DistancesMap(SAMPLES_N,SAMPLES_N, samples)




##################################################
# Simulated Annealing
##################################################
n = 5          # Number of cycles
m = 50          # Number of trials per cycle
na = 1          # Number of accepted solutions
prob_start = 0.7        # Probability of accepting worse solution at the start
prob_end = 0.001        # Probability of accepting worse solution at the end
t_start = -1.0/math.log(prob_start)             # Initial temperature
t_end = -1.0/math.log(prob_end)                 # Final temperature
frac = (t_end/t_start)**(1.0/(n-1.0))           # Fractional reduction every cycle
x_all = [create_first_list(SAMPLES_N)]          # Initialize x
x_current = x_all[0]
x_best = x_all[0]
f_best = objective(samples, x_current[1])
f_all = [f_best]      
t_current = t_start          # Current temperature
DeltaE_avg = 0.0     # DeltaE Average


for i in range(n):
    print('Cycle: ' + str(i) + ' with Temperature: ' + str(t_current))
    for j in range(m):
        # Generate new trial points
        while True:
            temp = get_variables(*x_current)
            if constraint_capacity(robot.capacity, temp[1], samples) and \
                constraint_categories(samples, temp[1], CATEGORIES) and \
                constraint_range(robot.range, temp[0], distances_map):
                x_current = temp
                break

        DeltaE = abs(objective(samples, x_current[1])-f_best)
        if (objective(samples, x_current[1]) < f_best):
            # Initialize DeltaE_avg if a worse solution was found
            #   on the first iteration
            if (i==0 and j==0): DeltaE_avg = DeltaE
            # objective function is worse
            # generate probability of acceptance
            p = math.exp(-DeltaE/(DeltaE_avg * t_current))
            # determine whether to accept worse point
            if (random.random()<p):
                # accept the worse solution
                accept = True
            else:
                # don't accept the worse solution
                accept = False
        else:
            # objective function is higher, automatically accept
            accept = True
        if (accept==True):
            # update currently accepted solution
            x_best = x_current
            f_best = objective(samples, x_best[1])
            # increment number of accepted solutions
            na = na + 1.0
            # update DeltaE_avg
            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
    # Record the best x values at the end of every cycle
    x_all.append(x_best)
    f_all.append(f_best)
    # Lower the temperature for next cycle
    t_current = frac * t_current

# print solution
print('Best solution: \n' + pretty_matrix(x_best[0]))
print(x_best[1])
print('Best objective: ' + str(f_best))

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
