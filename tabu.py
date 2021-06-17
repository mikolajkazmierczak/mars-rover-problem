import random
from utils import *


def main(settings):
  def find_neighborhood(solution, decisions):
    neighborhood = []
    length = 50
    while len(neighborhood) < length:
      candidate = get_variables(solution, decisions)
      if constraint_capacity(robot.capacity, candidate[1], samples) and \
        constraint_categories(samples, candidate[1], CATEGORIES) and \
        constraint_range(robot.range, candidate[0], distances_map):
        neighborhood.append(candidate)
    return neighborhood


  def tabu_search(path, d, first_value):
    tabu = []
    solution, decisions, current_value = path, d, first_value
    best_solution_ever = solution

    for count in range(ITERATIONS):
      neighborhood = find_neighborhood(solution, decisions)
      best_index = 0
      best_solution = neighborhood[best_index]
      print(f'Count: {count} with Distance: {objective(samples,best_solution[1])}')
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

      yield (count+1, best_solution_ever, current_value)


  # Config
  random.seed(settings['seed'])
  # tabu
  ITERATIONS = settings['tabu']['iterations']
  SIZE = settings['tabu']['size']

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
  decisions = [0 for _ in range(SAMPLES_N)]
  path = [[0 for _ in range(SAMPLES_N+1)] for _ in range(SAMPLES_N+1)]
  
  # Tabu search
  path, decisions = create_first_list(SAMPLES_N)
  distance = objective(samples, decisions)
  memo_paths, memo_values = [], []
  for count, solution, value in tabu_search(path, decisions, distance):
    memo_paths.append(solution)
    memo_values.append(value)
    masses = mass_vector(memo_paths, samples)
    distances = distance_vector(memo_paths, distances_map)
    yield count, memo_values, masses, distances

  # Solution
  print(f'Best solution:\n{pretty_matrix(solution[0])}')
  print(f'Best decisions:\n{solution[1]}')
  print(f'Best objective: {value}')
