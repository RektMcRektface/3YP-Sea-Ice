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
file_name = 'pathplanning_algo/map200/map.txt'

start = (0, 0) # Top-left corner for ship
destination = [199,199] # bottom-right corner for ship

max_risk_value = 7 # maximum value of danger map 

coverage_width = 50  # Example coverage width for drones

ship_speed = [1,1,1,3,5,6,9] # this is the time it travels, so the smaller the value is, the faster it travels

ship_speed = [4.1987, 4.0503, 3.8385,3.5471, 3.1599, 2.6607,2.0333]
# -4 2.0333  

# -3 2.6607 

# -2 3.1599 

# -1 3.5471

# 0 3.8385

# 1 4.0503

# 2 4.1987

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
    

# print("Matrix values range from {} to {}".format(np.min(matrix), np.max(matrix)))

matrix = [[-value + 3 for value in row] for row in matrix]
# matrix = [[value + 1 for value in row] for row in matrix]

simple_matrix = matrix



##################################### ship path dijkstra ####################################################

# # 1: when only moving in 4 directions
# shortest_path, shortest_path_length, runtime, count = dijkstra_v4.dijkstra_path_4(matrix,limit=4)
# ship_path = shortest_path
# mean_risk_value,ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix : ", count)
# print("shortest_path_length for dijkstra algo 4-direction is: ", shortest_path_length)
# print("mean_risk_value for dijkstra algo 4-direction is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# 2: when able to move diagonal 
shortest_path, shortest_path_length, runtime, count= dijkstra_v4.dijkstra_path_8(matrix,limit=4)
ship_path = shortest_path
mean_risk_value,ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
print("runtime is: ", runtime)
print(" occurrences of each value from 1 to 7 in the matrix : ", count)
print("shortest_path_length for dijkstra algo 8-direction is: ", shortest_path_length)
print("mean_risk_value for dijkstra algo 8-direction is: ", mean_risk_value)
print("estimated ship travelling time: ", ship_time)


# # 3: when able to move diagonal and add fixed penalty
# shortest_path, shortest_path_length, runtime, count = dijkstra_v4.dijkstra_path_8fixed(matrix, threshold=3, penalty=5)
# ship_path = shortest_path
# mean_risk_value,ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix : ", count)
# print("shortest_path_length for dijkstra algo 8-direction with fixed penalty is: ", shortest_path_length)
# print("mean_risk_value for dijkstra algo 8-direction with fixed penalty is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# # 4: when able to move diagonal and add various penalty
# shortest_path, shortest_path_length, runtime, count = dijkstra_v4.dijkstra_path_8vary(matrix, threshold=3, penalty_rate=3)
# ship_path = shortest_path
# mean_risk_value,ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for dijkstra algo 8-direction with various penalty is: ", shortest_path_length)
# print("mean_risk_value for dijkstra algo 8-direction with various penalty is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# # 5: when able to move diagonal and add various penalty and a fixed limit
# shortest_path, shortest_path_length, runtime, count = dijkstra_v4.dijkstra_path_8final(matrix, limit=5, threshold=3, penalty_rate=1)
# ship_path = shortest_path
# mean_risk_value,ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for dijkstra algo 8-direction with fixed limit is: ", shortest_path_length)
# print("mean_risk_value for dijkstra algo 8-direction with fixed limit is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


##################################### ship path a_star ####################################################

# # 6: when only moving in 4 directions
# simple_matrix = np.array(simple_matrix)
# goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
# ship_path, ship_path_length, runtime, count = a_star_v1.a_star_search_4(simple_matrix, start, goal, limit=4)
# ship_path = ship_path[::-1]  # Reverse path to start from the beginning
# mean_risk_value , ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for a-star algo 4-direction is: ", ship_path_length)
# print("mean_risk_value for a-star algo 4-direction with is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# # 7: when able to move diagonal 
# simple_matrix = np.array(simple_matrix)
# goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
# ship_path, ship_path_length, runtime, count= a_star_v1.a_star_search_8(simple_matrix, start, goal,limit=4)
# ship_path = ship_path[::-1]  # Reverse path to start from the beginning
# mean_risk_value, ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for a-star algo 8-direction is: ", ship_path_length)
# print("mean_risk_value for a-star algo 8-direction with is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# # 8: when able to move diagonal and add fixed penalty
# simple_matrix = np.array(simple_matrix)
# goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
# ship_path, ship_path_length, runtime, count= a_star_v1.a_star_search_8fixed(simple_matrix, start, goal,threshold=3, penalty=5)
# ship_path = ship_path[::-1]  # Reverse path to start from the beginning
# mean_risk_value, ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for a-star algo 8-direction with fixed penealty is: ", ship_path_length)
# print("mean_risk_value for a-star algo 8-direction with fixed penalty is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# # 9: when able to move diagonal and add various penalty
# simple_matrix = np.array(simple_matrix)
# goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
# ship_path, ship_path_length, runtime, count= a_star_v1.a_star_search_8vary(simple_matrix, start, goal,threshold=3, penalty_rate=2)
# ship_path = ship_path[::-1]  # Reverse path to start from the beginning
# mean_risk_value, ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for a-star algo 8-direction with various penalty is: ", ship_path_length)
# print("mean_risk_value for a-star algo 8-direction with various penalty is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)


# # 10: when able to move diagonal and add various penalty with a fixed limit
# simple_matrix = np.array(simple_matrix)
# goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
# ship_path, ship_path_length, runtime, count= a_star_v1.a_star_search_8final(simple_matrix, start, goal,threshold=3, penalty_rate=1, limit =5)
# ship_path = ship_path[::-1]  # Reverse path to start from the beginning
# mean_risk_value, ship_time = functions_v2.averagingandspeed(matrix, ship_path,ship_speed)
# print("runtime is: ", runtime)
# print("occurrences of each value from 1 to 7 in the matrix: ", count)
# print("shortest_path_length for a-star algo 8-direction is: ", ship_path_length)
# print("mean_risk_value for a-star algo 8-direction with is: ", mean_risk_value)
# print("estimated ship travelling time: ", ship_time)



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

centers = [] # irrelevant 

functions_v2.overall_visualisation_v3(simple_matrix, max_risk_value, ship_path, centers, drone_path)


#对比同一个threshold risk value的情况下：path的长短，经过的max risk和经过的次数，average risk value, run的时间长度， 肉眼观察是不是smooth的 