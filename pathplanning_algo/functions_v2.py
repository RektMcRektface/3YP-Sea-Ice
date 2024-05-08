from math import inf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math
import dijkstra_v3 


def compressed_matrix(original_matrix, reduce_scale):
    """
    Returns a compressed matrix of size n * n from a original size

    Exceptions:
    Size of original matrix is not multiples of reduction scale, and this makes reduction number not integer.
    """
    if len(original_matrix)%reduce_scale == 0:
        
        scl = reduce_scale
        l = len(original_matrix)
        n = l//scl# dimensions of compressed matrix
        compressed_matrix = [[0 for _ in range(n)] for _ in range(n)] # initialise the compressed matrix
        
        # sum up n*n blocks
        for i in range(l):
            
            for j in range(l):
                
                compressed_matrix[i//n][j//n] += original_matrix[i][j]
            
        # get the average value for each nodes
        for i in range(n):
            
            for j in range(n):
                
                compressed_matrix[i][j] /= (scl * scl)
                
    else:
        print("Error: either number of rows or columns is not multiples of reduction scale selected, please re-select proper scale. ")
    
    return compressed_matrix

def weighted_matrix(matrix):
    """
    Returns a matrix with a weighted distance, 
    assume direction go to the [right | downward | diagonal downward right | diagonal downward left].
    with the distance to be the value of started point from orignal matrix

    Exceptions:
    Index out of range, Be careful with last row and last column that some directions are not existed.
    """
    
    l = len(matrix)
    num_v = l * l # number of vertices in matrix
    weighted_matrix = [[0 for _ in range(num_v)] for _ in range(num_v)] # initialise the weighted matrix
    
    for i in range(l):
        if i != l-1:
            for j in range(l):
                if j != l-1 and j!=0:
                    weighted_matrix[i*l+j][i*l+(j+1)] = weighted_matrix[i*l+(j+1)][i*l+j] =matrix[i][j] #direction to right/left
                    weighted_matrix[i*l+j][(i+1)*l+j] = weighted_matrix[(i+1)*l+j][i*l+j] =matrix[i][j] #direction to downward/up
                    weighted_matrix[i*l+j][(i+1)*l+(j+1)] = weighted_matrix[(i+1)*l+(j+1)][i*l+j] =matrix[i][j] #diagonal right direction
                    weighted_matrix[i*l+j][(i+1)*l+(j-1)] = weighted_matrix[(i+1)*l+(j-1)][i*l+j] =matrix[i][j] #diagonal left direction
                    
                elif j==l-1:
                    weighted_matrix[i*l+j][(i+1)*l+j] = weighted_matrix[(i+1)*l+j][i*l+j] =matrix[i][j]#direction to downward
                    weighted_matrix[i*l+j][(i+1)*l+(j-1)] = weighted_matrix[(i+1)*l+(j-1)][i*l+j] =matrix[i][j] #diagonal left direction
                else:
                    weighted_matrix[i*l+j][i*l+(j+1)] = weighted_matrix[i*l+(j+1)][i*l+j] =matrix[i][j] #direction to right/left
                    weighted_matrix[i*l+j][(i+1)*l+j] = weighted_matrix[(i+1)*l+j][i*l+j] =matrix[i][j] #direction to downward/up
                    weighted_matrix[i*l+j][(i+1)*l+(j+1)] = weighted_matrix[(i+1)*l+(j+1)][i*l+j] =matrix[i][j] #diagonal right direction
                    
        else:
            for j in range(l-1):
             weighted_matrix[i*l+j][i*l+(j+1)] = weighted_matrix[i*l+(j+1)][i*l+j] =matrix[i][j] #direction to right
             
            

    return weighted_matrix

def draw_heatmap(matrix, max_risk_value):
    
    """
    Returns only a graph of heatmap 
    """
    
    N = max_risk_value 
    cmap = LinearSegmentedColormap.from_list("custom", ["green", "yellow", "red"], N)
    plt.figure(figsize=(10, 8))  # Set the figure size for better readability
    sns.heatmap(matrix, annot=False, cmap=cmap, vmin=1, vmax=N)

    plt.title('Danger Map Heatmap')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    plt.show()
    
def overall_visualisation(matrix, max_risk_value, list_vertices):
    
    """
    Returns a graph of heatmap with a path line on it.
    """
    
    N = max_risk_value 
    cmap = LinearSegmentedColormap.from_list("custom", ["green", "yellow", "red"], N)
    plt.figure(figsize=(10, 8))  # Set the figure size for better readability
    sns.heatmap(matrix, annot=False, cmap=cmap, vmin=1, vmax=N)

    plt.title('Danger Map Heatmap')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    
    # Plotting the path on the heatmap
    # Unzipping the list of vertices to get separate lists of rows and columns
    rows = [list_vertices[i][0] for i in range(len(list_vertices))]
    cols = [list_vertices[i][1] for i in range(len(list_vertices))]
    plt.plot(cols, rows, color='blue', marker='o', linestyle='-', linewidth=2, markersize=5, label='Path')
    
    plt.legend()
    plt.grid(False) # Turn off the grid to not overlap with the heatmap

    plt.show()

# improved version of visualisation with added centre of icebergs pinned out
def overall_visualisation_v2(matrix, max_risk_value, list_vertices, list_centres):
    
    """
    Returns a graph of heatmap with a path line on it.
    """
    
    N = max_risk_value 
    cmap = LinearSegmentedColormap.from_list("custom", ["green", "yellow", "red"], N)
    plt.figure(figsize=(10, 8))  # Set the figure size for better readability
    sns.heatmap(matrix, annot=False, cmap=cmap, vmin=1, vmax=N)

    plt.title('Danger Map Heatmap')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    
    # Plotting the path on the heatmap
    # Unzipping the list of vertices to get separate lists of rows and columns
    rows = [list_vertices[i][0] for i in range(len(list_vertices))]
    cols = [list_vertices[i][1] for i in range(len(list_vertices))]
    plt.plot(cols, rows, color='blue', marker='o', linestyle='-', linewidth=2, markersize=5, label='Path')
    
    for point in list_centres:
        plt.plot(point[1], point[0], marker='X', markersize=10, color='purple', label='Additional Point')

    # To avoid duplicate legends for each additional point, we handle the legend entries manually
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Removing duplicate labels
    plt.legend(by_label.values(), by_label.keys())
    
    plt.grid(False) # Turn off the grid to not overlap with the heatmap

    plt.show()
    
# improved version of visualisation with added centre of icebergs pinned out
def overall_visualisation_v3(matrix, max_risk_value, list_vertices, list_centres, list_drones):
    
    """
    Returns a graph of heatmap with a path line on it.
    """
    
    N = max_risk_value 
    cmap = LinearSegmentedColormap.from_list("custom", ["green", "yellow", "red"], N)
    plt.figure(figsize=(10, 8))  # Set the figure size for better readability
    sns.heatmap(matrix, annot=False, cmap=cmap, vmin=1, vmax=N)

    plt.title('Danger Map Heatmap with limit=5')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    
    # Plotting the ship path on the heatmap
    # Unzipping the list of vertices to get separate lists of rows and columns
    rows = [list_vertices[i][0] for i in range(len(list_vertices))]
    cols = [list_vertices[i][1] for i in range(len(list_vertices))]
    plt.plot(cols, rows, color='blue', marker='o', linestyle='-', linewidth=4, markersize=5, label='Ship Path')
    
    # Plotting the drone path on the heatmap
    # Unzipping the list of vertices to get separate lists of rows and columns
    rows = [list_drones[i][0] for i in range(len(list_drones))]
    cols = [list_drones[i][1] for i in range(len(list_drones))]
    # plt.plot(cols, rows, color='black', marker='o', linestyle='-', linewidth=2, markersize=5, label='Drone Path')
    
    for point in list_centres:
        plt.plot(point[1], point[0], marker='X', markersize=10, color='purple', label='Additional Point')

    # To avoid duplicate legends for each additional point, we handle the legend entries manually
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Removing duplicate labels
    plt.legend(by_label.values(), by_label.keys())
    
    plt.grid(False) # Turn off the grid to not overlap with the heatmap

    plt.show()

def path2vertex(path, compressed_matrix):
    
    """
    Returns a list of corresponding vertices from path generated by Dijkstra
    """
    
    l = len(compressed_matrix)
    n = len(path)
    list_vertices = []
    
    for i in range(n):
        row = path[i]//l
        column = path[i]%l
        list_vertices.append([row,column])
    
    return list_vertices

def expanded_matrix(list_vertices,original_matrix, reduce_scale, limit):
    
    """
    Returns a list of expanded vertices, which are from the original matrix, can be directly used for visualisation.
    """
    
    expanded_list_vertices = []
    scl = reduce_scale
    
    for i in range(len(list_vertices)-1):
        
        cell_matrix = [[0 for _ in range(scl)] for _ in range(scl)] # initialise the compressed matrix
        
        start_vertex = list_vertices[i]
        end_vertex = list_vertices[i+1]
        
        
        if start_vertex[1] <= end_vertex[1]: # to check if direction is to downward left or not
            r = 0
            for row in range(scl*start_vertex[0],scl*start_vertex[0]+scl):
                
                c = 0
                for col in range(scl*start_vertex[1],scl*start_vertex[1]+scl):
                    
                    cell_matrix[r][c] = original_matrix[row][col]
                    c += 1
                r+= 1
            
            if start_vertex[0] == end_vertex[0]: # horizontal moving
                start_point = 0
                end_point = scl-1
            elif start_vertex[1] == end_vertex[1]: # vertical moving
                start_point = 0
                end_point = scl * (scl-1)       
            else: # diagonal right moving
                start_point = 0
                end_point = scl * scl -1
                
        else: # for the condition that it is going downward left
            
            r = 0
            for row in range(scl*start_vertex[0]-1,scl*start_vertex[0]+scl-1):
                
                c = 0
                for col in range(scl*start_vertex[1]-scl,scl*start_vertex[1]):
                    
                    cell_matrix[r][c] = original_matrix[row][col]
                    c += 1
                r+= 1
            
            start_point = scl -1
            end_point = scl * (scl-1)
            
            
        weighted_cell_matrix = weighted_matrix(cell_matrix)
        optimal_path = dijkstra_v3.find_shortest_path(weighted_cell_matrix, limit, start_point, end_point)
        new_list_vertices = path2vertex(optimal_path, cell_matrix)
        
        for j in range(len(new_list_vertices)):
            
            new_list_vertices[j][0] = new_list_vertices[j][0] + start_vertex[0]*scl
            new_list_vertices[j][1] = new_list_vertices[j][1] + start_vertex[1]*scl
            
            expanded_list_vertices.append(new_list_vertices[j])
     
    return expanded_list_vertices

def averagingandspeed(matrix, path,path_length):
    overall_score = 0
    overall_time = 0
    a =0
    b=0 
    
    for i,j in path:
        overall_score = overall_score + matrix[i][j]
        
    mean_value = - overall_score/len(path) + 3 
    
    speed = 0.0027 * mean_value ** 3 - 0.0398 * mean_value **2 + 0.2489 * mean_value + 3.8385

    overall_time = path_length * speed
        
    return overall_score/len(path), overall_time

def plot_histogram(data):
    # Extract keys and values from the dictionary
    keys = list(data.keys())
    values = list(data.values())
    
    # Creating the histogram
    plt.figure(figsize=(10, 5))  # Set the size of the plot
    plt.bar(keys, values, color='blue')  # Create a bar chart with blue bars
    
    # Adding titles and labels
    plt.title('Histogram of Values')
    plt.xlabel('Keys')
    plt.ylabel('Values')
    
    # Display the histogram
    plt.show()