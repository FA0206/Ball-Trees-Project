import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Circle
import numpy as np

class TreePlotter:
    @staticmethod
    def plot_tree(tree, query_point=None, knn_queried_points=None, 
                  range_queried_points=None, radius=None):
        """
        Static method to plot the Ball Tree visualization.
        Works with any Ball Tree instance that follows the original structure.
        
        Args:
            tree: Ball Tree instance
            query_point: Optional point for query visualization
            knn_queried_points: Optional k-nearest neighbor points
            range_queried_points: Optional points from range query
            radius: Optional radius for range query
        """
        # Check dimensionality - directly using the method from your original implementation
        if (tree.data.shape[1] > 2 and not tree.has_classification) or \
           (tree.data.shape[1] > 3 and tree.has_classification):
            print("Plotting is supported only for 2D data.")
            return
        
        fig, ax = plt.subplots(figsize=(8, 8))

        # Data point plotting logic (from your original method)
        TreePlotter._plot_data_points(tree, ax)
        
        # Additional plotting elements
        if range_queried_points is not None and radius is not None:
            TreePlotter._plot_range_query(ax, query_point, range_queried_points, radius)

        if knn_queried_points is not None:
            TreePlotter._plot_knn_points(ax, knn_queried_points)

        if query_point is not None:
            TreePlotter._plot_query_point(ax, query_point)
        
        # Plot the tree structure
        TreePlotter._plot_tree_structure(tree.root, ax)

        # Finalize plot
        ax.set_aspect('equal', 'box')
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.title("Ball* Tree Visualization")
        plt.legend()
        plt.show()

    @staticmethod
    def _plot_data_points(tree, ax):
        """Plot data points, handling classification if present"""
        if tree.has_classification:
            data, labels = tree.data[:, :-1], tree.data[:, -1]
            unique_classes = np.unique(labels)
            
            if len(unique_classes) > 20:
                print("Too many unique classes to plot distinct colors (limit 20).")
                return
            
            cmap = cm.get_cmap('tab20', len(unique_classes))
            colors = {cls: cmap(i) for i, cls in enumerate(unique_classes)}
            
            for cls in unique_classes:
                class_points = data[labels == cls]
                ax.scatter(class_points[:, 0], class_points[:, 1], 
                           s=10, color=colors[cls], label=f'Class {int(cls)}')
        else:
            ax.scatter(tree.data[:, 0], tree.data[:, 1], 
                       s=10, color='black', label='Data Points')

    @staticmethod
    def _plot_tree_structure(node, ax, level=0, max_levels=10):
        """
        Recursively plot the tree structure with color-coded circles
        Directly adapted from your original _plot_tree method
        """
        if node is None:
            return

        cmap = cm.get_cmap('tab10', max_levels)

        if node.radius is not None and node.center is not None:
            color = cmap(level % max_levels)
            circle = Circle(node.center, node.radius, 
                            color=color, fill=False, 
                            linestyle='-', linewidth=1)
            ax.add_patch(circle)

        if node.left is not None:
            TreePlotter._plot_tree_structure(node.left, ax, level + 1, max_levels)
        if node.right is not None:
            TreePlotter._plot_tree_structure(node.right, ax, level + 1, max_levels)

    @staticmethod
    def _plot_knn_points(ax, knn_queried_points):
        """Plot k-nearest neighbor points"""
        knn_queried_points = np.array(knn_queried_points)
        ax.scatter(knn_queried_points[:, 0], knn_queried_points[:, 1], 
                   s=30, color='red', label='KNN Queried Points')

    @staticmethod
    def _plot_range_query(ax, query_point, range_queried_points, radius):
        """Plot range query results"""
        circle = Circle(query_point, radius, 
                        color='black', fill=False, 
                        linestyle='-', linewidth=2)
        ax.add_patch(circle)

        if not range_queried_points:
            print("No elements found in the range query.")
        else:
            range_queried_points = np.array(range_queried_points)
            ax.scatter(range_queried_points[:, 0], range_queried_points[:, 1], 
                       s=30, color='Orange', label='Range Queried Points')

    @staticmethod
    def _plot_query_point(ax, query_point):
        """Plot the query point"""
        ax.scatter(query_point[0], query_point[1], 
                   s=50, color='purple', label='Query Point')