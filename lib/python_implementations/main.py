import pandas as pd
import os
from methods.ball_star_tree import BallStarTree
from utils.plotting import TreePlotter
from methods.median_split_ball_tree import MedianSplitBallTree

def main():
    # Double check the path to the dataset if you encounter a FileNotFoundError
    # Define the relative path to the dataset
    file_dir = os.path.dirname(__file__)  # Directory of the current Python file
    csv_path = os.path.join(file_dir, '..', '..', 'Datasets', 'csv', '2D_Moons.csv')  # Adjusted path

    # Load the dataset with headers
    df = pd.read_csv(csv_path)
    data = df.to_numpy()

    # Initialize and fit the Ball* Tree 
    # Note: Updated to match the new BallStarTree constructor signature
    ball_star_tree = BallStarTree(
        leaf_size=10,           # From BaseBallTree
        has_classification=True, # From BaseBallTree
        max_iterations=100,     # BallStarTree specific parameter
        alpha=0.5,              # BallStarTree specific parameter
        S=10                    # BallStarTree specific parameter
    )
    ball_star_tree.fit(data)  # Pass data to fit method

    # Define query point
    query_point = [0.5, 0.5]

    # K-Nearest Neighbors Query
    k = 5
    nearest_neighbors = ball_star_tree.knn_query(query_point, k)
    print(f"\n\n\n\nThe {k} nearest neighbors to {query_point} are:")
    print(nearest_neighbors)

    # Convert nearest_neighbors to just a list of points
    # Assuming the knn_query returns a list of tuples (distance, point)
    nearest_neighbors_points = [point[1] for point in nearest_neighbors]

    # Range Query
    radius = 0.5
    range_query_points = ball_star_tree.range_query(query_point, radius)
    print(f"\n\n\n\nThe points within a radius of {radius} from {query_point} are:")
    print(range_query_points)

    # Use the TreePlotter to visualize the results
    TreePlotter.plot_tree(
        ball_star_tree, 
        query_point=query_point, 
        knn_queried_points=nearest_neighbors_points, 
        range_queried_points=range_query_points, 
        radius=radius
    )
    
    # Median Split Ball Tree (to be implemented)
    # median_tree = MedianSplitBallTree(leaf_size=20)
    # median_tree.fit(X)

if __name__ == "__main__":
    main()