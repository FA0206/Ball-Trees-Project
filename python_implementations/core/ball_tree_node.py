import numpy as np
from math import *

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