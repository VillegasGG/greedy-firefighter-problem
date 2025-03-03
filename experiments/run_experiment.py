import sys
import os
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from visualizer import TreeVisualizer
from greedy.simulation import Simulation
from config_tree import my_tree, root
from helpers import save_results

visualizer = TreeVisualizer(my_tree)

def run_fire_simulation(simulation):
    step = 0
    burning_nodes = simulation.state.burning_nodes
    burned_nodes = simulation.state.burned_nodes
    protected_nodes = simulation.state.protected_nodes
    while not simulation.is_completely_burned(burning_nodes, burned_nodes, protected_nodes):
        step += 1
        simulation.greedy_step()
        simulation.propagate()
        print(f"Paso {step}")
        burning_nodes = simulation.state.burning_nodes
        burned_nodes = simulation.state.burned_nodes
        protected_nodes = simulation.state.protected_nodes

        visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, simulation.firefighter.position)

    save_results(burned_nodes, burning_nodes, protected_nodes, "results.json")
    visualizer.plot_3d_final_state(burning_nodes, burned_nodes, protected_nodes, simulation.firefighter.position)
    print('-' * 50 + f"\nDaño: {len(burned_nodes) + len(burning_nodes)}\n" + '-' * 50)

def simulate_fire(tree):
    simulation = Simulation(tree)
    simulation.start_fire(root)
    burned_nodes = simulation.state.burned_nodes
    burning_nodes = simulation.state.burning_nodes
    protected_nodes = simulation.state.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, 0, protected_nodes, simulation.firefighter.position)
    run_fire_simulation(simulation)

def execute_experiment():
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    visualizer.plot_2d_tree_with_root(my_tree, root)
    my_tree.save_positions_to_json("positions.txt")
    my_tree.save_edges_to_json("edges.txt")
    print("Root:", root)
    simulate_fire(my_tree)
   
def main():
    start_time = time.perf_counter()
    execute_experiment()
    end_time = time.perf_counter()
    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
