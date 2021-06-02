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

        # Since cell_data is filled with arbitrary numbers, we need to convert them into consecutive numbers
        unique_values = []
        for i in range(len(self.cell_data)):            
            if(self.cell_data[i] not in unique_values):
                unique_values.append(self.cell_data[i])

        unique_values.sort()
        
        for i in range(len(self.cell_data)):            
            for j in range(len(unique_values)):
                if(self.cell_data[i] == unique_values[j]):
                    self.cell_data[i] = j

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

    # Saves the df into a pkl file
    def save(self, file_name=None, directory=None):
        if file_name == None:
            file_name = self.file_name
        
        if directory == None:
            directory = "./"
        
        self.df.to_pickle(directory + file_name[0:len(file_name) - 4] + ".pkl")

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