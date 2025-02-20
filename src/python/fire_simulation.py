from python.greedy_step import GreedyStep
from python.firefighter import Firefighter

from collections import deque

import numpy as np

class FirePropagation:
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()  # Nodes that have already burned
        self.burning_nodes = set()  # Nodes currently on fire
        self.protected_nodes = set()  # Nodes that have been protected
        self.firefighter = Firefighter(tree)
        self.greedy = GreedyStep(tree)
    
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
                    if neighbor not in self.protected_nodes:    # If node is not defended, it will burn
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

        return burning_nodes, burned_nodes
    
    def is_protected_by_ancestor(self, node):
        """
        Checa si un nodo tiene un ancestro protegido
        """
        path = self.tree.get_path_to_root(node)
        for ancestor in path:
            if ancestor in self.protected_nodes:
                return True
        return False

    def get_candidates(self):
        """
        Obtiene los candidatos para ser protegidos
        """
        candidates = set()
        final_candidates = set()

        set_nodes = set(self.tree.nodes)
        
        unnafected_nodes = set_nodes - self.burned_nodes - self.protected_nodes - self.burning_nodes

        firefighter_distances = self.get_distances_from_firefighter(unnafected_nodes)
        fire_distances = self.greedy.steps_to_reach_all()
        speed = self.firefighter.speed
      
        print("Unnafected nodes:", len(unnafected_nodes))

        for element in unnafected_nodes:
            is_protected = self.is_protected_by_ancestor(element)
            if not is_protected:
                candidates.add(element)

        # Time taken to reach each candidate
        time_to_reach = {}
        for candidate in candidates:
            time_to_reach[candidate] = firefighter_distances[candidate] / speed
        
        # Show data:
        for candidate in candidates:
            print("Node:", candidate)
            print("Time to reach:", time_to_reach[candidate])
            print("Firefighter distance:", firefighter_distances[candidate])
            print("Speed:", speed)
            print("")

        # Filter candidates that can be reached before the fire
        for candidate in candidates:
            if time_to_reach[candidate] < fire_distances[candidate]:
                final_candidates.add(candidate)

        
        print("Candidates:", len(final_candidates))
        print("Candidates:", final_candidates)
        return final_candidates

    def greedy_step(self):
        """
        Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande
        """
        print("Greedy step")
        burned_and_burning_nodes = self.burned_nodes.union(self.burning_nodes)
        self.greedy.burned_nodes = burned_and_burning_nodes
        candidates = self.get_candidates()
        node_to_protect = self.greedy.get_node_to_protect(candidates)
        
        if node_to_protect:
            self.protected_nodes.add(node_to_protect)
            self.firefighter.move_to_node(self.tree.nodes_positions[node_to_protect])

    def get_distance_to_node(self, node):
        """
        Obtiene la distancia de un solo nodo al bombero
        """
        position = self.tree.nodes_positions[node]
        firefighter_position = self.firefighter.position
        return np.linalg.norm(position - firefighter_position)

    def get_distances_from_firefighter(self, nodes):
        """
        Obtiene la distancia de todos los nodos al bombero
        """
        distances = {}
        for node in nodes:
            distances[int(node)] = float(self.get_distance_to_node(node))
        return distances