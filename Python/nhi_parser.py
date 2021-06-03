import numpy as np
import pandas as pd

# Object class parser
class Parser:
    def __init__(self, file_name=None):
        # Columns in pandas df. These are also fields in this class
        self.x_coordinates = []
        self.y_coordinates = []
        self.z_coordinates = []
        self.cell_data = []
        self.ave_mobility = []
        self.ave_energy = []
        self.gb_count = []
        self.df = pd.DataFrame()
        self.file_name = file_name

        # Call parse function
        if file_name != None:
            self.parse(file_name)

    # Parses the VTK file into a df
    def parse(self, file_name):
        # Used to determine what column we are adding to
        current_row = ""

        # Open the file and iterate over every line
        with open(file_name, "r") as f:
            for line in f:
                # Get the line in string form
                line = line.strip()

                # If line is empty or contains descriptive information, continue
                if line == "" or "SCALARS" in line or "FIELD" in line or "LOOKUP_TABLE" in line:
                    continue

                # Check to see what column we are adding to
                if "X_COORDINATES" in line:
                    current_row = "X_COORDINATES"
                    continue
                elif "Y_COORDINATES" in line:
                    current_row = "Y_COORDINATES"
                    continue
                elif "Z_COORDINATES" in line:
                    current_row = "Z_COORDINATES"
                    continue
                elif "CELL_DATA" in line:
                    current_row = "CELL_DATA"
                    continue
                elif "AveMobility" in line:
                    current_row = "AveMobility"
                    continue
                elif "AveEnergy" in line:
                    current_row = "AveEnergy"
                    continue
                elif "GBcount" in line:
                    current_row = "GBcount"
                    continue

                # Determine what column we are adding to
                if current_row == "X_COORDINATES":
                    self.x_coordinates.append(float(line.strip()))
                elif current_row == "Y_COORDINATES":
                    self.y_coordinates.append(float(line.strip()))
                elif current_row == "Z_COORDINATES":
                    self.z_coordinates.append(float(line.strip()))
                elif current_row == "CELL_DATA":
                    self.cell_data.append(float(line.strip()))
                elif current_row == "AveMobility":
                    self.ave_mobility.append(float(line.strip()))
                elif current_row == "AveEnergy":
                    self.ave_energy.append(float(line.strip()))
                elif current_row == "GBcount":
                    self.gb_count.append(float(line.strip()))
        
        # Index the grainbounds starting at zero
        for i in range(len(self.cell_data)):
            self.cell_data[i] -= 1

        # Format the data into pd Series
        self.x_coordinates = pd.Series(self.x_coordinates, name="X_COORDINATES")
        self.y_coordinates = pd.Series(self.y_coordinates, name="Y_COORDINATES")
        self.z_coordinates = pd.Series(self.z_coordinates, name="Z_COORDINATES")
        self.cell_data = pd.Series(self.cell_data, name="CELL_DATA")
        self.ave_mobility = pd.Series(self.ave_mobility, name="AVE_MOBILITY")
        self.ave_energy = pd.Series(self.ave_energy, name="AVE_ENERGY")
        self.gb_count = pd.Series(self.gb_count, name="GB_COUNT")

        # Format the series into a df
        self.df = pd.concat([self.x_coordinates, self.y_coordinates, self.z_coordinates, self.cell_data, self.ave_mobility, self.ave_energy, self.gb_count], axis=1)
        return self.df

    # Returns the cell_data into a three dimensional array or a cube
    def cube(self):
        cube = np.ndarray(shape=((self.x_coordinates).size - 1, (self.y_coordinates).size - 1, (self.z_coordinates).size - 1))        

        for i in range((self.x_coordinates).size - 1):
            for j in range((self.y_coordinates).size - 1):
                for k in range((self.z_coordinates).size - 1):
                    cube[i, j, k] = self.cell_data[(i * ((self.x_coordinates).size - 2) * ((self.y_coordinates).size - 2)) + (j * ((self.z_coordinates).size - 2)) + k]
        
        return cube
    
    # Returns the adjacency_matrix
    def adjacency_matrix(self):
        cube = self.cube()
        max_value = int(max(self.cell_data) + 1)
        adjacency_matrix = np.zeros(shape=(max_value, max_value))
        
        # Loop through each element in the cube
        for i in range(cube.shape[0]):
            for j in range(cube.shape[1]):
                for k in range(cube.shape[2]):
                    # Check all six sides of the selected element, if there is 
                    # an element from a different grainboundary, update the adjacency matrix    
 
                    # Check the element in front of the current element
                    if(i - 1 >= 0):
                        if(cube[i, j, k] != cube[i - 1, j, k]):
                            adjacency_matrix[int(cube[i, j, k]), int(cube[i - 1, j, k])] = 1

                    # Check the element behind the current element
                    if(i + 1 < cube.shape[0]):
                        if(cube[i, j, k] != cube[i + 1, j, k]):
                            adjacency_matrix[int(cube[i, j, k]), int(cube[i + 1, j, k])] = 1

                    # Check the element to the left of the current element
                    if(j - 1 >= 0):
                        if(cube[i, j, k] != cube[i, j - 1, k]):
                            adjacency_matrix[int(cube[i, j, k]), int(cube[i, j - 1, k])] = 1

                    # Check the element to the right of the current element
                    if(j + 1 < cube.shape[1]):
                        if(cube[i, j, k] != cube[i, j + 1, k]):
                            adjacency_matrix[int(cube[i, j, k]), int(cube[i, j + 1, k])] = 1

                    # Check the element on top of the current element
                    if(k - 1 >= 0):
                        if(cube[i, j, k] != cube[i, j, k - 1]):
                            adjacency_matrix[int(cube[i, j, k]), int(cube[i, j, k - 1])] = 1

                    # Check the element on the bottom of the current element
                    if(k + 1 < cube.shape[2]):
                        if(cube[i, j, k] != cube[i, j, k + 1]):
                            adjacency_matrix[int(cube[i, j, k]), int(cube[i, j, k + 1])] = 1

        return adjacency_matrix

    # Saves the df into a pkl file
    def save(self, file_name=None, directory=None):
        if file_name == None:
            file_name = self.file_name
        
        if directory == None:
            directory = "./"
        
        if(".pkl" in file_name):
            self.df.to_pickle(directory + file_name)
        else:
            self.df.to_pickle(directory + file_name + ".pkl")

    # Loads the df from a pkl file
    def load(self, file_name):        
        self.file_name = file_name[0:len(file_name) - 4] + ".vtk"
        self.df = pd.read_pickle(file_name)
        self.x_coordinates = self.df.T.iloc[0]
        self.y_coordinates = self.df.T.iloc[1]
        self.z_coordinates = self.df.T.iloc[2]
        self.cell_data = self.df.T.iloc[3]
        self.ave_mobility = self.df.T.iloc[4]
        self.ave_energy = self.df.T.iloc[5]
        self.gb_count = self.df.T.iloc[6]