from tree_generator import generate_random_tree, add_random_firefighter_position
import numpy as np

n_nodes = 22
my_tree, edges, nodes_positions = generate_random_tree(n_nodes, 5, 'min')
