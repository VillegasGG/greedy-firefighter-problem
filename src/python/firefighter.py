"""
Firefighter class:
    - A firefighter has position and speed
    - A firefighter can move to a position
    - A firefighter can protect a node
"""
import random
import numpy as np


class Firefighter:
    def __init__(self, tree, speed=1):
        self.speed = speed
        self.position = None
        self.tree = tree

    def move_to_node(self, new_position):
        self.position = new_position

    def add_random_initial_firefighter_position(self):
        '''
        Add a random firefighter position in tridimensional space with scale 1.
        '''
        random_point = (
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

        self.position = random_point