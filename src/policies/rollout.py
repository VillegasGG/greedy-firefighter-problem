from greedyff.greedy_sim import GreedyStep
from greedyff.get_candidates_utils import get_candidates
from greedyff.greedy_sim import GreedySim
from visualizer import TreeVisualizer
from helpers import vizualize_state

import copy

class Rollout:
    def __init__(self, tree):
        self.original_tree = tree

    def calcule_best_time(self, candidates, min_burned_nodes):
        """
        Calculate the best candidate by time to reach the node.
        """
        best_candidate = None
        min_time = float('inf')

        for candidate in candidates:
            if candidate[1] == min_burned_nodes:
                if candidate[0][1] < min_time:
                    min_time = candidate[0][1]
                    best_candidate = candidate[0][0]

        return best_candidate, min_time

    def get_node_to_protect(self, candidates, env, step):
        # Initialize min burned nodes to a infinity value
        min_burned_nodes = float('inf')
        best_candidate = None
        num_final_candidates = 0
        candidate_burned = []
        protecting_node = env.firefighter.protecting_node

        if protecting_node:
            print(f"Firefighter is already protecting node {protecting_node}")
        else:
            print("Firefighter is not protecting any node")

        if(not candidates):
            print('No candidates to protect')
            return None, None
        
        for candidate in candidates:
            # Create a copy of the environment to simulate the action
            print(f"Creating a copy of the environment for candidate {candidate[0]} with time {candidate[1]}")
            env_copy = copy.deepcopy(env)
            node = candidate[0]
            node_time = candidate[1]
            ff_speed = env.firefighter.speed
            output_dir_name = f"output/rollout/step_{step}_node_{node}_time_{node_time}"

            greedy_sim = GreedySim(env=env_copy, ff_speed=ff_speed, output_dir=output_dir_name)
            print(f"Simulating action for node {node} with time {node_time}")
            # Simulate the action of protecting the node
            greedy_sim.run()
            print(len(greedy_sim.state.burned_nodes), "burned nodes after simulation")
        
        return


    def select_action(self, env, step):
        """
        Selects the best action for the firefighter using a rollout policy.
        """
        greedy = GreedyStep(self.original_tree)
        
        # Get the candidates for the firefighter action
        candidates = get_candidates(env.tree, env.state, env.firefighter)

        node_to_protect, node_time = self.get_node_to_protect(candidates, env, step)
        print(f'Node to protect: {node_to_protect} | Time to reach: {node_time}')

        if node_to_protect is not None:
            node_pos = env.tree.nodes_positions[node_to_protect]
            if(env.firefighter.get_remaining_time() >= node_time):
                env.state.protected_nodes.add(node_to_protect)
                env.firefighter.move_to_node(node_pos, node_time)
                env.firefighter.protecting_node = None
            else:
                env.firefighter.move_fraction(node_pos)
                env.firefighter.protecting_node = node_to_protect
                    
            env.firefighter.print_info()
            return True

        else:
            print('No node to protect')
            return False