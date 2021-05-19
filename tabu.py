import random
from main import Robot, Sample, MarsMap, DistancesMap, \
  constraint_capacity, constraint_categories, constraint_comeback, \
  constraint_range, constraint_row_col_sum, objective
                   

# Config
random.seed(42)


# Constants
# robot
CAPACITY = 10
RANGE = 20
# map
X, Y = 5, 5
# samples
SAMPLES_N = 5
VALUES_RANGE = (1,10)
CATEGORIES_N = 2
CATEGORIES = [random.randrange(*VALUES_RANGE) for _ in range(CATEGORIES_N)]
MASS_RANGE = (1,10)


# Variables
decisions = [0 for _ in range(SAMPLES_N)]
path = [[0 for _ in range(SAMPLES_N+1)] for _ in range(SAMPLES_N+1)]


robot = Robot(CAPACITY, RANGE)

mars_map = MarsMap(X,Y)

samples = [Sample(i, CATEGORIES, MASS_RANGE) for i in range(SAMPLES_N)]
for sample in samples:
  mars_map.push_sample(sample)

distances_map = DistancesMap(SAMPLES_N,SAMPLES_N, samples)


print(mars_map)
print(distances_map)
