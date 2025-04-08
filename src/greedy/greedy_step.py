from collections import deque

class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def get_candidate_subtree(self, node): 
        queue = []
        visited = set()
        visited.add(node)
        queue.append(node)

        while queue:
            s = queue.pop(0)
            neighbors = self.tree.get_neighbors(s)
            for neighbor in neighbors:
                if neighbor not in visited:
                    if neighbor not in self.burned_nodes:
                        queue.append(neighbor)
                        visited.add(neighbor)
            
        return visited

    def get_node_to_protect(self, candidates, firefighter):
        """
        Selecciona el nodo a proteger basado en el subarbol más grande
        """

        candidates_depths = {}
        candidates_time = {}

        for candidate in candidates:
            subtree = self.get_candidate_subtree(candidate[0])
            depth = len(subtree)
            candidates_depths[candidate[0]] = depth
            candidates_time[candidate[0]] = candidate[1]

        if not candidates_depths:
            print('No candidates')
            return None, None
        
        max_depth = max(candidates_depths.values())
        
        node_to_protect =  [node for node, depth in candidates_depths.items() if depth == max_depth][0]
        print('Node protected: ' + str(int(node_to_protect)) + ' Safe: ' + str(max_depth) + ' nodes')

        if(firefighter.protecting_node):
            if(firefighter.protecting_node != node_to_protect):
                if candidates_depths[firefighter.protecting_node] < candidates_depths[node_to_protect]:
                    print('!'*50)
                    print(f'FF is moving to node {node_to_protect} but better option is {firefighter.protecting_node}')
                    print(candidates_depths)
                    print(f'Actual protecting node: {firefighter.protecting_node} has {candidates_depths[firefighter.protecting_node]} nodes')
                    print(f'New protecting node: {node_to_protect} has {candidates_depths[node_to_protect]} nodes')
                    print(f'Actual protecting node time: {candidates_time[firefighter.protecting_node]}')
                    print(f'New protecting node time: {candidates_time[node_to_protect]}')
                    print('!'*50)
            return firefighter.protecting_node, candidates_time[firefighter.protecting_node]

        return node_to_protect, candidates_time[node_to_protect]
        
    # Function to know in how many steps the fire will reach each node
    def steps_to_reach_all(self):
        
        layer = {}
        visited = set()
        
        # BFS to get the layers of the tree
        queue = deque()
        
        for node in self.burned_nodes:
            queue.append(node)
            visited.add(node)
            layer[int(node)] = 0

        while queue:
            s = queue.popleft()
            neighbors = self.tree.get_neighbors(s)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    layer[int(neighbor)] = layer[s] + 1

        return layer
    
    def get_final_candidates(self, candidates, fire_time, time_ff_reach, env):

        final_candidates = set()

        # Filter candidates that can be reached before the fire
        for candidate in candidates:
            time_ff_reach_candidate = time_ff_reach[candidate]
            time_to_burn_candidate = fire_time[candidate]
            remaining_time = env.firefighter.get_remaining_time()
            if time_ff_reach_candidate > time_to_burn_candidate:
                continue
            elif remaining_time < 1:
                next_step_burn = time_to_burn_candidate - 1
                next_step_ff = time_ff_reach_candidate - remaining_time
                if next_step_ff < next_step_burn:
                    final_candidates.add((candidate, time_ff_reach[candidate]))
                else:
                    # print(f'IMPORTANT!!  -- Node: {candidate} | Time to reach: {time_ff_reach[candidate]} | Time to burn: {fire_time[candidate]} but remaining time is {remaining_time}')
                    continue
            else:
                if time_ff_reach[candidate] < time_to_burn_candidate:
                    final_candidates.add((candidate, time_ff_reach[candidate]))

        return final_candidates
    
    def is_protected_by_ancestor(self, node, env):
        path = env.tree.get_path_to_root(node)
        for ancestor in path:
            if ancestor in env.state.protected_nodes:
                return True
        return False

    def get_not_protected_nodes(self, env):
        candidates = set()

        unnafected_nodes = set(env.tree.nodes) - env.state.burned_nodes - env.state.protected_nodes - env.state.burning_nodes

        for element in unnafected_nodes:
            is_protected = self.is_protected_by_ancestor(element, env)
            if not is_protected:
                candidates.add(element)

        return candidates

    def get_candidates(self, env):

        first_candidates = self.get_not_protected_nodes(env)

        ff_distances = env.firefighter.get_distances_to_nodes(first_candidates)
        fire_time = self.steps_to_reach_all()

        time_ff_reach = {} # Time taken to reach each candidate
        for candidate in first_candidates:
            time_ff_reach[candidate] = ff_distances[candidate] / env.firefighter.speed
      
        # self.show_candidates("Candidates after first filter (After protected by ancestor):", first_candidates, fire_time, time_ff_reach)

        final_candidates = self.get_final_candidates(first_candidates, fire_time, time_ff_reach, env)
        
        # self.show_candidates_tuple("Final candidates:", final_candidates, fire_time)

        return final_candidates

    def select_node_to_protect_and_move(self, env):
        """
        - Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande (aunque este mas lejos)
        - Se mueve el bombero al nodo seleccionado
        """
        burned_and_burning_nodes = env.state.burned_nodes.union(env.state.burning_nodes)
        self.burned_nodes = burned_and_burning_nodes
        candidates = self.get_candidates(env)
        node_to_protect, node_time = self.get_node_to_protect(candidates, env.firefighter)
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






            


