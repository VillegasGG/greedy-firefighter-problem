from policies.greedy_step import GreedyStep
from helpers import vizualize_state

import copy

class Rollout:
    def __init__(self, tree):
        self.original_tree = tree

    def get_node_to_protect(self, candidates, env):
        # Initialize min burned nodes to a infinity value
        min_burned_nodes = float('inf')
        best_candidate = None

        if(not candidates):
            print('No candidates to protect')
            return None, None
        
        for candidate in candidates:
            # Create a copy of the environment to simulate the action
            # print(f"Simulating action for candidate: {candidate}")
            env_copy = copy.deepcopy(env)
            node = candidate[0]
            node_time = candidate[1]

            while(env_copy.firefighter.get_remaining_time() > 0 and node_time!= 0):
                node_time = env_copy.firefighter.get_distance_to_node(node)
                node_position = env_copy.tree.nodes_positions[node]

                # print(f"Firefighter position: {env_copy.firefighter.position} | Node position: {node_position} | Time to reach: {node_time}")
                # print(f"Firefighter remaining time: {env_copy.firefighter.get_remaining_time()}")

                if(env_copy.firefighter.get_remaining_time() >= node_time):
                    env_copy.state.protected_nodes.add(node)
                    env_copy.firefighter.move_to_node(node_position, node_time)
                    env_copy.firefighter.protecting_node = None
                else:
                    env_copy.firefighter.move_fraction(node_position)
                    env_copy.firefighter.protecting_node = node
                    
            # Propagate the fire in the copied environment 
            env_copy.propagate()

            # Save the number of burned nodes in the copied environment
            num_burned_nodes = len(env_copy.state.burned_nodes)
            num_burning_nodes = len(env_copy.state.burning_nodes)
            total_burning_nodes = num_burned_nodes + num_burning_nodes

            print(f"Candidate {candidate} results: {total_burning_nodes} burned nodes")

            # Check if the number of burned nodes is less than the current minimum
            if total_burning_nodes < min_burned_nodes:
                min_burned_nodes = total_burning_nodes
                best_candidate = candidate

        print(f"Best candidate: {best_candidate} with {min_burned_nodes} burned nodes")

        if(env.firefighter.protecting_node):
            print(f"Firefighter is already protecting node {env.firefighter.protecting_node}")
            return env.firefighter.protecting_node, env.firefighter.get_distance_to_node(env.firefighter.protecting_node)

        return best_candidate[0], best_candidate[1]

    def select_action(self, env):
        """
        Selects the best action for the firefighter using a rollout policy.
        """
        greedy = GreedyStep(self.original_tree)
        
        # Get the candidates for the firefighter action
        candidates = greedy.get_candidates(env)

        node_to_protect, node_time = self.get_node_to_protect(candidates, env)
        print(f'Node to protect: {node_to_protect} | Time to reach: {node_time}')

        if node_to_protect:
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