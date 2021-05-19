def euclidean_distance(p1, p2):
  return round( ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** (1/2), 3 )


def pretty_stringify_two_level_array(array):
  max_len = max([len(str(p)) for l in array for p in l])
  output = ''
  for level in array:
    for point in level:
      output += str(point) + ' '*(max_len-len(str(point))) + ' '
    output += '\n'
  return output
