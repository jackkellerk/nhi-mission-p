import os
from nhi_parser import Parser

# Create a parsing object
if(not os.path.isfile("../Data/saved_data.pkl")):
    parser = Parser("../Data/data.vtk")
    parser.save("../Data/saved_data.pkl")
else:
    parser = Parser().load("../Data/saved_data.pkl")

# Print it out in cube representation
print(parser.cube())