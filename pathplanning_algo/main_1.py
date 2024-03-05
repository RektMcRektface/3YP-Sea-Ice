import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import functions
import functions_v2
import dijkstra_v1
import dijkstra_v2
import dijkstra_v3
import a_star_v1
import drone_v1
import dron_path_v1
import os

#################################### parameters #####################################################

# Assuming the text file is named 'matrix.txt' and is located in the same directory as this script
file_name = 'pathplanning_algo/map.txt'

start = (0, 0) # Top-left corner for ship
destination = [199,199] # bottom-right corner for ship

max_risk_value = 7 # maximum value of danger map we set for ship to pass

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
matrix = [[-value + 5 for value in row] for row in matrix]
simple_matrix = matrix

##################################### ship path ####################################################

simple_matrix = np.array(simple_matrix)
goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
ship_path = a_star_v1.a_star_search(simple_matrix, start, goal)
ship_path = ship_path[::-1]  # Reverse path to start from the beginning
# ship_path = [] # if don't want to show ship-path

centers = [] # irrelevant 


##################################### drone path ###################################################

drone_path = dron_path_v1.calculate_drone_path(simple_matrix, coverage_width) # Calculate the drone path


#################################### visualisation ###############################################

functions_v2.overall_visualisation_v3(simple_matrix, max_risk_value, ship_path, centers, drone_path)
