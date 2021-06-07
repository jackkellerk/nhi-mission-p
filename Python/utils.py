"""
@author: houliang
"""

import numpy as np
import torch
import networkx as nx # one of python graph library

# transfer numpy array to torch tensor
def transferNumpy2Tensor(numpy_data, isFloat = True):
    if isFloat:
        tensor_data = torch.from_numpy(numpy_data).type('torch.FloatTensor')
    else:
        tensor_data = torch.from_numpy(numpy_data).type('torch.LongTensor')
    return tensor_data

# transfer adj and boundary matrix to networkx graph
def transferMatrix2Graph(adjacency_matrix, squares_boundary_matrix, subgraph_size=None):
    G=nx.Graph()
    n = adjacency_matrix.shape[0]
    if subgraph_size is not None:
        n = subgraph_size
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if adjacency_matrix[i,j]==1:
                G.add_edge(i,j,weight=squares_boundary_matrix[i,j])
    return G    

# save graph into one kind of format which can be imported into cytoscape
def saveGraph2GML(G, path, file_name="data_graph"):
    nx.readwrite.gml.write_gml(G, path+file_name+".gml")       

# generate the size of grain
def getGrainSize(data, max_id):
    size_matrix = np.zeros(shape=(max_id))
    for p_i in range(data.shape[0]):
        for p_j in range(data.shape[1]):
            for p_k in range(data.shape[2]):
                size_matrix[data[p_i, p_j, p_k]] += 1
    return size_matrix

# generate adjacent points around the center
def getAdjPoints4Loop(center_point, dims=3):
    i,j,k = center_point
    adj_p_list=[]
    for d in range(dims):
        for m in [1,-1]:
            center=[i,j,k]
            center[d]+=m
            adj_p_list.append(center)
    return adj_p_list        

# generate adj matrix
def getAdjacencyMatrix(data, max_id):
    adjacency_matrix = np.zeros(shape=(max_id, max_id))
    for p_i in range(data.shape[0]):
        for p_j in range(data.shape[1]):
            for p_k in range(data.shape[2]):
                adj_p_list = getAdjPoints4Loop([p_i,p_j,p_k])
                for adj_p in adj_p_list:
                    i,j,k = adj_p
                    if i>=0 and j>=0 and k>=0 and i<data.shape[0] and j<data.shape[1] and k<data.shape[2]: 
                        if data[p_i, p_j, p_k] != data[i, j, k]:
                            adjacency_matrix[data[p_i, p_j, p_k], data[i, j, k]] = 1
    return adjacency_matrix  

# generate adj matrix and boundary matrix. Still in progress to check its accuracy
def getAdjacencyMatrixAndBoundary(data, max_id):
    adjacency_matrix = np.zeros(shape=(max_id, max_id))
    squares_boundary_matrix = np.zeros(shape=(max_id, max_id))
    for p_i in range(data.shape[0]):
        for p_j in range(data.shape[1]):
            for p_k in range(data.shape[2]):
                adj_p_list = getAdjPoints4Loop([p_i,p_j,p_k])
                for adj_p in adj_p_list:
                    i,j,k = adj_p
                    if i>=0 and j>=0 and k>=0 and i<data.shape[0] and j<data.shape[1] and k<data.shape[2]: 
                        if data[p_i, p_j, p_k] != data[i, j, k]:
                            adjacency_matrix[data[p_i, p_j, p_k], data[i, j, k]] = 1
                            squares_boundary_matrix[data[p_i, p_j, p_k], data[i, j, k]] += 1
    return adjacency_matrix, squares_boundary_matrix

# generate adj matrix by considering the diagonal adjacency 
def getAdjacencyMatrixWithDiag(data, max_id):
    adjacency_matrix = np.zeros(shape=(max_id, max_id))
    for p_i in range(data.shape[0]):
        for p_j in range(data.shape[1]):
            for p_k in range(data.shape[2]):
                for i in range(p_i-1,p_i+2):
                    for j in range(p_j-1,p_j+2):
                        for k in range(p_k-1,p_k+2):
                            if i>=0 and j>=0 and k>=0 and i<data.shape[0] and j<data.shape[1] and k<data.shape[2]: 
                                if data[p_i, p_j, p_k] != data[i, j, k]:
                                    adjacency_matrix[data[p_i, p_j, p_k], data[i, j, k]] = 1
    return adjacency_matrix                              

# To generate boundary matrix. Still in progress to check its accuracy
# ---------------------------------------- 
def getSquareBoundary(data, max_id):
    squares_boundary_matrix = np.zeros(shape=(max_id, max_id))
    for p_i in range(data.shape[0]):
        for p_j in range(data.shape[1]):
            for p_k in range(data.shape[2]):
                adj_p_list = getAdjPoints4Loop([p_i,p_j,p_k])
                for adj_p in adj_p_list:
                    i,j,k = adj_p
                    if i>=0 and j>=0 and k>=0 and i<data.shape[0] and j<data.shape[1] and k<data.shape[2]: 
                        if data[p_i, p_j, p_k] != data[i, j, k]:
                            squares_boundary_matrix[data[p_i, p_j, p_k], data[i, j, k]] += 1
    return squares_boundary_matrix                            
# ---------------------------------------- 