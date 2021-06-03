from nhi_parser import Parser

# Create a parsing object
parser = Parser("../Data/data.vtk")

# Print it out in cube representation
print(parser.cube())