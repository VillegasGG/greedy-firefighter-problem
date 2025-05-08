from policies.greedy_step import GreedyStep
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
            env_copy = copy.deepcopy(env)
            node = candidate[0]
            node_time = candidate[1]

            visualizer = TreeVisualizer(env_copy.tree)

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
            file_route = "images/rollout/"
            file_name = f"step_{step}_candidate_{int(candidate[0])}"
            # vizualize_state(visualizer, env_copy, file_name, file_route)
            visualizer.plot_3d_final_state(env_copy.state.burning_nodes, env_copy.state.burned_nodes, env_copy.state.protected_nodes, env_copy.firefighter.position, file_route, file_name)

            # Save the number of burned nodes in the copied environment
            num_burned_nodes = len(env_copy.state.burned_nodes)
            num_burning_nodes = len(env_copy.state.burning_nodes)
            total_burning_nodes = num_burned_nodes + num_burning_nodes

            candidate_burned.append((candidate, total_burning_nodes))

            print(f"Candidate {candidate} results: {total_burning_nodes} burned nodes")


            # Check if the number of burned nodes is less than the current minimum
            if total_burning_nodes < min_burned_nodes:
                min_burned_nodes = total_burning_nodes
                best_candidate = candidate

        # If there are multiple candidates with the same number of burned nodes, select the one with the minimum time to reach
        for candidate in candidate_burned:
            if candidate[1] == min_burned_nodes:
                num_final_candidates += 1
                
        if(env.firefighter.protecting_node and env.firefighter.protecting_node != best_candidate[0]):
            print(f"Firefighter is already protecting node {env.firefighter.protecting_node}")
            return env.firefighter.protecting_node, env.firefighter.get_distance_to_node(env.firefighter.protecting_node)

        if num_final_candidates == 1:
            print(f"Best candidate: {best_candidate} with {min_burned_nodes} burned nodes")
            return best_candidate[0], best_candidate[1]
        else:
            # If there are multiple candidates with the same number of burned nodes, return the minimum time to reach
            print("Multiple candidates with the same number of burned nodes")
            best = self.calcule_best_time(candidate_burned, min_burned_nodes)
            print(f"Best candidate by time: {best}")
            return best[0], best[1]

    def select_action(self, env, step):
        """
        Selects the best action for the firefighter using a rollout policy.
        """
        greedy = GreedyStep(self.original_tree)
        
        # Get the candidates for the firefighter action
        candidates = greedy.get_candidates(env)

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