import numpy as np
import heapq
import functions_v2

def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def a_star_search(matrix, start, goal):
    neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)] # Right, Down, Left, Up
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + matrix[current[0]][current[1]]
            if 0 <= neighbor[0] < matrix.shape[0]:
                if 0 <= neighbor[1] < matrix.shape[1]:
                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue
                    
                    if  tentative_g_score < gscore.get(neighbor, np.inf) or neighbor not in [i[1]for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))
                else:
                    # Array bounds y walls
                    continue
            else:
                # Array bounds x walls
                continue

    return False


# simple_matrix = np.array([[1 ,2 ,2 ,3 ,4 ,4 ,4 ,8 ,9 ,10,10,9 ,7 ,5 ,4 ,4 ,2 ,4 ,3 ,3 ,2 ,5 ,6 ,8 ,4 ],
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
#                  ])

# start = (0, 0) # Top-left corner
# goal = (simple_matrix.shape[0]-1, simple_matrix.shape[1]-1) # Bottom-right corner
# path = a_star_search(simple_matrix, start, goal)

# # Convert path to a more readable format
# path = path[::-1]  # Reverse path to start from the beginning
# print(path)

# max_risk_value = 10

# functions_v2.overall_visualisation(simple_matrix, max_risk_value, path)
