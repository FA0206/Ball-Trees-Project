import numpy as np
from core.base_ball_tree import BaseBallTree
from core.ball_tree_node import BallTreeNode

"""
NOTE: This implementation will not match with the CPP implementation.
This is because the CPP implementation keeps a upper bound on the number of points in a node.
This implementation keeps keep splitting the node further until splitting results in a node with less than self.leaf_size points.
Which means, self.leaf_size is the lower bound on the number of points in a node
"""

class MedianSplitBallTree(BaseBallTree):
    def __init__(self, leaf_size=10, **kwargs):
        super().__init__(leaf_size=leaf_size, **kwargs)
        self.node_count = 0  # To track the number of nodes in the tree

    def fit(self, X, y=None):
        """
        Fit the Median Split Ball Tree on the data.
        """
        if self.has_classification and y is not None:
            self.data = np.column_stack((X, y))
        else:
            self.data = X

        self.root = BallTreeNode(data=self.data)
        self.volume = 0  # Initialize total volume
        self._median_split(self.root)
        
        # Print total tree statistics
        print(f"Total number of nodes: {self.node_count}")
        print(f"Total volume of the tree: {self.volume}")
        print(f"\nThe average depth of the tree is: {self.avg_leaf_depth()}")
        return self

    def _median_split(self, node):
        # Extract data points and handle classification mode
        if self.has_classification:
            full_data = node.data
            data = full_data[:, :-1]
        else:
            data = node.data

        # Increment the node count and print node details
        self.node_count += 1
        node.center, node.radius = self._calculate_center_and_radius(data)
        print(f"Node {self.node_count}: Center={node.center}, Radius={node.radius}, Points={data.shape[0]}")

        # Compute the median and farthest points
        median = np.median(data, axis=0)
        distances_to_median = np.linalg.norm(data - median, axis=1)
        farthest_point = data[np.argmax(distances_to_median)]
        distances_to_far_point = np.linalg.norm(data - farthest_point, axis=1)
        second_farthest_point = data[np.argmax(distances_to_far_point)]

        # Partition data
        left_indices = []
        right_indices = []

        for i, point in enumerate(data):
            if np.linalg.norm(point - farthest_point) <= np.linalg.norm(point - second_farthest_point):
                left_indices.append(i)
            else:
                right_indices.append(i)

        left_data = node.data[left_indices]
        right_data = node.data[right_indices]

        # Ensure both children have at least self.leaf_size points
        if left_data.shape[0] < self.leaf_size or right_data.shape[0] < self.leaf_size:
            return

        # Create and recursively split child nodes
        node.left = BallTreeNode(data=left_data)
        node.right = BallTreeNode(data=right_data)

        self._median_split(node.left)
        self._median_split(node.right)

        # Update volume for the current node
        self.volume += node.calculate_volume(data.shape[1])

    def _calculate_center_and_radius(self, data):
        """
        Calculates the center and radius for a given set of points.
        """
        center = np.mean(data, axis=0)
        radius = np.max(np.linalg.norm(data - center, axis=1))  # axis=1 calculates norm per row
        return center, radius
