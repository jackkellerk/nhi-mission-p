import numpy as np

# Get the adjacency matrix from the front face
def front_face(cube):
    max_value = int(np.amax(cube) + 1)
    adjacency_matrix = np.zeros(shape=(max_value, max_value))

    # Loop through each element in the cube
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):  
                # Check the element in front of the current element
                if(i - 1 >= 0):
                    if(cube[i, j, k] != cube[i - 1, j, k]):
                        adjacency_matrix[int(cube[i, j, k]), int(cube[i - 1, j, k])] = 1

    return adjacency_matrix

# Get the adjacency matrix from the back face
def back_face(cube):
    max_value = int(np.amax(cube) + 1)
    adjacency_matrix = np.zeros(shape=(max_value, max_value))

    # Loop through each element in the cube
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):  
                # Check the element behind the current element
                if(i + 1 < cube.shape[0]):
                    if(cube[i, j, k] != cube[i + 1, j, k]):
                        adjacency_matrix[int(cube[i, j, k]), int(cube[i + 1, j, k])] = 1

    return adjacency_matrix

# Get the adjacency matrix from the back face
def right_face(cube):
    max_value = int(np.amax(cube) + 1)
    adjacency_matrix = np.zeros(shape=(max_value, max_value))

    # Loop through each element in the cube
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):  
                # Check the element to the left of the current element
                if(j - 1 >= 0):
                    if(cube[i, j, k] != cube[i, j - 1, k]):
                        adjacency_matrix[int(cube[i, j, k]), int(cube[i, j - 1, k])] = 1

    return adjacency_matrix

# Get the adjacency matrix from the back face
def left_face(cube):
    max_value = int(np.amax(cube) + 1)
    adjacency_matrix = np.zeros(shape=(max_value, max_value))

    # Loop through each element in the cube
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):  
                # Check the element to the right of the current element
                if(j + 1 < cube.shape[1]):
                    if(cube[i, j, k] != cube[i, j + 1, k]):
                        adjacency_matrix[int(cube[i, j, k]), int(cube[i, j + 1, k])] = 1

    return adjacency_matrix

# Get the adjacency matrix from the back face
def top_face(cube):
    max_value = int(np.amax(cube) + 1)
    adjacency_matrix = np.zeros(shape=(max_value, max_value))

    # Loop through each element in the cube
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):  
                # Check the element on top of the current element
                if(k - 1 >= 0):
                    if(cube[i, j, k] != cube[i, j, k - 1]):
                        adjacency_matrix[int(cube[i, j, k]), int(cube[i, j, k - 1])] = 1

    return adjacency_matrix

# Get the adjacency matrix from the back face
def bottom_face(cube):
    max_value = int(np.amax(cube) + 1)
    adjacency_matrix = np.zeros(shape=(max_value, max_value))

    # Loop through each element in the cube
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):  
                # Check the element on the bottom of the current element
                if(k + 1 < cube.shape[2]):
                    if(cube[i, j, k] != cube[i, j, k + 1]):
                        adjacency_matrix[int(cube[i, j, k]), int(cube[i, j, k + 1])] = 1

    return adjacency_matrix