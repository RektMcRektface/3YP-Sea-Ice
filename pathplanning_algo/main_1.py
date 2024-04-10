import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import functions
import functions_v2
import dijkstra_v1
import dijkstra_v2
import dijkstra_v4
import a_star_v1
import drone_v1
import dron_path_v1
import os
import ACO

#################################### parameters #####################################################

# Assuming the text file is named 'matrix.txt' and is located in the same directory as this script
file_name = 'pathplanning_algo/map.txt'

start = (0, 0) # Top-left corner for ship
destination = [199,199] # bottom-right corner for ship

max_risk_value = 7 # maximum value of danger map 

coverage_width = 50  # Example coverage width for drones

################################### matrix generation ##################################################

# Initialize an empty list to hold the matrix
matrix = []

# Print the current working directory 
print("Current Working Directory: ", os.getcwd())

try:
    # Open the file for reading
    with open(file_name, 'r') as file:
        # Read each line in the file
        for line in file:
            # Strip newline characters and split the line into components based on commas
            row = line.strip().split(',')
            # Convert each string in the row to an integer (or float if necessary) and append to the matrix
            matrix.append([int(value) for value in row])
    
    print("Matrix loaded successfully.")
    # Optionally, print the matrix or its size to verify
    print(f"Matrix size: {len(matrix)}x{len(matrix[0])}")
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found in the current directory.")
except Exception as e:
    print(f"An error occurred: {e}")
    
# Add 5 to all values in the matrix
# print("Matrix values range from {} to {}".format(np.min(matrix), np.max(matrix)))
matrix = [[-value + 3 for value in row] for row in matrix]
simple_matrix = matrix

##################################### ship path a_star ####################################################

simple_matrix = np.array(simple_matrix)
goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
ship_path, ship_path_length = a_star_v1.a_star_search_4(simple_matrix, start, goal,5)
ship_path = ship_path[::-1]  # Reverse path to start from the beginning
print("shortest_path_length for a-star algo is: ", ship_path_length)

centers = [] # irrelevant 

##################################### ship path dijkstra ####################################################

# shortest_path, shortest_path_length = dijkstra_v4.dijkstra_path_4(matrix,5)
# ship_path = shortest_path
# print("shortest_path_length for dijkstra algo is: ", shortest_path_length)

##################################### ship path ACO ####################################################

# matrix_np = np.array(matrix)
# # print(matrix)
# print("Matrix values range from {} to {}".format(np.min(matrix), np.max(matrix)))
# aco = ACO.ACO(matrix_np, ants=50, evaporation_rate=0.1, iterations=100)
# best_path = aco.run()
# ship_path = best_path
# print(ship_path)

##################################### drone path ###################################################

drone_path = dron_path_v1.calculate_drone_path(simple_matrix, coverage_width) # Calculate the drone path
drone_path = []

#################################### visualisation ###############################################

functions_v2.overall_visualisation_v3(simple_matrix, max_risk_value, ship_path, centers, drone_path)


#对比同一个threshold risk value的情况下：path的长短，经过的max risk和经过的次数，run的时间长度， 肉眼观察是不是smooth的 