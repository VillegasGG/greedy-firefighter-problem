import os
import sys
from policies.greedy_step import GreedyStep
import copy

class Rollout:
    def __init__(self, tree):
        self.original_tree = tree

    def select_action(self, env):
        """
        Selects the best action for the firefighter using a rollout policy.
        """
        greedy = GreedyStep(self.original_tree)
        
        # Get the candidates for the firefighter action
        candidates = greedy.get_candidates(env)
        
        for candidate in candidates:
            # Create a copy of the environment to simulate the action
            print(f"Simulating action for candidate: {candidate}")
            env_copy = copy.deepcopy(env)

            node = candidate[0]
            node_time = candidate[1]
            node_position = env_copy.tree.nodes_positions[node]
          
            if(env_copy.firefighter.get_remaining_time() >= node_time):
                env_copy.state.protected_nodes.add(node)
                env_copy.firefighter.move_to_node(node_position, node_time)
                env_copy.firefighter.protecting_node = None
            else:
                env_copy.firefighter.move_fraction(node_position)
                env_copy.firefighter.protecting_node = node
                
            env_copy.firefighter.print_info()

        return False