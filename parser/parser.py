import numpy as np

def parse_to_matrix(filepath, separator = " ", dtype = np.int32):
	"""
	By: Jan
	Reads a textfile to a matrix.
	Assumptions:Every line corresponds to one line of the matrix
	Every line has the same number of items
	A space character ends every line

	separator is the sign with which weights are separated
	dtype names the datatype of the returned matrix. Note that computations with int32 might be way faster!
	"""
	file = open(filepath, "r")

	array = []

	for line in file.readlines():
		weight_list = line.split(separator)[:-1] # To account for the space after each line of weights
		array.append(weight_list)

	return np.asarray(array, dtype = dtype)
