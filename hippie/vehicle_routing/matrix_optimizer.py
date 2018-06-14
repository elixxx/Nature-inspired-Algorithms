import parser
import numpy as np


def path_length(distance_matrix, via_matrix, path, length = 0):
    from_node = path[0]
    for to_node in path[1:]:
        length += distance_matrix[to_node][from_node]
        from_node = to_node
    return length


def optimize_distances(distances, depth = 0):
    """Optimizes a distance matrix for depth steps or until convergence"""
    if depth == 0:
        #Dirty method to iterate until convergence
        depth = np.infty

    dim_x, dim_y = distances.shape
    opt_dist = distances.copy()

    # Initialize an array of empty lists for encoding via which consumers you go
    opt_via = np.empty((distances.shape), dtype=np.object_)
    opt_via.fill([])
    opt_via = np.frompyfunc(list, 1, 1)(opt_via)

    iteration = 0
    while True:
        if iteration >= depth:
            break

        opt_dist_old = opt_dist.copy()
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

        if (opt_dist_old == opt_dist).all():
            #If no changes in otp_dist happened in one iteration, stop optimization
            print("Convergence!")
            break
        iteration += 1

    return opt_dist, opt_via

def print_optimization(distances, opt_distances):
    smaller = np.sum((distances >opt_distances))
    ratios = 1-np.divide(opt_distances+0.0001, distances+0.0001) # Dirty method to avoid division by 0
    avg_ratio = np.average(ratios)
    print("The distances were optimized by an average of ~{}%".format(avg_ratio*100))
    print("We managed to reduce path distances for {} of {} node transitions".format(smaller, distances.size))


matrix_via1 = np.mat([[0, 10, 2], [10, 0, 3], [2, 3, 0]])
# Optimized path from 0 to 1 via 2 and 3
matrix_via2 = np.mat([[0, 30, 5, 30], [30, 0, 40, 5], [5, 40, 0, 5], [30, 5, 5, 0]])


file = "../../problems/vehicle_routing/distance.txt"
distances = parser.parse_to_matrix(file)
matrix = distances

opt_dist, opt_via = optimize_distances(matrix, depth = 0)
print("Simple matrix")
print(matrix)

print("Optimized matrix")
print(opt_dist)
print(opt_via)

print_optimization(matrix, opt_dist)

print(path_length(opt_dist, opt_via, [0, 1, 2, 0]))