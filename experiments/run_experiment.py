import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


from greedy.simulation import Simulation
from config_tree import my_tree, root

def main():
    simulation = Simulation(my_tree)
    my_tree.save_positions_to_json("data/positions.json")
    my_tree.save_edges_to_json("data/edges.json")
    simulation.run_simulation(graph=True)
 
if __name__ == "__main__":
    main()


# Checar como paralelizar rollout con cuda o hilos