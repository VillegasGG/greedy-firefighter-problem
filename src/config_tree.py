import numpy as np
from src.tree_utils import Tree

nodes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
edges = [(0, 1), (0, 2), (0, 3), (0, 4), 
         (1, 5), (1, 6), 
         (2, 8), (2, 9),
         (3, 11),
         (6, 7),
         (9, 10),
         (11, 12),
         (12, 13),
         (13, 14)  ]  # Conexiones entre nodos

# Definir posiciones específicas para los nodos
nodes_positions = [
    [0, 0, 15],   # Nodo 0
    [0, -4, 12],   # Nodo 1
    [4, 0, 12],  # Nodo 2
    [-4, 0, 12],   # Nodo 3
    [0, 4, 12],    # Nodo 4
    [0, -6, 9],   # Nodo 5
    [0, -2, 9],   # Nodo 6
    [0, -2, 6],  # Nodo 7
    [6, 0, 9],   # Nodo 8
    [2, 0, 9],    # Nodo 9
    [2, 0, 6],   # Nodo 10
    [-4, 0, 9],   # Nodo 11
    [-4, 0, 6],  # Nodo 12
    [-4, 0, 3],   # Nodo 13
    [-4, 0, 0]    # Nodo 14
]

my_tree = Tree(nodes, edges, nodes_positions)
root = 0