import os.path
from nhi_parser import Parser

print("This will take about 10 minutes to fully run. \
       I recommend you use the save and load functions \
       to speed up the parsing process!")

# Create a parsing object
if(os.path.isfile("encoded_data.pkl")):
       parser = Parser().load("encoded_data.pkl")
else:
       parser = Parser("data.vtk")
       parser.save("encoded_data")

# Print it out
print(parser.cell_data)