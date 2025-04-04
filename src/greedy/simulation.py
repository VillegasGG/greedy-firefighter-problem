from greedy.greedy_step import GreedyStep
from firefighter import Firefighter
from fire_state import FireState
from greedy.environment import Environment

class Simulation:
    def __init__(self, tree):
        self.env = Environment(tree)
        self.greedy = GreedyStep(tree)

    def start_fire(self, initial_node):
        if initial_node in self.env.tree.nodes:
            self.env.state.burning_nodes.add(initial_node)
        else:
            raise ValueError("The initial node does not exist in the tree.")
        
        # Add a random firefighter position
        self.env.firefighter.add_random_initial_position()

    def propagate(self):
        new_burning_nodes = set()
        
        for node in self.env.state.burning_nodes:
            neighbors = self.env.tree.get_neighbors(node)  # Method in the Tree class to get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in self.env.state.burned_nodes and neighbor not in self.env.state.burning_nodes:
                    if neighbor not in self.env.state.protected_nodes:    # If node is not defended, it will burn
                        new_burning_nodes.add(neighbor)
        
        # Update the state of the nodes
        self.env.state.burned_nodes.update(self.env.state.burning_nodes)
        self.env.state.set_burning_nodes(new_burning_nodes)

    def is_completely_burned(self):
        """
        Checa si ya no hay nodos por quemar
        """
        if not self.env.state.burning_nodes and not self.env.state.burned_nodes:
            return False

        for node in self.env.state.burning_nodes:
            neighbors = self.env.tree.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.env.state.burned_nodes and neighbor not in self.env.state.burning_nodes and neighbor not in self.env.state.protected_nodes:
                    return False
        return True

    def is_protected_by_ancestor(self, node):
        path = self.env.tree.get_path_to_root(node)
        for ancestor in path:
            if ancestor in self.env.state.protected_nodes:
                return True
        return False

    def show_candidates(self, message, candidates, fire_time, time_ff_reach=None):
        print('-' * 50)
        print(message)
        print(f'Len candidates: {len(candidates)}')
        for candidate in candidates:
            print(f'Node: {candidate} | Fire time: {fire_time[candidate]} | Time to reach: {time_ff_reach[candidate] if time_ff_reach else "Not calculated"}')
        print('-' * 50)

    def show_candidates_tuple(self, message, candidates, fire_time):
        print(message)
        print(f'Len candidates: {len(candidates)}')
        for candidate in candidates:
            print(f'Node: {candidate[0]} | Time to reach: {candidate[1]} | Fire time: {fire_time[candidate[0]]}')
        print('-' * 50)

    def get_not_protected_nodes(self):
        candidates = set()

        unnafected_nodes = set(self.env.tree.nodes) - self.env.state.burned_nodes - self.env.state.protected_nodes - self.env.state.burning_nodes

        for element in unnafected_nodes:
            is_protected = self.is_protected_by_ancestor(element)
            if not is_protected:
                candidates.add(element)

        return candidates

    def get_final_candidates(self, candidates, fire_time, time_ff_reach):

        final_candidates = set()

        # Filter candidates that can be reached before the fire
        for candidate in candidates:
            time_ff_reach_candidate = time_ff_reach[candidate]
            time_to_burn_candidate = fire_time[candidate]
            remaining_time = self.env.firefighter.get_remaining_time()
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

    def get_candidates(self):

        first_candidates = self.get_not_protected_nodes()

        ff_distances = self.env.firefighter.get_distances_to_nodes(first_candidates)
        fire_time = self.greedy.steps_to_reach_all()

        time_ff_reach = {} # Time taken to reach each candidate
        for candidate in first_candidates:
            time_ff_reach[candidate] = ff_distances[candidate] / self.env.firefighter.speed
      
        # self.show_candidates("Candidates after first filter (After protected by ancestor):", first_candidates, fire_time, time_ff_reach)

        final_candidates = self.get_final_candidates(first_candidates, fire_time, time_ff_reach)
        
        # self.show_candidates_tuple("Final candidates:", final_candidates, fire_time)

        return final_candidates

    def select_node_to_protect_and_move(self):
        """
        - Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande (aunque este mas lejos)
        - Se mueve el bombero al nodo seleccionado
        """
        burned_and_burning_nodes = self.env.state.burned_nodes.union(self.env.state.burning_nodes)
        self.greedy.burned_nodes = burned_and_burning_nodes
        candidates = self.get_candidates()
        node_to_protect, node_time = self.greedy.get_node_to_protect(candidates, self.env.firefighter)
        print(f'Node to protect: {node_to_protect} | Time to reach: {node_time}')
        
        if node_to_protect:
            node_pos = self.env.tree.nodes_positions[node_to_protect]
            if(self.env.firefighter.get_remaining_time() >= node_time):
                self.env.state.protected_nodes.add(node_to_protect)
                self.env.firefighter.move_to_node(node_pos, node_time)
                self.env.firefighter.protecting_node = None
            else:
                self.env.firefighter.move_fraction(node_pos)
                self.env.firefighter.protecting_node = node_to_protect
                
            self.env.firefighter.print_info()
            return True

        else:
            print('No node to protect')
            return False

    def firefighter_action(self):
        """
        Turno del bombero
        """
        exist_candidate = True

        while(self.env.firefighter.get_remaining_time() > 0 and exist_candidate):
            exist_candidate = self.select_node_to_protect_and_move()
            
    def execute_step(self):
        """
        Ejecuta un paso de la simulacion:
        A) Si no hay nodos quemados:
            - Se inicia el fuego en el nodo raiz
            - Se coloca un bombero en una posicion aleatoria
        B) Si hay nodos quemados:
            - Turno del bombero dado que el anterior fue propagacion o inicio del fuego
            - Turno de la propagacion del fuego
        """
        self.env.firefighter.init_remaining_time()

        if not self.env.state.burning_nodes:
            self.start_fire(self.env.tree.root)
        else:
            self.firefighter_action()
            self.propagate()
