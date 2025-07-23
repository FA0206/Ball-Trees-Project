from core.base_ball_tree import BaseBallTree
from core.ball_tree_node import BallTreeNode

import numpy as np
from math import *

class BallStarTree(BaseBallTree):
    # Note: data isn't directly passed to the constructor, but is passed to the fit method
    def __init__(self, max_iterations=10, alpha=0.5, S=10, **kwargs):
        super().__init__(**kwargs)
        self.max_iterations = max_iterations
        self.alpha = alpha
        self.S = S

    def fit(self, X, y=None):
        """
        Fit the Ball* Tree on the data.
        """
        self.data = X if y is None else np.column_stack((X, y))

        self.root = BallTreeNode(data=self.data)

        self._pca_split_node(self.root)

        # Print total tree statistics
        print(f"Total number of nodes: {self.node_count}")
        print(f"Total volume of the tree: {self.volume}")
        avg_depth, max_depth = self.calculate_tree_depth()
        print(f"\nThe average depth and max depth of the tree is: {avg_depth} and {max_depth}")
        return self
        
    def _pca_split_node(self, node, count = 0):
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

        self.node_count += 1
        # Calculate center and radius for every node, including leaves
        node.center, node.radius = self._calculate_center_and_radius(data)

        print(f"Node {self.node_count}: Center = {node.center}, Radius = {node.radius}, Points = {data.shape[0]}")
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
        self._pca_split_node(node.left, count)
        self._pca_split_node(node.right, count)

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