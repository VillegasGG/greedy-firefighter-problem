import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from visualizer import TreeVisualizer
from greedy.simulationRO import SimulationRO
from config_tree import my_tree, root
from helpers import save_results

visualizer = TreeVisualizer(my_tree)

def vizualize_state(simulation, step):
    burning_nodes = simulation.state.burning_nodes
    burned_nodes = simulation.state.burned_nodes
    protected_nodes = simulation.state.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, simulation.firefighter.position)
   
def execute_experiment():
    step = -1
    simulation = SimulationRO(my_tree)

    start_time = time.perf_counter()
    
    while not simulation.is_completely_burned():
        step += 1
        if step>0: print(f"{'#' * 50}\nWHEN STATE {step-1}:")
        simulation.execute_step()
        vizualize_state(simulation, step)
    
    end_time = time.perf_counter()
        
    print('#' * 50)

    visualizer.plot_3d_final_state(simulation.state.burning_nodes, simulation.state.burned_nodes, simulation.state.protected_nodes, simulation.firefighter.position)
    save_results(simulation.state.burned_nodes, simulation.state.burning_nodes, simulation.state.protected_nodes, "result.json")
    
    print('-' * 50 + f"\nDaño: {len(simulation.state.burned_nodes) + len(simulation.state.burning_nodes)}\n" + '-' * 50)

    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

def main():
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    my_tree.save_positions_to_json("data/positions.json")
    my_tree.save_edges_to_json("data/edges.json")

    execute_experiment()
 


if __name__ == "__main__":
    main()


# Checar como paralelizar rollout con cuda o hilos