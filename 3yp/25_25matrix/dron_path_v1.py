import numpy as np



def calculate_path_cost(matrix, width, direction='horizontal'):
    """
    Calculate the total cost of covering the matrix with given width.
    :param matrix: 2D numpy array of the grid.
    :param width: Coverage width of the drone.
    :param direction: Direction of the drone's passes ('horizontal' or 'vertical').
    :return: Total cost and path of the drone.
    """
    total_cost = 0
    path = []
    if direction == 'horizontal':
        for row in range(0, matrix.shape[0], width):
            if row + width > matrix.shape[0]:  # Handle case where remaining area is less than width
                row = matrix.shape[0] - width
            for col in range(matrix.shape[1]):
                path.append((row, col))
                total_cost += np.sum(matrix[row:row+width, col])
    elif direction == 'vertical':
        for col in range(0, matrix.shape[1], width):
            if col + width > matrix.shape[1]:  # Handle case where remaining area is less than width
                col = matrix.shape[1] - width
            for row in range(matrix.shape[0]):
                path.append((row, col))
                total_cost += np.sum(matrix[row, col:col+width])
    return total_cost, path



def generate_drone_path(matrix, coverage_width):
    
    """
        this function would be the correct one, so don't use it.
    
    """
    path = []
    rows, cols = len(matrix), len(matrix[0])
    # Assuming the drone starts at the top-left corner and moves horizontally
    for row in range(0, rows, coverage_width):
        # If the row is even, move right; if odd, move left for zigzag pattern
        if (row // coverage_width) % 2 == 0:
            for col in range(cols):
                path.append((row, col))
                # Cover additional rows based on the coverage width
                for w in range(1, coverage_width):
                    if row + w < rows:
                        path.append((row + w, col))
        else:
            for col in range(cols - 1, -1, -1):
                path.append((row, col))
                # Cover additional rows based on the coverage width
                for w in range(1, coverage_width):
                    if row + w < rows:
                        path.append((row + w, col))
    return path




def calculate_drone_path(matrix, scan_width):
    """
        this function gives a drone's pathplanning with a given scan width
    
    """
    rows, cols = len(matrix), len(matrix[0])
    path = []
    direction = 1  # Start moving right; -1 means moving left

    # Calculate the number of passes needed based on the scanning width
    for row in range(0, rows, scan_width):
        if direction == 1:  # Moving right
            for col in range(cols):
                path.append((row, col))
        else:  # Moving left
            for col in range(cols - 1, -1, -1):
                path.append((row, col))
        
        # Move down by scan_width rows for the next pass, if within matrix bounds
        for down_step in range(1, min(scan_width, rows - row)):
            new_row = row + down_step
            if direction == 1:  # If moving right, add rightmost cell of the next row
                path.append((new_row, cols - 1))
            else:  # If moving left, add leftmost cell of the next row
                path.append((new_row, 0))

        direction *= -1  # Change direction for the next horizontal pass

    return path


