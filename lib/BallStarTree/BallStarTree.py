import numpy as np
from math import *
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.cm as cm
import heapq

class BallTreeNode:
    def __init__(self, data=None, left=None, right=None, center=None, radius=None):
        self.data = data         # Data points at this node
        self.left = left         # Left child
        self.right = right       # Right child
        self.center = center     # Center of the ball
        self.radius = radius     # Radius of the ball
    
    def calculate_volume(self, current_dim):
        """
        Calculate the volume of the ball using recursive formula.
        This is done in O(d) time complexity where d is the dimension of the ball.
        """
        if current_dim == 0:
            return 1
        elif current_dim == 1:
            return 2 * self.radius
        else:
            return 2 * pi * (self.radius ** 2) * self.calculate_volume(current_dim - 2) / current_dim


class BallStarTree:
    def __init__(self, data, has_classification, leaf_size=10, max_iterations=100, alpha=0.5, S=10):
        self.root = None             # Root node of the tree
        self.data = data             # Initial dataset (n-dimensional points)
        self.leaf_size = leaf_size   # Threshold for leaf size
        self.max_iterations = max_iterations  # Power iteration convergence
        self.alpha = alpha           # Weight for objective function
        self.S = S                   # Number of intervals for splitting
        self.volume = 0              # To keep track of total volume of all balls
        self.has_classification = has_classification
    
    # Construction functions below:

    def fit(self):
        """
        Fit the Ball* Tree on the data.
        """
        self.root = BallTreeNode(data=self.data)
        print("Building the Ball* Tree...")

        # Double check if self.data.shape[1] works
        self._split_node(self.root)

        # Print the total volume and average depth of the tree
        print(f"Total volume of the tree: {self.volume}")
        print("\nThe average depth of the tree is: ", self.avg_leaf_depth())
    
        # Once tree has been built, print the structure and plot it (this works for any dimension)
        # self.print_tree(self.root)
        
    def _split_node(self, node, count = 0):
        """
        Recursively split the node into two children nodes. 
        The node is split along the principal component of the data points.
        The center and radius of the ball are calculated for each node (including leaves).
        The optimal split threshold is found using an objective function that balances the size of the two children nodes.
        """
        if (self.has_classification):
            full_data = node.data
            data = full_data[:, :-1]
        else:
            data = node.data
        # Calculate center and radius for every node, including leaves
        node.center, node.radius = self._calculate_center_and_radius(data)

        print("Node: \nPoints:", len(node.data))
        print("Center and Radius: ", node.center, node.radius)
        # Update the total volume of the tree
        self.volume += node.calculate_volume(data.shape[1])

        # Calculate the principal component
        principal_component = self.power_iteration(data)
        # Project the data points onto the principal component
        projections = data @ principal_component

        # Find the best threshold to split the data
        t_min, t_max = projections.min(), projections.max()
        N = len(projections)
        best_threshold = t_min
        min_objective = float('inf')
        optimal_N1, optimal_N2 = None, None

        # The objective function balances the size of the two children nodes
        # and the distance of the threshold from the center of the data
        for i in range(1, self.S):
            threshold = t_min + i * (t_max - t_min) / self.S
            N1 = np.sum(projections <= threshold)
            N2 = N - N1
            term1 = abs(N2 - N1) / N
            term2 = fabs(threshold - ((t_min + t_max) / 2)) / (t_max - t_min)
            objective_value = term1 + self.alpha * term2

            if objective_value < min_objective:
                min_objective = objective_value
                best_threshold = threshold
                optimal_N1, optimal_N2 = N1, N2

        # Split the data based on the best threshold
        if (self.has_classification):
            left_data = full_data[projections <= best_threshold]
            right_data = full_data[projections > best_threshold]
        else:
            left_data = data[projections <= best_threshold]
            right_data = data[projections > best_threshold]

        if len(left_data) < self.leaf_size or len(right_data) < self.leaf_size:
            return

        # Create left and right child nodes
        node.left = BallTreeNode(data=left_data)
        node.right = BallTreeNode(data=right_data)

        # To control the depth of the tree (uncomment below lines)
        # count += 1
        # if (count == 5):
        #     return

        # Recursively split child nodes
        self._split_node(node.left, count)
        self._split_node(node.right, count)

    def power_iteration(self, data):
        """
        This function performs the power iteration method to find the top principal component of the covariance matrix.
        """
        centered_data = data - np.mean(data, axis=0) # axis=0 makes sure the mean is along columns

        # Note: We're assume the data is normalized, i.e., zero mean and unit variance
        # Fix this later by adding a normalization step
        
        # Step 1: Compute covariance matrix
        covariance_matrix = np.cov(centered_data, rowvar=False)

        # Step 2: Power iteration on the covariance matrix to find the top principal component
        b_k = np.random.rand(covariance_matrix.shape[1])
        for _ in range(self.max_iterations):
            b_k1 = np.dot(covariance_matrix, b_k)
            b_k = b_k1 / np.linalg.norm(b_k1)
        
        return b_k

    def _calculate_center_and_radius(self, data):
        """
        Calculates the center and radius for a given set of points.
        """
        center = np.mean(data, axis=0) 
        radius = np.max(np.linalg.norm(data - center, axis=1))  # axis=1 calculates norm per row
        return center, radius

    # Plotting and printing functions below:

    def _plot_tree(self, node, ax, level=0, max_levels = 10):
        # Plot the circle for the current node
        if node is None:
            return

        # Define a colormap (e.g., 'viridis' or 'tab10') to vary colors by level
        cmap = cm.get_cmap('tab10', max_levels)  # Set max_levels based on expected tree depth

        # Draw the node's circle if it has a radius and center defined
        if node.radius is not None and node.center is not None:
            color = cmap(level % max_levels)  # Map the level to a color in the colormap
            circle = Circle(node.center, node.radius, color=color, fill=False, linestyle='-', linewidth=1)
            ax.add_patch(circle)
            # ax.plot(node.center[0], node.center[1], 'ro')  # Mark the center of the circle


        # Recursively plot left and right children
        if node.left is not None:
            self._plot_tree(node.left, ax, level + 1, max_levels)
        if node.right is not None:
            self._plot_tree(node.right, ax, level + 1, max_levels)

    def plot(self, query_point = None, knn_queried_points = None, range_queried_points = None, radius = None):
        # Check if the data is 2D
        if (self.data.shape[1] > 2 and not self.has_classification) or (self.data.shape[1] > 3 and self.has_classification):
            print("Plotting is supported only for 2D data.")
            return
        
        fig, ax = plt.subplots(figsize=(8, 8))

        if self.has_classification:
            # Separate data and labels
            data, labels = self.data[:, :-1], self.data[:, -1]
            unique_classes = np.unique(labels)
            
            # Limit the number of unique classes to 20
            if len(unique_classes) > 20:
                print("Too many unique classes to plot distinct colors (limit 20).")
                return
            
            # Use colormap 'tab20' or 'tab20b' for up to 20 distinct colors
            cmap = cm.get_cmap('tab20', len(unique_classes))
            colors = {cls: cmap(i) for i, cls in enumerate(unique_classes)}
            
            # Plot points with colors based on classification
            for cls in unique_classes:
                class_points = data[labels == cls]
                ax.scatter(class_points[:, 0], class_points[:, 1], s=10, color=colors[cls], label=f'Class {int(cls)}')
        else:
            # Plot all points in black if there is no classification
            ax.scatter(self.data[:, 0], self.data[:, 1], s=10, color='black', label='Data Points')
        
        if knn_queried_points is not None:
            # Plot queried points in red
            knn_queried_points = np.array(knn_queried_points)
            ax.scatter(knn_queried_points[:, 0], knn_queried_points[:, 1], s=30, color='red', label='Queried Points')
        
        if range_queried_points is not None and radius is not None:
            # Plot range circle in thick border and black as well as mention it in the legend
            circle = Circle(query_point, radius, color='black', fill=False, linestyle='-', linewidth=2)
            ax.add_patch(circle)

            if (range_queried_points == []):
                print("No elements found in the range query.")
            else:
                # Plot range queried points in beige
                range_queried_points = np.array(range_queried_points)
                ax.scatter(range_queried_points[:, 0], range_queried_points[:, 1], s=30, color='Orange', label='Range Queried Points')

        if query_point is not None:
            # Plot the query point in green
            ax.scatter(query_point[0], query_point[1], s=50, color='purple', label='Query Point')
        
        # Plot the tree recursively
        self._plot_tree(self.root, ax)

        # Set plot details
        ax.set_aspect('equal', 'box')
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.title("Ball* Tree Visualization")
        plt.legend()
        plt.show()

    def print_tree(self, node=None, depth=0):
        """
        Recursively prints the Ball* Tree structure with indentation representing depth.
        """
        if node is None:
            node = self.root
        
        # Print the current node's details
        indent = "  " * depth
        print(f"{indent}Depth {depth}, Points: {len(node.data)}, Radius: {node.radius}, Center: {node.center}")

        # Recursively print the left and right children, if they exist
        if node.left is not None:
            print(f"{indent}Left:")
            self.print_tree(node.left, depth + 1)
        if node.right is not None:
            print(f"{indent}Right:")
            self.print_tree(node.right, depth + 1)

    # Query functions below:

    def knn_query(self, query_point, k=1):
        """
        Query the Ball* Tree to find the k-nearest neighbors of a given query point.
        Uses a priority queue to keep track of the k-nearest neighbors found so far.
        Performs backtracking to explore other subtrees if there's a chance of finding closer neighbors.
        """
        # Priority queue to store the k-nearest neighbors (using max-heap to track the furthest neighbor in the list)
        # Set the knn_heap with one element with infinite distance
        knn_heap = [(-float('inf'), None)]
        
        # Recursive function to perform search and backtracking
        def search_node(node):
            if node is None:
                return
            
            # print("Searching node with", len(node.data), "points")
            # print("The points are: ", node.data)

            # Calculate distance from query point to the node's center
            distance_to_center = np.linalg.norm(query_point - node.center)
            
            # If this is a leaf node, or the query point is outside the node's children's balls, evaluate all the points in the node
            if (node.left is None and node.right is None):
                # print("FOUND A LEAF")
                if ((len(knn_heap) < k) or distance_to_center - node.radius < -knn_heap[0][0]):
                    # print("Distance to center - radius and max element of the heap: ", distance_to_center - node.radius, -knn_heap[0][0])
                    # print("and the heap is not full or the distance to surface from query is lesser than the farthest neighbor in heap")
                    for point in node.data:
                        if (not self.has_classification):
                            dist = np.linalg.norm(query_point - point)
                        else:
                            dist = np.linalg.norm(query_point - point[:-1])

                        # Maintain a heap of size k for the k-nearest neighbors
                        if len(knn_heap) < k:
                            heapq.heappush(knn_heap, (-dist, point))
                            # print("Added a point to the heap: ", point)
                        else:
                            # Only add closer neighbors to the heap
                            if dist < -knn_heap[0][0]:  # knn_heap[0] is the farthest neighbor in the current heap
                                heapq.heapreplace(knn_heap, (-dist, point))
                                # print("Added a point to the heap: ", point)

                    # print("Heap after leaf search: ", knn_heap)
                    # print("Heap length: ", len(knn_heap))
                else:
                    print("Skipping the leaf of size ", len(node.data))
                return
            else:
                pass
                # print("NOT A LEAF or (the heap is full and the distance to surface from query is greater than the farthest neighbor in heap)")

            # Check if the current node's ball might contain closer points than the furthest neighbor
            if len(knn_heap) < k or distance_to_center - node.radius < -knn_heap[0][0]:
                # print("Distance to center - radius and max element of the heap: ", distance_to_center - node.radius, -knn_heap[0][0])
                # print("Exploring the internal node...")
                # Traverse the closer child first
                if np.linalg.norm(query_point - node.left.center) <= np.linalg.norm(query_point - node.right.center):
                    search_node(node.left)
                    search_node(node.right)
                else:
                    search_node(node.right)
                    search_node(node.left)
            else:
                print("Skipping the node of size ", len(node.data))

        # Start the search from the root node
        search_node(self.root)

        # Return sorted list of nearest neighbors by distance
        return knn_heap

    def range_query(self, query_point, range):
        """
        Query the Ball* Tree to find all points within a given range of a query point.
        Performs backtracking to explore other subtrees if there's a chance of finding points within the range.
        """
        points_in_range = []
        def search_node(node):
            if node is None:
                return
            distance_to_center = np.linalg.norm(query_point - node.center)

            if (distance_to_center - node.radius > range):
                if (node.left is None and node.right is None):
                    print("Skipping the leaf of size ", len(node.data))
                else:
                    print("Skipping the node of size ", len(node.data))
                return
            
            if (node.left is None and node.right is None):
                for point in node.data:
                    if (not self.has_classification):
                        dist = np.linalg.norm(query_point - point)
                    else:
                        dist = np.linalg.norm(query_point - point[:-1])

                    if dist <= range:
                        points_in_range.append(point)
                return

            if (np.linalg.norm(query_point - node.left.center) <= np.linalg.norm(query_point - node.right.center)):
                search_node(node.left)
                search_node(node.right)
            else:
                search_node(node.right)
                search_node(node.left)

        print("Starting the range query...")
        search_node(self.root)
        print("Range query completed.")

        return points_in_range

    # Analysis functions below:

    def avg_leaf_depth(self):
        """
        Calculate the average depth of the leaves in the Ball* Tree.
        """
        sum_depth = 0
        num_leaves = 0

        # Perform a DFS traversal to calculate the sum of depths and number of leaves
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            if node.left is None and node.right is None:
                sum_depth += depth
                num_leaves += 1
            if node.left is not None:
                stack.append((node.left, depth + 1))
            if node.right is not None:
                stack.append((node.right, depth + 1))

        return sum_depth / num_leaves