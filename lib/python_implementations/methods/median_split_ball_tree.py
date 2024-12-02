from core.base_ball_tree import BaseBallTree
from core.ball_tree_node import BallTreeNode

import numpy as np

class MedianSplitBallTree(BaseBallTree):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fit(self, X, y=None):
        # Median split-specific tree construction logic
        self.data = X if y is None else np.column_stack((X, y))

        root_node = self._construct_median_node(X, y)
        self.root = root_node
        return self

    def _construct_median_node(self, data, labels=None):
        # Recursive median split node construction
        # Implement your median split logic here
        pass