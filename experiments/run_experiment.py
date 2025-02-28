import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from visualizer import TreeVisualizer
from greedy.simulation import Simulation
from config_tree import my_tree, root

visualizer = TreeVisualizer(my_tree)

def vizualize_state(simulation, step):
    burning_nodes = simulation.state.burning_nodes
    burned_nodes = simulation.state.burned_nodes
    protected_nodes = simulation.state.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, simulation.firefighter.position)
   
def execute_experiment():
    step = -1
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    simulation = Simulation(my_tree)
    
    while not simulation.is_completely_burned():
        step += 1
        if step>0: print(f"{'#' * 50}\nWHEN STATE {step-1}:")
        simulation.execute_step()
        vizualize_state(simulation, step)
        
    print('#' * 50)

    visualizer.plot_3d_final_state(simulation.state.burning_nodes, simulation.state.burned_nodes, simulation.state.protected_nodes, simulation.firefighter.position)
    print('-' * 50 + f"\nDaño: {len(simulation.state.burned_nodes) + len(simulation.state.burning_nodes)}\n" + '-' * 50)

def main():
    start_time = time.perf_counter()
    execute_experiment()
    end_time = time.perf_counter()
    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
