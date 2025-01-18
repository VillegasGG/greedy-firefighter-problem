from src.python.greedy_step import GreedyStep

class FirePropagation:
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()  # Nodes that have already burned
        self.burning_nodes = set()  # Nodes currently on fire
    
    def start_fire(self, initial_node):
        """
        Comienza el fuego en un nodo específico
        """
        if initial_node in self.tree.nodes:
            self.burning_nodes.add(initial_node)
        else:
            raise ValueError("The initial node does not exist in the tree.")

    def propagate(self):
        """
        Simula un paso de la propagación del fuego
        """
        new_burning_nodes = set()
        
        for node in self.burning_nodes:
            neighbors = self.tree.get_neighbors(node)  # Method in the Tree class to get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in self.burned_nodes and neighbor not in self.burning_nodes:
                    new_burning_nodes.add(neighbor)
        
        # Update the state of the nodes
        self.burned_nodes.update(self.burning_nodes)
        self.burning_nodes = new_burning_nodes

    def is_completely_burned(self):
        """
        Checa si todos los nodos del arbol han sido quemados o no
        """
        return len(self.burned_nodes) == len(self.tree.nodes)

    def display_state(self):
        """
        Estado actual del incendio
        """
        burning_nodes = {int(node) for node in self.burning_nodes}
        burned_nodes = {int(node) for node in self.burned_nodes}

        print("Burning nodes:", burning_nodes)
        print("Burned nodes:", burned_nodes)

        return burning_nodes, burned_nodes
    
    def get_candidates(self):
        """
        Obtiene los candidatos para ser protegidos
        """
        candidates = set()
        for node in self.burning_nodes:
            neighbors = self.tree.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.burned_nodes and neighbor not in self.burning_nodes:
                    candidates.add(neighbor)

        return candidates

    def greedy_step(self):
        """
        Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande
        """
        print("Greedy step")
        burned_and_burning_nodes = self.burned_nodes.union(self.burning_nodes)
        b_nodes = {int(node) for node in burned_and_burning_nodes}
        print("Burned and burning nodes:", b_nodes)
        greedy_step = GreedyStep(self.tree)
        candidates = self.get_candidates()
        print("Candidates:", candidates)
        greedy_step.get_node_to_protect(self.burning_nodes, candidates)
        # self.tree.protect_node(node_to_protect)
        # return node_to_protect

