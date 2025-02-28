import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from visualizer import TreeVisualizer
from greedy.fire_simulation import FirePropagation
from config_tree import my_tree, root

def run_fire_simulation(fire, visualizer):
    step = 0
    burning_nodes = fire.state.burning_nodes
    burned_nodes = fire.state.burned_nodes
    protected_nodes = fire.state.protected_nodes
    while not fire.is_completely_burned(burning_nodes, burned_nodes, protected_nodes):
        step += 1
        fire.select_node_to_protect()
        fire.propagate()
        print(f"Paso {step}")
        burning_nodes = fire.state.burning_nodes
        burned_nodes = fire.state.burned_nodes
        protected_nodes = fire.state.protected_nodes
        visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, fire.firefighter.position)

    visualizer.plot_3d_final_state(burning_nodes, burned_nodes, protected_nodes, fire.firefighter.position)
    print('-' * 50 + f"\nDaño: {len(burned_nodes) + len(burning_nodes)}\n" + '-' * 50)

def simulate_fire(tree, visualizer, root):
    simulation = FirePropagation(tree)
    simulation.start_fire(root)
    burned_nodes = simulation.state.burned_nodes
    burning_nodes = simulation.state.burning_nodes
    protected_nodes = simulation.state.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, 0, protected_nodes, simulation.firefighter.position)
    run_fire_simulation(simulation, visualizer)

def execute_experiment():
    visualizer = TreeVisualizer(my_tree)
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    visualizer.plot_2d_tree_with_root(my_tree, root)
    print("Root:", root)
    simulate_fire(my_tree, visualizer, root)
    

def main():
    start_time = time.perf_counter()
    execute_experiment()
    end_time = time.perf_counter()
    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
