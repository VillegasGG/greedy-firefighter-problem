from collections import deque

class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def bfs(self, node): 
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
            
        print('Visited: ' + str(len(visited)) + ' nodes')
        print('Visited: ' + str(visited))
        return visited

    def get_node_to_protect(self, b_nodes, candidates):
        """
        Selecciona el nodo a proteger basado en el subarbol más grande
        """
        
        # Candidates depths dictionary
        candidates_depths = {}

        for candidate in candidates:
            visited = self.bfs(candidate)
            depth = len(visited)
            candidates_depths[candidate] = depth
            print('Candidate: ' + str(int(candidate)) + ' Depth: ' + str(depth) + ' nodes')

        if not candidates_depths:
            print('No candidates')
            return None
        
        max_depth = max(candidates_depths.values())
        node_to_protect =  [node for node, depth in candidates_depths.items() if depth == max_depth][0]
        print('Node protected: ' + str(int(node_to_protect)) + ' Safe: ' + str(max_depth) + ' nodes')

        return node_to_protect
    
    
    # Function to know in how many steps the fire will reach each node
    def steps_to_reach_all(self):
        
        # obtain layers of the tree before the fire with bfs
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






            


