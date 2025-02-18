from python.greedy_step import GreedyStep
from python.firefighter import Firefighter

import numpy as np

class FirePropagation:
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()  # Nodes that have already burned
        self.burning_nodes = set()  # Nodes currently on fire
        self.protected_nodes = set()  # Nodes that have been protected
        self.firefighter = Firefighter(tree)
    
    def start_fire(self, initial_node):
        """
        Comienza el fuego en un nodo específico
        """
        if initial_node in self.tree.nodes:
            self.burning_nodes.add(initial_node)
        else:
            raise ValueError("The initial node does not exist in the tree.")
        
        # Add a random firefighter position
        self.firefighter.add_random_initial_firefighter_position()

    def propagate(self):
        """
        Simula un paso de la propagación del fuego
        """
        new_burning_nodes = set()
        
        for node in self.burning_nodes:
            neighbors = self.tree.get_neighbors(node)  # Method in the Tree class to get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in self.burned_nodes and neighbor not in self.burning_nodes:
                    # If node is not defended, it will burn
                    if neighbor not in self.protected_nodes:
                        new_burning_nodes.add(neighbor)
        
        # Update the state of the nodes
        self.burned_nodes.update(self.burning_nodes)
        self.burning_nodes = new_burning_nodes

    def is_completely_burned(self, burning_nodes, burned_nodes, protected_nodes):
        """
        Checa si ya no hay nodos por quemar
        """
        for node in burning_nodes:
            neighbors = self.tree.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in burned_nodes and neighbor not in burning_nodes and neighbor not in protected_nodes:
                    return False
        return True

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
        greedy_step.burned_nodes = burned_and_burning_nodes
        candidates = self.get_candidates()
        self.get_distances_from_firefighter()
        node_to_protect = greedy_step.get_node_to_protect(b_nodes, candidates)
        greedy_step.steps_to_reach_all()
        if node_to_protect:
            self.protected_nodes.add(node_to_protect)
            print("Protected nodes:", self.protected_nodes)

    def get_distance_to_node(self, node):
        """
        Obtiene la distancia de un solo nodo al bombero
        """
        position = self.tree.nodes_positions[node]
        firefighter_position = self.firefighter.actual_position
        print(f"Position: {position} Node: {node}")
        print(f"Firefighter position: {firefighter_position}")
        print(f"Distance: {np.linalg.norm(position - firefighter_position)}")
        return np.linalg.norm(position - firefighter_position)

    def get_distances_from_firefighter(self):
        """
        Obtiene la distancia de todos los nodos al bombero
        """
        distances = {}
        for node in self.get_candidates():
            distances[node] = self.get_distance_to_node(node)
        return distances