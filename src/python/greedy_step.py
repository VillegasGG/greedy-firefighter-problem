class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def get_node_to_protect(self, burning_nodes, candidates):
        """
        Selecciona el nodo a proteger basado en el subarbol más grande
        """

