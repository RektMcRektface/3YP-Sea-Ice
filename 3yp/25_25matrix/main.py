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

# some useful parameters

scale = 5 # how large the matrix is gonna be compressed
max_risk_value = 7 # maximum value of danger map we set, e.g. 10/10 in simple_matrix
destination = [199,199] # set the destination to be fixed
limit = 4 # automatically set the highest risk that we want to take 


# this matrix is of size 25 * 25, simulate a simple iceberg danger map, with a range of 1-10 10 to be highest

# simple_matrix = [[1 ,2 ,2 ,3 ,4 ,4 ,4 ,8 ,9 ,10,10,9 ,7 ,5 ,4 ,4 ,2 ,4 ,3 ,3 ,2 ,5 ,6 ,8 ,4 ],
#                  [2 ,3 ,4 ,3 ,4 ,2 ,6 ,9 ,9 ,10,8 ,7 ,5 ,4 ,1 ,1 ,2 ,3 ,5 ,3 ,6 ,5 ,6 ,4 ,3 ],
#                  [1 ,2 ,3 ,2 ,1 ,4 ,4 ,6 ,8 ,8 ,7 ,7 ,5 ,4 ,2 ,2 ,3 ,4 ,5 ,4 ,3 ,2 ,3 ,5 ,6 ],
#                  [2 ,3 ,3 ,2 ,3 ,5 ,7 ,8 ,7 ,9 ,8 ,5 ,4 ,4 ,3 ,3 ,5 ,6 ,7 ,7 ,6 ,6 ,5 ,2 ,1 ],
#                  [5 ,4 ,4 ,4 ,3 ,3 ,5 ,6 ,7 ,7 ,6 ,4 ,2 ,2 ,1 ,2 ,2 ,5 ,6 ,5 ,6 ,8 ,7 ,4 ,2 ],
#                  [3 ,4 ,5 ,7 ,4 ,5 ,4 ,5 ,5 ,6 ,4 ,3 ,2 ,3 ,2 ,4 ,6 ,7 ,8 ,9 ,9 ,10,10,6 ,4 ],
#                  [3 ,3 ,3 ,2 ,3 ,4 ,2 ,5 ,5 ,4 ,3 ,3 ,2 ,2 ,2 ,4 ,5 ,6 ,8 ,9 ,10,10,9 ,9 ,7 ],
#                  [4 ,4 ,3 ,3 ,2 ,3 ,3 ,4 ,4 ,5 ,5 ,5 ,5 ,3 ,2 ,1 ,2 ,4 ,6 ,8 ,9 ,9 ,8 ,7 ,6 ],
#                  [7 ,7 ,5 ,3 ,1 ,2 ,3 ,4 ,5 ,5 ,6 ,5 ,4 ,4 ,3 ,3 ,2 ,2 ,4 ,6 ,8 ,8 ,7 ,6 ,4 ],
#                  [10,8 ,6 ,2 ,3 ,2 ,3 ,4 ,5 ,6 ,6 ,6 ,5 ,3 ,2 ,4 ,4 ,6 ,7 ,8 ,6 ,7 ,6 ,5 ,3 ],
#                  [9 ,7 ,5 ,5 ,4 ,2 ,3 ,5 ,6 ,7 ,8 ,8 ,6 ,4 ,3 ,3 ,3 ,4 ,6 ,6 ,5 ,6 ,3 ,3 ,2 ],
#                  [8 ,5 ,3 ,2 ,2 ,5 ,5 ,5 ,7, 8, 10,10,8 ,5 ,7 ,5 ,5 ,4 ,2 ,3 ,5 ,5 ,4 ,2 ,3 ],
#                  [4 ,2 ,1 ,1 ,3 ,6 ,7 ,8 ,8 ,9 ,10,10,10,8 ,8 ,7 ,6 ,4 ,2 ,4 ,3 ,6 ,2 ,3 ,1 ],
#                  [4 ,5 ,3 ,2 ,4 ,5 ,5 ,7 ,9 ,8 ,10,10,8 ,8 ,7 ,5 ,7 ,6 ,4 ,2 ,4 ,5 ,5 ,3 ,4 ],
#                  [5 ,4 ,3 ,2 ,3 ,4 ,3 ,5 ,3 ,6 ,7 ,8 ,6 ,5 ,4 ,3 ,4 ,4 ,3 ,3 ,3 ,4 ,5 ,5 ,6 ],
#                  [2 ,3 ,4 ,3 ,4 ,2 ,2 ,4 ,2 ,5 ,6 ,5 ,5 ,4 ,3 ,3 ,5 ,5 ,5 ,4 ,3 ,4 ,5 ,7 ,9 ],
#                  [5 ,4 ,4 ,3 ,2 ,3 ,3 ,4 ,4 ,5 ,4 ,3 ,2 ,4 ,4 ,1 ,3 ,3 ,5 ,3 ,2 ,3 ,6 ,8 ,9 ],
#                  [4 ,3 ,3 ,2 ,3 ,2 ,3 ,3 ,1 ,3 ,2 ,4 ,3 ,3 ,3 ,3 ,2 ,3 ,5 ,3 ,3 ,5 ,7 ,8 ,10],
#                  [2 ,2 ,3 ,2 ,4 ,3 ,2 ,3 ,4 ,2 ,5 ,4 ,1 ,3 ,2 ,4 ,4 ,3 ,3 ,2 ,4 ,2 ,4 ,6 ,7 ],
#                  [2 ,3 ,4 ,4 ,2 ,3 ,4 ,3 ,4 ,4 ,6 ,5 ,5 ,5 ,6 ,5 ,5 ,4 ,3 ,3 ,6 ,5 ,5 ,5 ,6 ],
#                  [5 ,4 ,4 ,3 ,5 ,4 ,3 ,4 ,5 ,6 ,6 ,7 ,6 ,5 ,4 ,4 ,3 ,3 ,5 ,3 ,5 ,4 ,5 ,4 ,3 ],
#                  [8 ,7 ,5 ,5 ,5 ,3 ,5 ,6 ,6 ,6 ,6 ,7 ,7 ,6 ,6 ,6 ,4 ,3 ,2 ,3 ,6 ,5 ,3 ,2 ,2 ],
#                  [5 ,4 ,3 ,3 ,2 ,3 ,4 ,5 ,6 ,6 ,6 ,6 ,5 ,5 ,5 ,5 ,5 ,4 ,3 ,2 ,5 ,4 ,3 ,1 ,1 ],
#                  [6 ,3 ,4 ,3 ,4 ,4 ,5 ,5 ,6 ,6 ,6 ,6 ,5 ,5 ,5 ,5 ,5 ,3 ,2 ,2 ,4 ,3 ,6 ,5 ,3 ],
#                  [7 ,6 ,5 ,3 ,2 ,5 ,6 ,6 ,6 ,6 ,6 ,6 ,6 ,6 ,5 ,3 ,2 ,4 ,5 ,3 ,6 ,3 ,3 ,3 ,2 ],
#                  ]

# Assuming the text file is named 'matrix.txt' and is located in the same directory as this script
file_name = '25_25matrix/map.txt'

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
matrix = [[value + 5 for value in row] for row in matrix]
simple_matrix = matrix

############### converting matrix ###########################################################

# compressed_matrix = functions_v2.compressed_matrix(simple_matrix, scale)
# # print(new_matrix)

# weighted_matrix = functions_v2.weighted_matrix(compressed_matrix)
# print(matrix)

################# version 1###################################################################


# optimal_path = dijkstra_v1.find_shortest_path(weighted_matrix, 0, 24)
# print(optimal_path)

# list_vertices = functions.path2vertex(optimal_path, compressed_matrix)
# print(list_vertices)

# functions.overall_visualisation(compressed_matrix, max_risk_value, list_vertices)


################# version 2####################################################################


# optimal_path_v2 = dijkstra_v2.find_shortest_path(weighted_matrix, 0, 24)
# print(optimal_path_v2)

# list_vertices_v2 = functions.path2vertex(optimal_path_v2, compressed_matrix)
# print(list_vertices_v2)


# expanded_list_vertices = functions.expanded_matrix(list_vertices_v2,simple_matrix, scale)
# expanded_list_vertices.append(destination)
# print(expanded_list_vertices)

# functions.overall_visualisation(compressed_matrix, max_risk_value, list_vertices_v2)

# functions.overall_visualisation(simple_matrix, max_risk_value, expanded_list_vertices)


#################version 3#########################################################################


# optimal_path_v3 = dijkstra_v3.find_all(weighted_matrix, limit, 0, 24)[1]
# # print(optimal_path_v3)

# list_vertices_v3 = functions_v2.path2vertex(optimal_path_v3, compressed_matrix)
# print(list_vertices_v3)

# expanded_list_vertices = functions_v2.expanded_matrix(list_vertices_v3,simple_matrix, scale,limit)
# expanded_list_vertices.append(destination)
# print(expanded_list_vertices)

# # functions_v2.overall_visualisation(compressed_matrix, max_risk_value, list_vertices_v3)
# functions_v2.overall_visualisation(simple_matrix, max_risk_value, expanded_list_vertices)


################## visualisation ####################################################################

# functions.draw_heatmap(compressed_matrix, max_risk_value)


#################a_star research######################################################################
simple_matrix = np.array(simple_matrix)
start = (0, 0) # Top-left corner
goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
path = a_star_v1.a_star_search(simple_matrix, start, goal)

# Convert path to a more readable format
path = path[::-1]  # Reverse path to start from the beginning
path = []
# print(path)

# value_threshold = 5  # Define what you consider a "high" value
# centers = drone_v1.find_high_value_centers(simple_matrix, value_threshold)
# print("Centers of high value areas:", centers)
centers = []

coverage_width = 50  # Example coverage width

# Calculate the drone path
drone_path = dron_path_v1.calculate_drone_path(simple_matrix, coverage_width)
# drone_path = []

functions_v2.overall_visualisation_v3(simple_matrix, max_risk_value, path, centers, drone_path)
