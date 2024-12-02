import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot2DGraph(csv_file):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)
    
    # Check if the file contains 'X' and 'Y' columns
    if 'Feature1' in data.columns and 'Feature2' in data.columns:
        # Plot the data
        plt.scatter(data['Feature1'], data['Feature2'])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('2D Scatter Plot')
        plt.show()
    else:
        print("The CSV file is not two dimensional!")
   

def plot_3d_blobs(csv_file):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)
    
    # Check if the file contains 'X', 'Y', and 'Z' columns
    if 'Feature1' in data.columns and 'Feature2' in data.columns and 'Feature3' in data.columns:
        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the data
        ax.scatter(data['Feature1'], data['Feature2'], data['Feature3'])

        # Label the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Scatter Plot')

        # Show the plot
        plt.show()
    else:
        print("The CSV file does not contain 'X', 'Y', and 'Z' columns.")

def plot2DCircle(fname, scatterFileName):
  data = pd.read_csv(fname)
  data1 = pd.read_csv(scatterFileName)

  figure, axes = plt.subplots()

  for i in range (0, len(data), 1):
    x1 = data['Center1'][i]
    x2 = data['Center2'][i]
    r = data['Radius'][i]

    circle = plt.Circle((x1, x2), r, fill=False)

    axes.add_artist(circle)
  
  if 'Feature1' in data1.columns and 'Feature2' in data1.columns:
        plt.scatter(data1['Feature1'], data1['Feature2'], s=3)
  else:
        print("The CSV file is not two dimensional!")
  
  axes.set_aspect(1)
  plt.xlim(-2, 3)
  plt.ylim(-1.5, 1.75)
  plt.title("Ball Trees Circles")
  plt.show()



# plot2DCircle('testResults.csv', "Datasets/csv/2D_Moons.csv")

'''
# Usage example:
plot_3d_blobs('3D_Swiss_Roll.csv')

# Usage example:
plot2DGraph('2D_Blobs.csv')
'''
