import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from simulation import Simulation
from config_tree import my_tree
from policies.rollout import Rollout

def main():
    rollout_simulation = Simulation(Rollout(my_tree), my_tree)
    my_tree.save_positions_to_json("data/positions.json")
    my_tree.save_edges_to_json("data/edges.json")
    rollout_simulation.run_simulation(True)
 
if __name__ == "__main__":
    main()


# Checar como paralelizar rollout con cuda o hilos