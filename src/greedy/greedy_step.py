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






            


