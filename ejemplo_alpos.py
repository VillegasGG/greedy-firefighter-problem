import time
from src.python.visualizer import TreeVisualizer
from src.python.fire_simulation import FirePropagation
from tree_generator import generate_random_tree, add_random_firefighter_position

start_time = time.perf_counter()

n_nodes = 22
my_tree, edges, nodes_positions = generate_random_tree(n_nodes, 5, 'min')
add_random_firefighter_position(my_tree)
add_random_firefighter_position(my_tree)
add_random_firefighter_position(my_tree)

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