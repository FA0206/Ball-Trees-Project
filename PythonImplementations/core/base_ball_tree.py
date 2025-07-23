from abc import ABC, abstractmethod
import numpy as np
import heapq

class BaseBallTree(ABC):
    # Note: data isn't directly passed to the constructor, but is passed to the fit method
    def __init__(self, leaf_size=10, has_classification=False):
        self.leaf_size = leaf_size
        self.has_classification = has_classification
        self.volume = 0
        self.node_count = 0
        self.root = None
        self.data = None  # This will store the original dataset

    @abstractmethod
    def fit(self, X, y=None):
        """Abstract method to be implemented by specific construction methods."""
        pass

    def knn_query(self, query_point, k=1):
        """
        Query the Ball* Tree to find the k-nearest neighbors of a given query point.
        Uses a priority queue to keep track of the k-nearest neighbors found so far.
        Performs backtracking to explore other subtrees if there's a chance of finding closer neighbors.
        """
        # Priority queue to store the k-nearest neighbors (using max-heap to track the furthest neighbor in the list)
        # Set the knn_heap with one element with infinite distance
        knn_heap = [(-float('inf'), None)]
        stats = {'points_being_searched': 0, 'points_being_skipped': 0} 
        
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
                    stats['points_being_searched'] += len(node.data)
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
                    stats['points_being_skipped'] += len(node.data)
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
                stats['points_being_skipped'] += len(node.data)

        # Start the search from the root node
        print("Starting the KNN query...")
        search_node(self.root)
        print("KNN query completed.")

        # Return sorted list of nearest neighbors by distance
        return knn_heap, stats['points_being_searched'], stats['points_being_skipped']

    def range_query(self, query_point, range):
        points_in_range = []
        stats = {'points_being_searched': 0, 'points_being_skipped': 0} 

        def search_node(node):
            if node is None:
                return
            distance_to_center = np.linalg.norm(query_point - node.center)

            if distance_to_center - node.radius > range:
                stats['points_being_skipped'] += len(node.data)
                if node.left is None and node.right is None:
                    print("Skipping the leaf of size ", len(node.data))
                else:
                    print("Skipping the node of size ", len(node.data))
                return

            if node.left is None and node.right is None:
                stats['points_being_searched'] += len(node.data)
                for point in node.data:
                    if not self.has_classification:
                        dist = np.linalg.norm(query_point - point)
                    else:
                        dist = np.linalg.norm(query_point - point[:-1])

                    if dist <= range:
                        points_in_range.append(point)
                return

            if np.linalg.norm(query_point - node.left.center) <= np.linalg.norm(query_point - node.right.center):
                search_node(node.left)
                search_node(node.right)
            else:
                search_node(node.right)
                search_node(node.left)

        print("Starting the range query...")
        search_node(self.root)
        print("Range query completed.")

        return points_in_range, stats['points_being_searched'], stats['points_being_skipped']

    # Helper function to calculate tree depth metrics
    def calculate_tree_depth(tree):
        depths = []

        def traverse(node, depth):
            if node.left is None and node.right is None:
                depths.append(depth)
            else:
                traverse(node.left, depth + 1)
                traverse(node.right, depth + 1)

        traverse(tree.root, 1)
        return np.mean(depths), max(depths)