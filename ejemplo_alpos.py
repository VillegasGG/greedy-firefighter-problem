import time
import numpy as np
from src.python.tree_utils import Tree
from src.python.visualizer import TreeVisualizer
from src.python.fire_simulation import FirePropagation
from tree_generator import generate_prufer_sequence, calculate_degrees, construct_edges, generate_positions

start_time = time.perf_counter()

n_nodes = 22
prufer_sequence = generate_prufer_sequence(n_nodes)
degrees = calculate_degrees(prufer_sequence, n_nodes)
edges = construct_edges(prufer_sequence, degrees)
nodes_positions = generate_positions(n_nodes, edges)
my_tree = Tree(np.arange(n_nodes), edges, nodes_positions)

visualizer = TreeVisualizer(my_tree)
visualizer.plot_3d_tree(my_tree, "images/initial_tree")
visualizer.plot_2d_tree_with_root(my_tree, 0)

# Simulación de propagación de fuego
fire = FirePropagation(my_tree)
fire.start_fire(0)
burning_nodes, burned_nodes = fire.display_state()
step = 0
visualizer.plot_fire_state(burning_nodes, burned_nodes, step)

while not fire.is_completely_burned():
    step += 1
    fire.propagate()
    burning_nodes, burned_nodes = fire.display_state()
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step)

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Tiempo de ejecución total: {execution_time:.4f} segundos")