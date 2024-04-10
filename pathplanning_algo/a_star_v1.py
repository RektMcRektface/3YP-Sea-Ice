import numpy as np
import heapq
import functions_v2
import math

################################## 4 directions ################################################
def heuristic_4(a, b):
    # Manhattan distance on a square grid
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def a_star_search_4(matrix, start, goal, limit):
    neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)] # Right, Down, Left, Up
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic_4(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data, gscore[goal]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            if 0 <= neighbor[0] < matrix.shape[0]:
                if 0 <= neighbor[1] < matrix.shape[1]:
                    if matrix[neighbor[0]][neighbor[1]] <= limit:
                        if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                            continue
                        
                        if  tentative_g_score < gscore.get(neighbor, np.inf) or neighbor not in [i[1]for i in oheap]:
                            came_from[neighbor] = current
                            gscore[neighbor] = tentative_g_score
                            fscore[neighbor] = tentative_g_score + heuristic_4(neighbor, goal)
                            heapq.heappush(oheap, (fscore[neighbor], neighbor))
                    else:
                        continue
                else:
                    # Array bounds y walls
                    continue
            else:
                # Array bounds x walls
                continue

    return False

######################################### 8 directions ##############################################
def heuristic_8(a, b):
    # Diagonal distance on a square grid
    dx = abs(b[0] - a[0])
    dy = abs(b[1] - a[1])
    h = 1 * (dx + dy) + (math.sqrt(2) - 2 * 1) * min(dx, dy)
    return h

def a_star_search_8(matrix, start, goal, limit):
    neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1),(1,1),(-1,-1),(1,-1),(-1,1)] # Right, Down, Left, Up,right-down,left-up,right-up,left-down
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic_8(start, goal)}
    oheap = []
    distance = 0
    
    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data, gscore[goal]

        close_set.add(current)
        
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            
            if 0 <= neighbor[0] < matrix.shape[0]:
                
                if 0 <= neighbor[1] < matrix.shape[1]:
                    if i !=0 and j != 0: # diagonal directions
                        tentative_g_score = gscore[current] + math.sqrt(2)
                        if matrix[neighbor[0]][neighbor[1]] <= limit:
                            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                                continue
                            
                            if  tentative_g_score < gscore.get(neighbor, np.inf) or neighbor not in [i[1]for i in oheap]:
                                came_from[neighbor] = current
                                gscore[neighbor] = tentative_g_score
                                fscore[neighbor] = tentative_g_score + heuristic_8(neighbor, goal)
                                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                        else:
                            continue
                    else:# vertical or horizontal directions
                        tentative_g_score = gscore[current] + 1
                        if matrix[neighbor[0]][neighbor[1]] <= limit:
                            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                                continue
                            
                            if  tentative_g_score < gscore.get(neighbor, np.inf) or neighbor not in [i[1]for i in oheap]:
                                came_from[neighbor] = current
                                gscore[neighbor] = tentative_g_score
                                fscore[neighbor] = tentative_g_score + heuristic_8(neighbor, goal)
                                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                        else:
                            continue
                else:
                    # Array bounds y walls
                    continue
            else:
                # Array bounds x walls
                continue

    return False
