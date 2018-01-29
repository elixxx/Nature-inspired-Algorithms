import parser
import numpy as np


def optimize_distances(distances, depth = 1):
    dim_x, dim_y = distances.shape
    opt_dist = distances.copy()

    # Initialize an array of empty lists for encoding via which consumers you go
    opt_via = np.empty((distances.shape), dtype=np.object_)
    opt_via.fill([])
    opt_via = np.frompyfunc(list, 1, 1)(opt_via)

    for iteration in range(depth):
        for from_y in range(dim_y):
            for to_x in range(from_y+1, dim_x):
                vias = [opt_dist[from_y, via] + opt_dist[via, to_x] for via in range(dim_y)]
                via_routes = [opt_via[from_y, via] + [via] + opt_via[via, to_x] for via in range(dim_y)]

                if not np.argmin(vias) in [from_y, to_x]:
                    opt_dist[from_y, to_x] = np.min(vias)
                    opt_via[from_y, to_x] = via_routes[np.argmin(vias)]
                # To make the matrix symmetrical again
                opt_dist[to_x, from_y] = opt_dist[from_y, to_x]
                opt_via[to_x, from_y] = list(reversed(opt_via[from_y, to_x]))

    return opt_dist, opt_via


matrix_via1 = np.mat([[0, 10, 2], [10, 0, 3], [2, 3, 0]])
# Optimized path from 0 to 1 via 2 and 3
matrix_via2 = np.mat([[0, 30, 5, 30], [30, 0, 40, 5], [5, 40, 0, 5], [30, 5, 5, 0]])


file = "../../problems/vehicle_routing/distance.txt"
distances = parser.parse_to_matrix(file)
matrix = distances

opt_dist, opt_via = optimize_distances(matrix, depth = 4)
print("Simple matrix")
print(matrix)

print("Optimized matrix")
print(opt_dist)
print(opt_via)