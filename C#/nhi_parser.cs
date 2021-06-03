using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Globalization;
using System.Collections.Generic;

// This class is a parser for vtk files
public class Parser
{
    // Fields
    public string fileDir = null;
    public List<int> x = new List<int>();
    public List<int> y = new List<int>();
    public List<int> z = new List<int>();
    public List<int> cellData = new List<int>();
    public List<float> aveMobility = new List<float>();
    public List<float> aveEnergy = new List<float>();
    public List<int> gbCount = new List<int>();

    // Constructors    
    public Parser() {}
    public Parser(string fileDir)
    {        
        this.read(fileDir);
    }

    // Method to read a vtk file and parse it
    public void read(string fileDir)
    {
        // Updaate fileDir
        this.fileDir = fileDir;

        // Read from file using FileStream
        using (var fileStream = new FileStream(fileDir, FileMode.Open, FileAccess.Read))
        {
            string line;
            string currentRow = "";
            var streamReader = new StreamReader(fileStream, Encoding.UTF8);

            // Iterate over every line in the file        
            while((line = streamReader.ReadLine()) != null)
            {
                if(line == "" || line.Contains("SCALARS") || line.Contains("FIELD") || line.Contains("LOOKUP_TABLE"))
                    continue;                
                
                // Check to see if we need to update the list we are adding to
                if(line.Contains("X_COORDINATES"))
                {
                    currentRow = "X_COORDINATES";
                    continue;
                }        
                else if(line.Contains("Y_COORDINATES"))
                {
                    currentRow = "Y_COORDINATES";
                    continue;
                }
                else if(line.Contains("Z_COORDINATES"))
                {
                    currentRow = "Z_COORDINATES";
                    continue;
                }                    
                else if(line.Contains("CELL_DATA"))
                {  
                    currentRow = "CELL_DATA";
                    continue;
                }                    
                else if(line.Contains("AveMobility"))
                {
                    currentRow = "AveMobility";
                    continue;
                }                    
                else if(line.Contains("AveEnergy"))
                {
                    currentRow = "AveEnergy";
                    continue;
                }                    
                else if(line.Contains("GBcount"))
                {
                    currentRow = "GBcount";
                    continue;
                }                    

                // Check to see what list to add to
                switch(currentRow)
                {
                    case "X_COORDINATES":                        
                        x.Add(int.Parse(line, CultureInfo.InvariantCulture));
                        break;
                    case "Y_COORDINATES":
                        y.Add(int.Parse(line, CultureInfo.InvariantCulture));                
                        break;
                    case "Z_COORDINATES":
                        z.Add(int.Parse(line, CultureInfo.InvariantCulture));
                        break;
                    case "CELL_DATA":
                        cellData.Add(int.Parse(line, CultureInfo.InvariantCulture));
                        break;
                    case "AveMobility":
                        aveMobility.Add(float.Parse(line, CultureInfo.InvariantCulture));
                        break;
                    case "AveEnergy":
                        aveEnergy.Add(float.Parse(line, CultureInfo.InvariantCulture));
                        break;
                    case "GBcount":
                        gbCount.Add(int.Parse(line, CultureInfo.InvariantCulture));
                        break;
                    default:
                        break;
                }   
            }
        }

        // Index the grainbounds starting at zero
        for(int i = 0; i < cellData.Count; i++)
            cellData[i]--;
    }

    // Returns a three dimensional representation of the cellData field
    public int[,,] cube()
    {
        int[,,] cube = new int[x.Count - 1, y.Count - 1, z.Count - 1];

        for(int i = 0; i < x.Count - 1; i++)
            for(int j = 0; j < y.Count - 1; j++)
                for(int k = 0; k < z.Count - 1; k++)
                    cube[i, j, k] = cellData[(i * (x.Count - 2) * (y.Count - 2)) + (j * (x.Count - 2)) + k];

        return cube;
    }

    // Returns an adjacency matrix of all of the individual grainbounds    
    public int[,] adjacencyMatrix()
    {
        int[,,] cube = this.cube();        
        int maxValue = cellData.Max() + 1;
        int[,] adjacencyMatrix = new int[maxValue, maxValue];
        
        // Loop through each element in the cube
        for(int i = 0; i < cube.GetLength(0); i++)
        {
            for(int j = 0; j < cube.GetLength(1); j++)
            {
                for(int k = 0; k < cube.GetLength(2); k++)
                {                    
                    // Check all six sides of the selected element, if there is 
                    // an element from a different grainboundary, update the adjacency matrix                    

                    // Check the element in front of the current element
                    if(i - 1 >= 0)
                        if(cube[i, j, k] != cube[i - 1, j, k])
                            adjacencyMatrix[cube[i, j, k], cube[i - 1, j, k]] = 1;

                    // Check the element behind the current element
                    if(i + 1 < cube.GetLength(0))
                        if(cube[i, j, k] != cube[i + 1, j, k])
                            adjacencyMatrix[cube[i, j, k], cube[i + 1, j, k]] = 1;

                    // Check the element to the left of the current element
                    if(j - 1 >= 0)
                        if(cube[i, j, k] != cube[i, j - 1, k])
                            adjacencyMatrix[cube[i, j, k], cube[i, j - 1, k]] = 1;

                    // Check the element to the right of the current element
                    if(j + 1 < cube.GetLength(1))
                        if(cube[i, j, k] != cube[i, j + 1, k])
                            adjacencyMatrix[cube[i, j, k], cube[i, j + 1, k]] = 1;

                    // Check the element on top of the current element
                    if(k - 1 >= 0)
                        if(cube[i, j, k] != cube[i, j, k - 1])
                            adjacencyMatrix[cube[i, j, k], cube[i, j, k - 1]] = 1;

                    // Check the element on the bottom of the current element
                    if(k + 1 < cube.GetLength(2))
                        if(cube[i, j, k] != cube[i, j, k + 1])
                            adjacencyMatrix[cube[i, j, k], cube[i, j, k + 1]] = 1;                    
                }
            }
        }        

        return adjacencyMatrix;
    }

    // This returns a dictionary key pair of the number of the unique grainboundaries and the selected color it will be
    // Source: https://www.ijser.org/researchpaper/Graph-Coloring-Algorithm-using-Adjacency-Matrices.pdf
    public Dictionary<int, string> graphColoringDictionary()
    {        
        int[,] adjacencyMatrix = this.adjacencyMatrix();
        Dictionary<int, string> graphColoringDictionary = new Dictionary<int, string>();

        // TODO: Implement the graph coloring algorithm linked above
        // For now, this should suffice
        Random rand = new Random();
        for(int i = 0; i < adjacencyMatrix.GetLength(0); i++)
        {            
            string color = "#" + ((int)Math.Floor(rand.NextDouble()*16777215)).ToString("X6");
            graphColoringDictionary.Add(i, color);
        }

        return graphColoringDictionary;
    }

    // This returns cube() but instead of numbered grainbounds, each value is the hex color it should be
    public string[,,] coloredCube()
    {
        int[,,] cube = this.cube();        
        Dictionary<int, string> graphColoringDictionary = this.graphColoringDictionary();
        string[,,] coloredCube = new string[cube.GetLength(0), cube.GetLength(1), cube.GetLength(2)];

        for(int i = 0; i < cube.GetLength(0); i++)
            for(int j = 0; j < cube.GetLength(1); j++)
                for(int k = 0; k < cube.GetLength(2); k++)
                    coloredCube[i, j, k] = graphColoringDictionary[cube[i, j, k]];

        return coloredCube;
    }

    // Starting point
    public static void Main(string[] args)
    {
        // Create parser object
        Parser parser = new Parser("../Data/data.vtk");
        var coloredCube = parser.coloredCube();
    }
}