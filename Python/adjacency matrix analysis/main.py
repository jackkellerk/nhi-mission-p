# Add NHI-Mission-P to folder of dependencies
import os, sys
path = os.getcwd()[:len(os.getcwd()) - os.getcwd()[::-1].index("\\")]
sys.path.insert(1, path)

# Import the actual dependencies
from nhi_parser import Parser
import analysis_utils as adjacency_matrix

parser = Parser("../../Data/data.vtk")
cube = parser.cube()

# Front facing adjacency matrix function
front_face = adjacency_matrix.front_face(cube)

# Back facing adjacency matrix function
back_face = adjacency_matrix.back_face(cube)

# Right facing adjacency matrix function
right_face = adjacency_matrix.right_face(cube)

# Left facing adjacency matrix function
left_face = adjacency_matrix.left_face(cube)

# top facing adjacency matrix function
top_face = adjacency_matrix.top_face(cube)

# Bottom facing adjacency matrix function
bottom_face = adjacency_matrix.bottom_face(cube)

# Add all of them up
total_matrix = front_face + back_face + right_face + left_face + top_face + bottom_face

# Test the adjacency matrices
print((total_matrix == parser.adjacency_matrix()).all())

# Remove the path added to the system
sys.path.remove(path)