import argparse
import copy


def generate_neighbours():
    return {
        0:
            [[1, 18.56], [2, 21.26], [3, 25.43], [4, 27.14], [5, 20.24], [6, 15.45], [7, 21.95], [8, 21.3], [9, 17.06], [10, 25.86], [11, 36.73], [12, 5.11], [13, 24.32], [14, 16.42], [15, 24.8], [16, 12.65], [17, 20.43], [18, 28.88], [19, 18.81], [20, 14.92]],
        1:
            [[0, 18.17], [2, 36.29], [3, 23.14], [4, 45.32], [5, 1.05], [6, 21.83], [7, 23.79], [8, 35.28], [9, 6.08], [10, 40.34], [11, 53.54], [12, 14.18], [13, 36.75], [14, 26.0], [15, 24.79], [16, 32.9], [17, 18.98], [18, 17.99], [19, 38.43], [20, 33.31]],
        2:
            [[0, 22.33], [1, 36.8], [3, 30.18], [4, 24.63], [5, 39.13], [6, 33.62], [7, 24.3], [8, 2.24], [9, 34.56], [10, 5.44], [11, 14.57], [12, 25.16], [13, 7.25], [14, 16.46], [15, 28.73], [16, 12.47], [17, 42.43], [18, 49.26], [19, 13.31], [20, 10.98]],
        3:
            [[0, 24.02], [1, 21.86], [2, 30.0], [4, 47.02], [5, 23.75], [6, 38.24], [7, 5.21], [8, 27.9], [9, 17.3], [10, 28.58], [11, 38.38], [12, 23.68], [13, 25.56], [14, 14.2], [15, 3.79], [16, 31.18], [17, 37.89], [18, 40.37], [19, 37.96], [20, 31.23]],
        4:
            [[0, 27.46], [1, 43.36], [2, 23.01], [3, 48.69], [5, 47.35], [6, 29.54], [7, 41.52], [8, 25.18], [9, 43.23], [10, 28.1], [11, 31.41], [12, 32.62], [13, 31.68], [14, 34.81], [15, 48.19], [16, 16.21], [17, 37.09], [18, 47.76], [19, 11.28], [20, 16.21]],
        5:
            [[0, 19.55], [1, 1.05], [2, 39.87], [3, 23.31], [4, 47.69], [6, 22.91], [7, 23.6], [8, 38.86], [9, 6.56], [10, 40.2], [11, 51.97], [12, 14.63], [13, 37.64], [14, 26.13], [15, 26.98], [16, 32.53], [17, 19.43], [18, 18.21], [19, 37.31], [20, 35.62]],
        6:
            [[0, 15.69], [1, 23.04], [2, 36.87], [3, 40.09], [4, 29.51], [5, 22.39], [7, 35.26], [8, 34.89], [9, 23.16], [10, 39.45], [11, 51.49], [12, 15.7], [13, 40.26], [14, 32.48], [15, 39.46], [16, 24.13], [17, 10.14], [18, 21.35], [19, 28.13], [20, 24.58]],
        7:
            [[0, 22.55], [1, 23.02], [2, 25.82], [3, 5.39], [4, 43.47], [5, 24.53], [6, 34.72], [8, 22.45], [9, 17.96], [10, 23.36], [11, 35.5], [12, 19.39], [13, 19.38], [14, 9.05], [15, 3.85], [16, 26.87], [17, 36.56], [18, 43.08], [19, 31.83], [20, 27.34]],
        8:
            [[0, 20.19], [1, 37.05], [2, 2.33], [3, 28.02], [4, 25.88], [5, 39.12], [6, 34.23], [7, 22.91], [9, 31.27], [10, 4.77], [11, 14.64], [12, 24.17], [13, 5.79], [14, 13.13], [15, 25.14], [16, 14.34], [17, 43.98], [18, 48.46], [19, 14.22], [20, 11.29]],
        9:
            [[0, 16.11], [1, 6.38], [2, 34.41], [3, 17.54], [4, 42.02], [5, 6.5], [6, 24.94], [7, 17.72], [8, 31.92], [10, 35.73], [11, 43.86], [12, 11.65], [13, 31.44], [14, 20.48], [15, 20.44], [16, 27.44], [17, 21.62], [18, 23.33], [19, 34.89], [20, 28.76]],
        10:
            [[0, 25.56], [1, 40.92], [2, 5.36], [3, 28.59], [4, 29.26], [5, 40.49], [6, 39.87], [7, 25.08], [8, 4.85], [9, 33.85], [11, 10.58], [12, 27.6], [13, 4.44], [14, 16.27], [15, 25.84], [16, 18.54], [17, 46.86], [18, 54.56], [19, 17.28], [20, 15.25]],
        11:
            [[0, 34.13], [1, 53.19], [2, 14.67], [3, 39.25], [4, 33.59], [5, 52.64], [6, 47.57], [7, 32.8], [8, 14.65], [9, 47.77], [10, 11.12], [12, 41.03], [13, 13.89], [14, 25.93], [15, 34.41], [16, 27.01], [17, 58.67], [18, 64.82], [19, 24.22], [20, 23.18]],
        12:
            [[0, 5.13], [1, 14.25], [2, 26.52], [3, 23.64], [4, 32.25], [5, 15.27], [6, 15.33], [7, 20.65], [8, 24.21], [9, 11.77], [10, 29.8], [11, 40.9], [13, 26.3], [14, 18.08], [15, 22.8], [16, 18.61], [17, 19.58], [18, 25.31], [19, 24.97], [20, 19.29]],
        13:
            [[0, 23.54], [1, 36.9], [2, 7.78], [3, 24.55], [4, 30.04], [5, 37.33], [6, 38.56], [7, 20.67], [8, 5.91], [9, 31.38], [10, 4.39], [11, 14.14], [12, 28.12], [14, 12.8], [15, 21.34], [16, 19.78], [17, 43.81], [18, 55.17], [19, 19.83], [20, 16.3]],
        14:
            [[0, 16.73], [1, 25.83], [2, 16.24], [3, 14.03], [4, 35.26], [5, 26.8], [6, 32.26], [7, 9.04], [8, 13.37], [9, 20.57], [10, 15.3], [11, 27.64], [12, 17.67], [13, 12.55], [15, 12.44], [16, 19.11], [17, 35.03], [18, 43.19], [19, 23.56], [20, 18.25]],
        15:
            [[0, 25.52], [1, 26.42], [2, 28.14], [3, 3.71], [4, 46.07], [5, 25.71], [6, 39.38], [7, 3.71], [8, 24.35], [9, 19.47], [10, 27.55], [11, 36.37], [12, 24.6], [13, 22.39], [14, 12.01], [16, 29.73], [17, 40.13], [18, 43.56], [19, 36.4], [20, 31.12]],
        16:
            [[0, 13.26], [1, 31.55], [2, 12.92], [3, 31.46], [4, 15.71], [5, 33.95], [6, 23.78], [7, 26.69], [8, 13.15], [9, 28.47], [10, 18.36], [11, 25.9], [12, 18.52], [13, 19.38], [14, 19.68], [15, 30.4], [17, 29.91], [18, 40.41], [19, 6.29], [20, 2.43]],
        17:
            [[0, 21.28], [1, 17.59], [2, 42.14], [3, 39.39], [4, 37.11], [5, 19.13], [6, 9.68], [7, 37.01], [8, 42.62], [9, 21.39], [10, 47.74], [11, 58.06], [12, 18.22], [13, 44.88], [14, 35.4], [15, 42.75], [16, 31.38], [18, 11.32], [19, 37.61], [20, 33.35]],
        18:
            [[0, 28.86], [1, 18.86], [2, 52.18], [3, 42.91], [4, 50.11], [5, 18.9], [6, 22.03], [7, 41.98], [8, 51.56], [9, 24.25], [10, 56.67], [11, 65.7], [12, 26.98], [13, 54.07], [14, 42.42], [15, 42.84], [16, 40.42], [17, 11.75], [19, 47.05], [20, 43.93]],
        19:
            [[0, 19.19], [1, 37.12], [2, 12.46], [3, 36.87], [4, 11.11], [5, 38.31], [6, 27.67], [7, 31.49], [8, 14.25], [9, 35.36], [10, 18.48], [11, 22.95], [12, 24.03], [13, 20.36], [14, 23.75], [15, 35.12], [16, 6.25], [17, 37.81], [18, 47.33], [20, 5.85]],
        20:
            [[0, 14.32], [1, 33.81], [2, 10.59], [3, 30.55], [4, 16.1], [5, 34.83], [6, 26.27], [7, 28.27], [8, 11.46], [9, 30.09], [10, 15.96], [11, 24.2], [12, 18.85], [13, 16.48], [14, 18.46], [15, 29.29], [16, 2.31], [17, 34.06], [18, 43.01], [19, 5.47]]
    }



def generate_first_solution(dict_of_neighbours):
    end_node = start_node = 0

    first_solution = []

    visiting = start_node

    distance_of_first_solution = 0
    while visiting not in first_solution:
        minim = 10000
        for k in dict_of_neighbours[visiting]:
            if int(k[1]) < int(minim) and k[0] not in first_solution:
                minim = k[1]
                best_node = k[0]

        first_solution.append(visiting)
        distance_of_first_solution = distance_of_first_solution + int(minim)
        visiting = best_node

    first_solution.append(end_node)

    position = 0
    for k in dict_of_neighbours[first_solution[-2]]:
        if k[0] == start_node:
            break
        position += 1

    distance_of_first_solution = (
        distance_of_first_solution
        + int(dict_of_neighbours[first_solution[-2]][position][1])
        - 10000
    )
    return first_solution, distance_of_first_solution


def find_neighborhood(solution, dict_of_neighbours):
    neighborhood_of_solution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0

            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                for i in dict_of_neighbours[k]:
                    if i[0] == next_node:
                        distance = distance + int(i[1])
            _tmp.append(distance)

            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours):
    count = 1
    solution = first_solution
    tabu_list = []
    best_cost = distance_of_first_solution
    best_solution_ever = solution

    while count <= ITERS:
        neighborhood = find_neighborhood(solution, dict_of_neighbours)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1

        found = False
        while not found:
            i = 0
            while i < len(best_solution):

                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1

            if [first_exchange_node, second_exchange_node] not in tabu_list \
            or [second_exchange_node, first_exchange_node] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            else:
                index_of_best_solution = index_of_best_solution + 1
                best_solution = neighborhood[index_of_best_solution]

        if len(tabu_list) >= SIZE:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_cost


ITERS = 100
SIZE = 20

dict_of_neighbours = generate_neighbours()
print(dict_of_neighbours)
first_solution, distance_of_first_solution = generate_first_solution(dict_of_neighbours)
best_sol, best_cost = tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours)
print(f"Best solution: {best_sol}, with total distance: {best_cost}.")

# SAMPLES_N = 20
# def get_matrixes(nodes):
#   path = [[0 for _ in range(SAMPLES_N+1)] for _ in range(SAMPLES_N+1)]
#   decisions = [0 for _ in range(SAMPLES_N)]
#   for i in range(len(nodes)-1):
#     path[nodes[i]][nodes[i+1]] = 1
#   for node in nodes[1:-1]:
#     decisions[node-1] = 1
#   return path, decisions

# path, decisions = get_matrixes(best_sol)
# from utils import pretty_matrix
# print(pretty_matrix(path))
# print(decisions)
# from main import objective, Sample
# import random
# VALUES_RANGE = (1,10)
# CATEGORIES_N = 2
# CATEGORIES = [random.randrange(*VALUES_RANGE) for _ in range(CATEGORIES_N)]
# MASS_RANGE = (1,10)
# samples = [Sample(i, CATEGORIES, MASS_RANGE) for i in range(SAMPLES_N)]
# print(objective(samples, decisions))




