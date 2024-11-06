import time
import numpy as np
from tree_utils import Tree
from src.python.visualizer import TreeVisualizer
from src.python.fire_simulation import FirePropagation

start_time = time.perf_counter()

# Crear un árbol de ejemplo
nodes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
edges = [(0, 1), (0, 2), (0, 3), (0, 4), 
         (1, 5), (1, 6), 
         (2, 8), (2, 9),
         (3, 11),
         (4, 15), (4, 16), (4, 17), (4, 18),
         (6, 7),
         (9, 10),
         (11, 12),
         (12, 13),
         (13, 14),
         (15, 19),
         (16, 20),
         (18,21)  ]  # Conexiones entre nodos

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
    [-4, 0, 0],    # Nodo 14
    [0, 2, 9],   # Nodo 15
    [-2, 4, 9],   # Nodo 16
    [2, 4, 9],  # Nodo 17
    [0, 6, 9],   # Nodo 18
    [0, 2, 6],    # Nodo 19
    [-2, 4, 6],   # Nodo 20
    [0, 6, 6]    # Nodo 21
]

# Crear una instancia de Tree
my_tree = Tree(nodes, edges, nodes_positions)

visualizer = TreeVisualizer(my_tree)
visualizer.plot_3d_tree(my_tree, "images/initial_tree")
visualizer.plot_2d_tree_with_root(my_tree, 0)

fire = FirePropagation(my_tree)
fire.start_fire(0)
burning_nodes, burned_nodes = fire.display_state()
step = 0
visualizer.plot_fire_state(burning_nodes, burned_nodes, step)

while (not fire.is_completely_burned()):
    step += 1
    fire.propagate()
    burning_nodes, burned_nodes = fire.display_state()
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step)

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Tiempo de ejecución total: {execution_time:.4f} segundos")