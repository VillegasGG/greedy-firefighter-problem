import time
import numpy as np
from src.python.tree_utils import Tree
from src.python.visualizer import TreeVisualizer
from src.python.fire_simulation import FirePropagation

start_time = time.perf_counter()

def run_fire_simulation(fire, visualizer):
    step = 0
    burning_nodes, burned_nodes = fire.display_state()
    protected_nodes = fire.protected_nodes
    while not fire.is_completely_burned(burning_nodes, burned_nodes, protected_nodes):
        step += 1
        fire.greedy_step()
        fire.propagate()
        print(f"Paso {step}")
        burning_nodes, burned_nodes = fire.display_state()
        protected_nodes = fire.protected_nodes
        visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes)

def simulate_fire(my_tree, visualizer):
    fire = FirePropagation(my_tree)
    fire.start_fire(0)
    visualizer.plot_3d_tree(my_tree, "images/initial_fire")
    step = 0
    burning_nodes, burned_nodes = fire.display_state()
    protected_nodes = fire.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step, None)

    run_fire_simulation(fire, visualizer)

    visualizer.plot_3d_final_state(burning_nodes, burned_nodes, protected_nodes)

# Crear un árbol de ejemplo
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

# Crear una instancia de Tree
my_tree = Tree(nodes, edges, nodes_positions)

visualizer = TreeVisualizer(my_tree)
visualizer.plot_3d_tree(my_tree, "images/initial_tree")
visualizer.plot_2d_tree_with_root(my_tree, 0)

simulate_fire(my_tree, visualizer)

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Tiempo de ejecución total: {execution_time:.4f} segundos")