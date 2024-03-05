# version 2:
# change shortest path finding to shortest average path finding

from math import inf

def find_all(weighted_matrix, start, end=-1):
    """
    Returns a tuple with a distances' list and paths' list of
    all remaining vertices with the same indexing with a shorted average value finding.
    """
    n = len(weighted_matrix)

    # the initial distance list = [0, inf, inf, inf,... ,inf]
    dist = [inf]*n
    dist[start] = weighted_matrix[start][start]  
    
    # the initial distance list = [0, inf, inf, inf,... ,inf]
    dist_av = [inf]*n
    dist_av[start] = weighted_matrix[start][start]  
    
    # a list to note whether a vertex has been visited or not
    spVertex = [False]*n
    
    #create a list which contains paths for each vertex
    path_list = [[] for _ in range(n)]
    
    parent = [-1]*n

    # for each vertex, the latest updated shortest path 
    path = [{}]*n

    for count in range(n-1):
        
        minix = inf
        u = 0
        
        #find the shorted average distance so far and continue the calculation by selecting an unvisited vertex
        for v in range(len(spVertex)):
            if spVertex[v] == False and dist_av[v] <= minix:
                minix = dist_av[v]
                u = v
                
        # noting the vertex to be a visited one
        spVertex[u] = True
        
        # update the distance list with a newly visited vertex
        for v in range(n):
            if not(spVertex[v]) and weighted_matrix[u][v] != 0 and dist[u] + weighted_matrix[u][v] < dist[v]:
                parent[v] = u
                dist[v] = dist[u] + weighted_matrix[u][v]
                
                for i in range(len(path_list[u])):
                    path_list[v].append(path_list[u][i])
                path_list[v].append(u)
                
                dist_av[v] = dist[v]/len(path_list[v])

    for i in range(n):
        j = i
        s = []
        while parent[j] != -1:
            s.append(j)
            j = parent[j]
        s.append(start)
        path[i] = s[::-1]

    return (dist[end], path[end]) if end >= 0 else (dist, path)



def find_shortest_path(wmat, start, end=-1):
    """
    Returns paths' list of all remaining vertices.
    """
    return find_all(wmat, start, end)[1]



def find_shortest_distance(wmat, start, end=-1):
    """
    Returns distances' list of all remaining vertices.
    """
    return find_all(wmat, start, end)[0]

