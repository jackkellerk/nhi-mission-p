import os.path
from nhi_parser import Parser

# Create a parsing object
if(os.path.isfile("encoded_data.pkl")):
       parser = Parser().load("encoded_data.pkl")
else:
       parser = Parser("../Data/data.vtk")
       parser.save("encoded_data")

# Print it out
print(parser.cell_data)