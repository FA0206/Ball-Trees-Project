import pandas as pd
import os
from methods.ball_star_tree import BallStarTree
from utils.plotting import TreePlotter
from methods.median_split_ball_tree import MedianSplitBallTree

# Define relative path to dataset
def get_dataset_path():
    file_dir = os.path.dirname(__file__)
    return os.path.join(file_dir, '..', '..', 'Datasets', 'csv', '2D_Moons.csv')

# Load dataset
def load_dataset(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df.to_numpy()
    except FileNotFoundError:
        print(f"❌ Dataset not found at {csv_path}. Please check the path.")
        exit()

# Build and fit a tree
def build_tree(tree_type, data, **kwargs):
    print(f"\n{'='*50}")
    print(f"🛠️ Building {tree_type.__name__}...")
    tree = tree_type(**kwargs)
    tree.fit(data)
    print(f"✅ {tree_type.__name__} has been successfully built.\n{'='*50}")
    return tree

# Perform KNN and range queries
def perform_queries(tree, query_point, k, radius):
    print(f"\n{'='*50}")
    print(f"🔍 Querying the {type(tree).__name__}...")
    
    # KNN Query
    nearest_neighbors = tree.knn_query(query_point, k)
    print(f"\nThe {k} nearest neighbors to {query_point} are:")
    print(f"{'='*50}")
    for i, neighbor in enumerate(nearest_neighbors):
        print(f"{i+1}. {neighbor[1]} (Distance: {neighbor[0]:.2f})")
    
    # Range Query
    range_query_points = tree.range_query(query_point, radius)
    print(f"\nThe points within a radius of {radius} from {query_point} are:")
    print(f"{'='*50}")
    if range_query_points:
        for i, point in enumerate(range_query_points):
            print(f"{i+1}. {point}")
    else:
        print(f"No points found within the radius of {radius}.")
    
    print(f"{'='*50}")
    return [point[1] for point in nearest_neighbors], range_query_points

# Main function to handle the workflow
def main():
    print("🌟 Starting the Ball Tree Visualization Workflow 🌟")
    print(f"{'='*50}")
    
    # Define dataset path and load data
    csv_path = get_dataset_path()
    print(f"🔄 Loading dataset from: {csv_path}")
    data = load_dataset(csv_path)

    # Query parameters
    query_point = [0.5, 0.5]
    k = 5
    radius = 0.5

    # Build both trees
    median_tree = build_tree(MedianSplitBallTree, data, leaf_size=5, has_classification=True)
    ball_star_tree = build_tree(
        BallStarTree, 
        data, 
        leaf_size=5, 
        has_classification=True, 
        max_iterations=100, 
        alpha=0.5, 
        S=10
    )

    # Perform queries on the Median Split Ball Tree
    median_knn_points, median_range_points = perform_queries(median_tree, query_point, k, radius)

    # Perform queries on the Ball* Tree
    ball_star_knn_points, ball_star_range_points = perform_queries(ball_star_tree, query_point, k, radius)

    # Plot both trees side by side
    print("\n🎨 Visualizing both trees side by side...")
    print(f"{'='*50}")
    TreePlotter.plot_side_by_side(
        median_tree,
        ball_star_tree,
        query_point=query_point,
        knn_queried_points_1=median_knn_points,
        range_queried_points_1=median_range_points,
        knn_queried_points_2=ball_star_knn_points,
        range_queried_points_2=ball_star_range_points,
        radius=radius,
    )
    
    print(f"\n{'='*50}")
    print("✅ Workflow completed successfully!")

if __name__ == "__main__":
    main()
