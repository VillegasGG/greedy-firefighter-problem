import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from visualizer import TreeVisualizer
from greedy.simulation import Simulation
from config_tree import my_tree, root
   
def execute_experiment():
    visualizer = TreeVisualizer(my_tree)
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    simulation = Simulation(my_tree)
    simulation.start_fire(root)
    burned_nodes = simulation.state.burned_nodes
    burning_nodes = simulation.state.burning_nodes
    protected_nodes = simulation.state.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, 0, protected_nodes, simulation.firefighter.position)
    
    step = 0

    while not simulation.is_completely_burned(burning_nodes, burned_nodes, protected_nodes):
        step += 1
        simulation.select_node_to_protect()
        simulation.propagate()
        print(f"Paso {step}")
        burning_nodes = simulation.state.burning_nodes
        burned_nodes = simulation.state.burned_nodes
        protected_nodes = simulation.state.protected_nodes
        visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, simulation.firefighter.position)

    visualizer.plot_3d_final_state(burning_nodes, burned_nodes, protected_nodes, simulation.firefighter.position)
    print('-' * 50 + f"\nDaño: {len(burned_nodes) + len(burning_nodes)}\n" + '-' * 50)

def main():
    start_time = time.perf_counter()
    execute_experiment()
    end_time = time.perf_counter()
    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
