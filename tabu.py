import copy
import random
from utils import pretty_matrix
from main import Robot, Sample, MarsMap, DistancesMap, \
  constraint_capacity, constraint_categories, constraint_comeback, \
  constraint_range, constraint_row_col_sum, objective


def get_matrixes(nodes):
  # generate a path and decisions matrixes from node path solution
  path = [[0 for _ in range(SAMPLES_N+1)] for _ in range(SAMPLES_N+1)]
  decisions = [0 for _ in range(SAMPLES_N)]
  for i in range(len(nodes)-1):
    path[nodes[i]][nodes[i+1]] = 1
  for node in nodes[1:-1]:
    decisions[node-1] = 1
  return path, decisions


def generate_neighbours():
  # generate a dict of solutions as: {0: [[1, 5.0]. [2, 4.0], ...], 1: ...}
  d = distances_map.distances
  neighbours = {}
  for i in range(len(d)):
    neighbours[i] = [[j, d[i][j]] for j in range(len(d)) if i != j]
  print(neighbours)
  return neighbours


def generate_first_solution_random(distances):
  # 1. generate random solution path like 0,3,1,2,0
  # 2. test if it fits the constraints (repeat up to X times)
  # 3. reduce the number of visited samples (0,2,3,0)
  # repeat
  tries = 100
  solution = None
  _len = len(distances)
  amount = _len-1
  while amount != 0 and not solution:
    count = 0
    while count < tries and not solution:
      path = [[0 for _ in range(SAMPLES_N+1)] for _ in range(SAMPLES_N+1)]
      decisions = [0 for _ in range(SAMPLES_N)]
      nodes = list(range(_len))
      nodes.pop(0)
      for _ in range(_len-1-amount):
        node = random.choice(nodes)
        nodes.remove(node) 
      random.shuffle(nodes)
      nodes = [0] + nodes + [0]
      # print(nodes)
      path, decisions = get_matrixes(nodes)
      if constraint_capacity(robot.capacity, decisions, samples) and \
        constraint_range(robot.range, path, distances_map) and \
        constraint_categories(samples, decisions, CATEGORIES):
        solution = nodes
      count += 1
    amount -= 1
  return solution


def generate_first_solution_dummy(neighbours):
  # generate a dummy solution based on distances only
  end = start = visiting = 0
  solution = []
  distance = 0

  while visiting not in solution:
    minim = 10000
    for k in neighbours[visiting]:
      if int(k[1]) < int(minim) and k[0] not in solution:
        minim = k[1]
        best_node = k[0]
    solution.append(visiting)
    distance += int(minim)
    visiting = best_node

  solution.append(end)

  position = 0
  for k in neighbours[solution[-2]]:
    if k[0] == start:
      break
    position += 1

  distance += int( neighbours[solution[-2]][position][1] ) - 10000
  return solution, distance


def find_neighborhood(solution, neighbours):
  neighborhood = []

  for i in solution[1:-1]:
    node1 = solution.index(i)
    for j in solution[1:-1]:
      node2 = solution.index(j)
      if i == j:
        continue

      neighbour = copy.deepcopy(solution)
      neighbour[node1] = j
      neighbour[node2] = i

      distance = 0
      for node in neighbour[:-1]:
        next_node = neighbour[neighbour.index(node)+1]
        for n in neighbours[node]:
          if n[0] == next_node:
            distance += int(n[1])
      neighbour.append(distance)

      if constraint_capacity(robot.capacity, decisions, samples) and \
        constraint_range(robot.range, path, distances_map) and \
        constraint_categories(samples, decisions, CATEGORIES):
        if neighbour not in neighborhood:
          neighborhood.append(neighbour)

  return sorted(neighborhood, key=lambda x: x[len(neighborhood[0])-1])


def tabu_search(first_solution, first_value, neighbours):
  tabu = []
  count = 1
  solution, value = first_solution, first_value
  best_solution_ever = solution

  while count <= ITERATIONS:
    neighborhood = find_neighborhood(solution, neighbours)
    best_index = 0
    best_solution = neighborhood[best_index]
    value_index = len(best_solution)-1

    found = False
    while not found:
      i = 0
      while i < len(best_solution):
        if best_solution[i] != solution[i]:
          first_exchange = best_solution[i]
          second_exchange = solution[i]
          break
        i += 1
      if [first_exchange, second_exchange] not in tabu\
      or [second_exchange, first_exchange] not in tabu:
        tabu.append([first_exchange, second_exchange])
        found = True
        solution = best_solution[:-1]
        cost = neighborhood[best_index][value_index]
        if cost < value:
          value = cost
          best_solution_ever = solution
      else:
        best_index += 1
        best_solution = neighborhood[best_index]

    if len(tabu) >= SIZE:
      tabu.pop(0)

    count += 1
  return best_solution_ever, value


# Config
random.seed(42)
ITERATIONS = 100
SIZE = 2

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

# print(pretty_matrix(distances_map.distances))


# Tabu search
neighbours = generate_neighbours()
nodes, distance = generate_first_solution_dummy(neighbours)
_, decisions = get_matrixes(nodes)
print(f'{pretty_matrix(path)}\nSolution: {decisions}\nValue: {distance}')
solution, value = tabu_search(nodes, distance, neighbours)
print(f'Solution: {solution}\nValue: {value}')

path, decisions = get_matrixes(solution)
obj = objective(samples, decisions)
print(pretty_matrix(path))
print(decisions)
print('Value:', obj)
