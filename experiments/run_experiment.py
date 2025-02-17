import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from python.visualizer import TreeVisualizer
from python.fire_simulation import FirePropagation
from config_tree2 import my_tree, root

def run_fire_simulation(fire, visualizer):
    step = 0
    while not fire.is_completely_burned(*fire.display_state(), fire.protected_nodes):
        step += 1
        fire.greedy_step()
        fire.propagate()
        print(f"Paso {step}")
        visualizer.plot_fire_state(*fire.display_state(), step, fire.protected_nodes, fire.firefighter.actual_position)

    visualizer.plot_3d_final_state(*fire.display_state(), fire.protected_nodes, fire.firefighter.actual_position)
    print('-' * 50)
    print(f"Daño: {len(fire.burned_nodes) + len(fire.burning_nodes)}")
    print('-' * 50)

def simulate_fire(tree, visualizer, root):
    fire = FirePropagation(tree)
    fire.start_fire(root)
    visualizer.plot_fire_state(*fire.display_state(), 0, fire.protected_nodes, fire.firefighter.actual_position)

    run_fire_simulation(fire, visualizer)

def execute_experiment():
    visualizer = TreeVisualizer(my_tree)
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    visualizer.plot_2d_tree_with_root(my_tree, 0)
    simulate_fire(my_tree, visualizer, root)

def main():
    start_time = time.perf_counter()
    execute_experiment()
    end_time = time.perf_counter()
    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
