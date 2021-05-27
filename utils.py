def euclidean_distance(p1, p2):
  return round( ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** (1/2), 3 )


def pretty_matrix(array):
  max_len = max([len(str(p)) for l in array for p in l])
  output = ''
  for i, level in enumerate(array):
    for point in level:
      output += str(point) + ' '*(max_len-len(str(point))) + ' '
    if i != len(array)-1:
      output += '\n'
  return output


def mass_vector(decision, samples):
  vector = []
  for j in decision:
    summary = []
    for i in range(len(samples)):
      summary.append(j[1][i] * samples[i].mass)
    vector.append(sum(summary))
  return vector


def distance_vector(path, distance_map):
  vector = []
  for p in path:
    summary =[]
    for i in range(len(distance_map.distances)):
      for j in range(len(distance_map.distances)):
        summary.append(p[0][i][j]*distance_map.distances[i][j])
    vector.append(sum(summary))
  return vector
