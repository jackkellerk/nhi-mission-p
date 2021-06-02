from nhi_parser import Parser

print("This will take about 10 minutes to fully run. \
       I recommend you use the save and load functions \
       to speed up the parsing process!")

# Create a parsing object
parser = Parser("data.vtk")

# Encode the data as a pkl file for reference later
parser.save("encoded_data")

# Print it out
print(parser.cell_data)