import random
import numpy as np

class Firefighter:
    def __init__(self, tree, speed=10):
        self.speed = speed
        self.position = None
        self.tree = tree
        self.__remaining_time__ = None

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

    def get_distance_to_node(self, node):
        position_node = self.tree.nodes_positions[node]
        return np.linalg.norm(position_node - self.position)    
    
    def init_remaining_time(self):
        self.__remaining_time__ = 1

    def update_remaining_time(self):
        self.__remaining_time__ -= 1
    
    def get_remaining_time(self):
        return self.__remaining_time__