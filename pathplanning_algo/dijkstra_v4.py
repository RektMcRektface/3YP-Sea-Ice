import heapq
import math
import time  # Import time module for timing the function


###################### 4 directions #######################################
def dijkstra_path_4(matrix, limit):
    
    start_time = time.time()  # Start timing
    
    value_count = {i: 0 for i in range(1, 8)}  # Initialize counts for values 1 to 7

    nrows, ncols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]  # Right, down, up, left
    start, goal = (0, 0), (nrows - 1, ncols - 1)
    
    # Distance grid initialized with infinity
    distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    distances[start[0]][start[1]] = 0
    
    # Parent grid to reconstruct the path later
    parents = [[None for _ in range(ncols)] for _ in range(nrows)]
    
    queue = [(0, start)]
    visited = set()
    
    while queue:
        current_distance, current_position = heapq.heappop(queue)
        if current_position in visited:
            continue
        visited.add(current_position)
        
        if current_position == goal:
            break
        
        for direction in directions:
            next_row, next_col = current_position[0] + direction[0], current_position[1] + direction[1]
            if 0 <= next_row < nrows and 0 <= next_col < ncols and matrix[next_row][next_col] <= limit:
                new_distance = current_distance + 1
                if new_distance < distances[next_row][next_col]:
                    distances[next_row][next_col] = new_distance
                    parents[next_row][next_col] = current_position
                    heapq.heappush(queue, (new_distance, (next_row, next_col)))
    
    path = []
    if distances[goal[0]][goal[1]] == float('inf'):
        return None  # No path found
    
    # Reconstruct the path
    current = goal
    while current:
        path.append(current)
        current = parents[current[0]][current[1]]
        if current and 1 <= matrix[current[0]][current[1]] <= 7:
            value_count[matrix[current[0]][current[1]]] += 1

    path.reverse()  # The path was constructed backwards, so reverse it
    
    end_time = time.time()  # Stop timing
    time_taken = end_time - start_time  # Calculate time taken
    
    return path, distances[goal[0]][goal[1]], time_taken, value_count



############################# 8 directions ###########################################
def dijkstra_path_8(matrix,limit):
    
    start_time = time.time()  # Start timing
    
    value_count = {i: 0 for i in range(1, 8)}  # Initialize counts for values 1 to 7

    nrows, ncols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1),(1,1),(-1,-1),(1,-1),(-1,1)]  # Right, down, up, left, right-down,left-up,right-up,left-down
    start, goal = (0, 0), (nrows - 1, ncols - 1)
    
    # Distance grid initialized with infinity
    distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    distances[start[0]][start[1]] = 0
    
    # Parent grid to reconstruct the path later
    parents = [[None for _ in range(ncols)] for _ in range(nrows)]
    
    queue = [(0, start)]
    visited = set()
    
    while queue:
        current_distance, current_position = heapq.heappop(queue)
        if current_position in visited:
            continue
        visited.add(current_position)
        
        if current_position == goal:
            break
        
        for direction in directions:
            if direction[0] != 0 and direction[1] != 0 : #diagonal directions
                next_row, next_col = current_position[0] + direction[0], current_position[1] + direction[1]
                if 0 <= next_row < nrows and 0 <= next_col < ncols and matrix[next_row][next_col] <= limit:
                    new_distance = current_distance + math.sqrt(2)
                    if new_distance < distances[next_row][next_col]:
                        distances[next_row][next_col] = new_distance
                        parents[next_row][next_col] = current_position
                        heapq.heappush(queue, (new_distance, (next_row, next_col)))
                        
            else: # vertical or horizontal directions
                next_row, next_col = current_position[0] + direction[0], current_position[1] + direction[1]
                if 0 <= next_row < nrows and 0 <= next_col < ncols and matrix[next_row][next_col] <= limit:
                    new_distance = current_distance + 1
                    if new_distance < distances[next_row][next_col]:
                        distances[next_row][next_col] = new_distance
                        parents[next_row][next_col] = current_position
                        heapq.heappush(queue, (new_distance, (next_row, next_col)))
    
    path = []
    if distances[goal[0]][goal[1]] == float('inf'):
        return None  # No path found
    
    # Reconstruct the path
    current = goal
    while current:
        path.append(current)
        current = parents[current[0]][current[1]]
        if current and 1 <= matrix[current[0]][current[1]] <= 7:
            value_count[matrix[current[0]][current[1]]] += 1
    path.reverse()  # The path was constructed backwards, so reverse it
    
    end_time = time.time()  # Stop timing
    time_taken = end_time - start_time  # Calculate time taken
    
    return path, distances[goal[0]][goal[1]], time_taken, value_count



############################# 8 directions with fixed penalty ###########################################
def dijkstra_path_8fixed(matrix, threshold, penalty):
    
    start_time = time.time()  # Start timing
    
    value_count = {i: 0 for i in range(1, 8)}  # Initialize counts for values 1 to 7

    nrows, ncols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # 8 directions
    start, goal = (0, 0), (nrows - 1, ncols - 1)

    distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    distances[start[0]][start[1]] = 0
    
    penalty_distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    penalty_distances[start[0]][start[1]] = 0
    
    parents = [[None for _ in range(ncols)] for _ in range(nrows)]
    
    queue = [(0, start)]
    visited = set()
    
    while queue:
        current_distance, current_position = heapq.heappop(queue)
        if current_position in visited:
            continue
        visited.add(current_position)
        
        if current_position == goal:
            break
        
        for direction in directions:
            next_row, next_col = current_position[0] + direction[0], current_position[1] + direction[1]
            if 0 <= next_row < nrows and 0 <= next_col < ncols:
                value = matrix[next_row][next_col]
                penalty_cost = penalty if value > threshold else 0  # Apply penalty if value exceeds limit
                
                # Determine cost based on direction
                step_cost = math.sqrt(2) if direction[0] != 0 and direction[1] != 0 else 1
                new_penalty_distance = current_distance + step_cost + penalty_cost
                new_distance = current_distance + step_cost
                
                if new_penalty_distance < penalty_distances[next_row][next_col]:
                    distances[next_row][next_col] = new_distance
                    penalty_distances[next_row][next_col] = new_penalty_distance
                    parents[next_row][next_col] = current_position
                    heapq.heappush(queue, (new_penalty_distance, (next_row, next_col)))

    # Reconstruct the path
    path = []
    if penalty_distances[goal[0]][goal[1]] == float('inf'):
        return None, None  # No path found

    current = goal
    while current:
        path.append(current)
        current = parents[current[0]][current[1]]
        if current and 1 <= matrix[current[0]][current[1]] <= 7:
            value_count[matrix[current[0]][current[1]]] += 1
    path.reverse()

    end_time = time.time()  # Stop timing
    time_taken = end_time - start_time  # Calculate time taken
    
    return path, distances[goal[0]][goal[1]],time_taken, value_count



############################# 8 directions with varying penalty ###########################################
def dijkstra_path_8vary(matrix, threshold, penalty_rate):
    
    start_time = time.time()  # Start timing
    
    value_count = {i: 0 for i in range(1, 8)}  # Initialize counts for values 1 to 7

    nrows, ncols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # 8 directions
    start, goal = (0, 0), (nrows - 1, ncols - 1)

    distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    distances[start[0]][start[1]] = 0
    
    penalty_distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    penalty_distances[start[0]][start[1]] = 0
    
    parents = [[None for _ in range(ncols)] for _ in range(nrows)]
    
    queue = [(0, start)]
    visited = set()
    
    while queue:
        current_distance, current_position = heapq.heappop(queue)
        if current_position in visited:
            continue
        visited.add(current_position)
        
        if current_position == goal:
            break
        
        for direction in directions:
            next_row, next_col = current_position[0] + direction[0], current_position[1] + direction[1]
            if 0 <= next_row < nrows and 0 <= next_col < ncols:
                value = matrix[next_row][next_col]
                penalty_cost = penalty_rate*(value - threshold) if value > threshold else 0  # Apply penalty if value exceeds limit
                
                # Determine cost based on direction
                step_cost = math.sqrt(2) if direction[0] != 0 and direction[1] != 0 else 1
                new_penalty_distance = current_distance + step_cost + penalty_cost
                new_distance = current_distance + step_cost
                
                if new_penalty_distance < penalty_distances[next_row][next_col]:
                    distances[next_row][next_col] = new_distance
                    penalty_distances[next_row][next_col] = new_penalty_distance
                    parents[next_row][next_col] = current_position
                    heapq.heappush(queue, (new_penalty_distance, (next_row, next_col)))

    # Reconstruct the path
    path = []
    if penalty_distances[goal[0]][goal[1]] == float('inf'):
        return None, None  # No path found

    current = goal
    while current:
        path.append(current)
        current = parents[current[0]][current[1]]
        if current and 1 <= matrix[current[0]][current[1]] <= 7:
            value_count[matrix[current[0]][current[1]]] += 1
    path.reverse()

    end_time = time.time()  # Stop timing
    time_taken = end_time - start_time  # Calculate time taken
    
    return path, distances[goal[0]][goal[1]],time_taken, value_count



############################# 8 directions with varying penalty and a fixed limit ##################################
def dijkstra_path_8final(matrix, limit, threshold ,penalty_rate ):
    
    start_time = time.time()  # Start timing
    
    value_count = {i: 0 for i in range(1, 8)}  # Initialize counts for values 1 to 7

    nrows, ncols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # 8 directions
    start, goal = (0, 0), (nrows - 1, ncols - 1)

    distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    distances[start[0]][start[1]] = 0
    
    penalty_distances = [[float('inf') for _ in range(ncols)] for _ in range(nrows)]
    penalty_distances[start[0]][start[1]] = 0
    
    parents = [[None for _ in range(ncols)] for _ in range(nrows)]
    
    queue = [(0, start)]
    visited = set()
    
    while queue:
        current_distance, current_position = heapq.heappop(queue)
        if current_position in visited:
            continue
        visited.add(current_position)
        
        if current_position == goal:
            break
        
        for direction in directions:
            next_row, next_col = current_position[0] + direction[0], current_position[1] + direction[1]
            
            if 0 <= next_row < nrows and 0 <= next_col < ncols :
                
                value = matrix[next_row][next_col]
                
                if value <= limit:
                    
                    penalty_cost = penalty_rate*(value - threshold) if value > threshold else 0  # Apply penalty if value exceeds limit
                    
                    # Determine cost based on direction
                    step_cost = math.sqrt(2) if direction[0] != 0 and direction[1] != 0 else 1
                    new_penalty_distance = current_distance + step_cost + penalty_cost
                    new_distance = current_distance + step_cost
                    
                    if new_penalty_distance < penalty_distances[next_row][next_col]:
                        distances[next_row][next_col] = new_distance
                        penalty_distances[next_row][next_col] = new_penalty_distance
                        parents[next_row][next_col] = current_position
                        heapq.heappush(queue, (new_penalty_distance, (next_row, next_col)))
                
    # Reconstruct the path
    path = []
    if penalty_distances[goal[0]][goal[1]] == float('inf'):
        return None, None  # No path found

    current = goal
    while current:
        path.append(current)
        current = parents[current[0]][current[1]]
        if current and 1 <= matrix[current[0]][current[1]] <= 7:
            value_count[matrix[current[0]][current[1]]] += 1
    path.reverse()

    end_time = time.time()  # Stop timing
    time_taken = end_time - start_time  # Calculate time taken
    
    return path, distances[goal[0]][goal[1]],time_taken, value_count
