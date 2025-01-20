class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def dfs(self, node, visited):
        neighbors = self.tree.get_neighbors(node)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                print(f"Agregando {neighbor} a visited")
                self.dfs(neighbor, visited)


    def get_node_to_protect(self, b_nodes, candidates):
        """
        Selecciona el nodo a proteger basado en el subarbol más grande
        """
        for candidate in candidates:
            print(f"Candidate: {candidate}")
            visited = set(b_nodes)
            visited.add(candidate)
            self.dfs(candidate, visited)


            


