import numpy as np
len_path = 40

pheromones = np.random.rand(len_path, len_path)

all_cities = list(range(0, len_path))
unvisited_cities = all_cities.copy()
current_city = np.random.choice(unvisited_cities)
unvisited_cities.remove(current_city)
path = [current_city]

while not len(unvisited_cities) == 0:
    next_pheromones = np.zeros(len_path)
    next_probs = np.zeros(len_path)
    print(path)
    for i in unvisited_cities:
        next_pheromones[i] = pheromones[current_city][i]
    next_probs = next_pheromones / np.sum(next_pheromones)
    print(next_probs, sum(next_probs))

    print(len(all_cities), len(next_probs))

    next_city = np.random.choice(all_cities, p=next_probs)
    path.append(next_city)
    unvisited_cities.remove(next_city)
    current_city = next_city

path.append(path[0])

print(path)
