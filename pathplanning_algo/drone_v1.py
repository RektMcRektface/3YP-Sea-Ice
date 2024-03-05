import numpy as np

#This code:
#Uses flood_fill to recursively find and group adjacent cells that meet the high-value criterion.
#Computes the mean of the coordinates in each cluster to find its center.
#Assumes a rectangular (non-ragged) numpy array as input for the matrix.

def find_high_value_centers(matrix, value_threshold):
    nrows, ncols = matrix.shape
    visited = np.zeros_like(matrix, dtype=bool)
    clusters = []

    def flood_fill(r, c):
        if r < 0 or r >= nrows or c < 0 or c >= ncols:
            return []
        if visited[r, c] or matrix[r][c] < value_threshold:
            return []
        visited[r, c] = True
        cluster = [(r, c)]
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in directions:
            cluster.extend(flood_fill(r + dr, c + dc))
        return cluster

    for r in range(nrows):
        for c in range(ncols):
            if matrix[r][c] >= value_threshold and not visited[r][c]:
                cluster = flood_fill(r, c)
                if cluster:
                    clusters.append(cluster)

    cluster_centers = []
    for cluster in clusters:
        cluster_centers.append(np.mean(cluster, axis=0))

    return cluster_centers

# simple_matrix = np.array([
#     # Your matrix values here
# ])

# value_threshold = 8  # Define what you consider a "high" value
# centers = find_high_value_centers(simple_matrix, value_threshold)
# print("Centers of high value areas:", centers)