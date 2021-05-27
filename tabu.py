import copy
import matplotlib.pyplot as plt
import random
from utils import pretty_matrix, mass_vector, distance_vector
from main import Robot, Sample, MarsMap, DistancesMap, \
  constraint_capacity, constraint_categories, constraint_comeback, \
  constraint_range, constraint_row_col_sum, objective


def get_column(path, n):
    return [path[i][n] for i in range(len(path))]
    

def get_index(vector):
    return [i for i, el in enumerate(vector) if el]


def create_first_list(x):
    decisions = [0 for _ in range(x)]
    path = [[0 for _ in range(x+1)] for _ in range(x+1)]

    for i in range(x//10 + 1):
        path[i][i+1] = 1
        decisions[i] = 1
    path[(x//10)+1][0] = 1
    return path, decisions


def find_neighborhood(solution, decisions):
  neighborhood = []
  length = 50
  while len(neighborhood) < length:
    candidate = find_neighbour(solution, decisions)
    if constraint_capacity(robot.capacity, candidate[1], samples) and \
        constraint_categories(samples, candidate[1], CATEGORIES) and \
        constraint_range(robot.range, candidate[0], distances_map):
          neighborhood.append(candidate)
  return neighborhood


def find_neighbour(path, decisions):    
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
        return find_neighbour(path, decisions)


def tabu_search(path, d, first_value):
  tabu = []
  count = 1
  solution, decisions, current_value = path, d, first_value
  best_solution_ever = solution

  while count <= ITERATIONS:
    print(count)
    neighborhood = find_neighborhood(solution, decisions)
    best_index = 0
    best_solution = neighborhood[best_index]
    found = False
    while not found:
      i = 0
      while i < len(best_solution[1]):
        if best_solution[1][i] != decisions[i]:
          id_exchange = i
          value_exchange = best_solution[1][i]
          break
        i += 1
      if [id_exchange, value_exchange] not in tabu:
        tabu.append([id_exchange, value_exchange])
        found = True
        solution, decisions = best_solution
        cost = objective(samples, decisions)
        if cost > current_value:
          current_value = cost
          best_solution_ever = solution, decisions
      else:
        best_index += 1
        best_solution = neighborhood[best_index]

    if len(tabu) >= SIZE:
      tabu.pop(0)

    count += 1
    memory_path.append(best_solution_ever)
    memory_value.append(current_value)
  return best_solution_ever, current_value


# Config
random.seed(3)
ITERATIONS = 100
SIZE = 15

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

# Variables
decisions = [0 for _ in range(SAMPLES_N)]
path = [[0 for _ in range(SAMPLES_N+1)] for _ in range(SAMPLES_N+1)]
memory_path = []
memory_value = []

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

path, decisions = create_first_list(SAMPLES_N)
distance = objective(samples, decisions)
print(f'{pretty_matrix(path)}\nSolution: {decisions}\nValue: {distance}')
solution, value = tabu_search(path, decisions, distance)
print('Solution: \n', pretty_matrix(solution[0]))
print('Decisions: ', solution[1])
print('Value: ', value)

masses = mass_vector(memory_path, samples)
dis = distance_vector(memory_path, distances_map)


fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(memory_value,'r.-')
ax1.legend(['Objective'])
ax2 = fig.add_subplot(312)
ax2.plot(masses,'g.-')
ax2.legend(['Masa'])
ax3 = fig.add_subplot(313)
ax3.plot(dis,'b.-')
ax3.legend(['Dystans'])

plt.show()
