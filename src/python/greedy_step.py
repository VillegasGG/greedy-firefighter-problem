class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def dfs(self, node, visited): #Cambiar a iterativo (bfs)
        neighbors = self.tree.get_neighbors(node)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                self.dfs(neighbor, visited)


    def get_node_to_protect(self, b_nodes, candidates):
        """
        Selecciona el nodo a proteger basado en el subarbol más grande
        """
        
        # Candidates depths dictionary
        candidates_depths = {}
        len_b_nodes = len(b_nodes)

        for candidate in candidates:
            visited = set(b_nodes)
            visited.add(candidate)
            self.dfs(candidate, visited)
            depth = len(visited) - len_b_nodes
            candidates_depths[candidate] = depth
            print('Candidate: ' + str(int(candidate)) + ' Depth: ' + str(depth) + ' nodes')

        if not candidates_depths:
            print('No candidates')
            return None
        
        max_depth = max(candidates_depths.values())
        node_to_protect =  [node for node, depth in candidates_depths.items() if depth == max_depth][0]
        print('Node protected: ' + str(int(node_to_protect)) + ' Safe: ' + str(max_depth) + ' nodes')

        return node_to_protect


            


