import heapq
import math

###################### 4 directions #######################################
def dijkstra_path_4(matrix, limit):
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
    path.reverse()  # The path was constructed backwards, so reverse it
    
    return path, distances[goal[0]][goal[1]]




############################# 8 directions ###########################################
def dijkstra_path_8(matrix,limit):
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
    path.reverse()  # The path was constructed backwards, so reverse it
    
    return path, distances[goal[0]][goal[1]]