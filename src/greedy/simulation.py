from greedy.greedy_step import GreedyStep
from firefighter import Firefighter
from fire_state import FireState

class Simulation:
    def __init__(self, tree):
        self.tree = tree
        self.state = FireState(tree)
        self.firefighter = Firefighter(tree)
        self.greedy = GreedyStep(tree)
    
    def start_fire(self, initial_node):
        if initial_node in self.tree.nodes:
            self.state.burning_nodes.add(initial_node)
        else:
            raise ValueError("The initial node does not exist in the tree.")
        
        # Add a random firefighter position
        self.firefighter.add_random_initial_position()

    def propagate(self):
        new_burning_nodes = set()
        
        for node in self.state.burning_nodes:
            neighbors = self.tree.get_neighbors(node)  # Method in the Tree class to get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in self.state.burned_nodes and neighbor not in self.state.burning_nodes:
                    if neighbor not in self.state.protected_nodes:    # If node is not defended, it will burn
                        new_burning_nodes.add(neighbor)
        
        # Update the state of the nodes
        self.state.burned_nodes.update(self.state.burning_nodes)
        self.state.set_burning_nodes(new_burning_nodes)

    def is_completely_burned(self):
        """
        Checa si ya no hay nodos por quemar
        """
        if not self.state.burning_nodes and not self.state.burned_nodes:
            return False

        for node in self.state.burning_nodes:
            neighbors = self.tree.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.state.burned_nodes and neighbor not in self.state.burning_nodes and neighbor not in self.state.protected_nodes:
                    return False
        return True

    def is_protected_by_ancestor(self, node):
        path = self.tree.get_path_to_root(node)
        for ancestor in path:
            if ancestor in self.state.protected_nodes:
                return True
        return False

    def show_candidates(self, message, candidates, fire_time, time_ff_reach=None):
        print('-' * 50)
        print(message)
        print(f'Len candidates: {len(candidates)}')
        for candidate in candidates:
            print(f'Node: {candidate} | Fire time: {fire_time[candidate]} | Time to reach: {time_ff_reach[candidate] if time_ff_reach else "Not calculated"}')
        print('-' * 50)

    def get_candidates(self):
        candidates = set()
        final_candidates = set()
        unnafected_nodes = set(self.tree.nodes) - self.state.burned_nodes - self.state.protected_nodes - self.state.burning_nodes

        ff_distances = self.get_distances_from_firefighter(unnafected_nodes)
        fire_time = self.greedy.steps_to_reach_all()
      
        self.show_candidates("Candidates before first filter (After get unnafected_nodes):", unnafected_nodes, fire_time)

        for element in unnafected_nodes:
            is_protected = self.is_protected_by_ancestor(element)
            if not is_protected:
                candidates.add(element)

        self.show_candidates("Candidates after first filter (After protected by ancestor):", candidates, fire_time)

        time_ff_reach = {} # Time taken to reach each candidate
        for candidate in candidates:
            time_ff_reach[candidate] = ff_distances[candidate] / self.firefighter.speed

        # Filter candidates that can be reached before the fire
        for candidate in candidates:
            time_ff_reach_candidate = time_ff_reach[candidate]
            time_to_burn_candidate = fire_time[candidate]
            remaining_time = self.firefighter.get_remaining_time()
            if time_ff_reach_candidate > time_to_burn_candidate:
                continue
            elif remaining_time < 1:
                next_step_burn = time_to_burn_candidate - 1
                next_step_ff = time_ff_reach_candidate - remaining_time
                if next_step_ff < next_step_burn:
                    final_candidates.add((candidate, time_ff_reach[candidate]))
                else:
                    print(f'IMPORTANT!!  -- Node: {candidate} | Time to reach: {time_ff_reach[candidate]} | Time to burn: {fire_time[candidate]} but remaining time is {remaining_time}')
            else:
                if time_ff_reach[candidate] < time_to_burn_candidate:
                    final_candidates.add((candidate, time_ff_reach[candidate]))
            
        print(f'Final candidates:')
        print(f'{len(final_candidates)} candidates')
        print(set((node[0], node[1]) for node in final_candidates))

        return final_candidates

    def get_distances_from_firefighter(self, nodes):
        """
        Obtiene la distancia de todos los nodos al bombero
        """
        distances = {}
        for node in nodes:
            distances[int(node)] = float(self.firefighter.get_distance_to_node(node))
        return distances

    def select_node_to_protect_and_move(self):
        """
        - Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande (aunque este mas lejos)
        - Se mueve el bombero al nodo seleccionado
        """
        burned_and_burning_nodes = self.state.burned_nodes.union(self.state.burning_nodes)
        self.greedy.burned_nodes = burned_and_burning_nodes
        candidates = self.get_candidates()
        node_to_protect, node_time = self.greedy.get_node_to_protect(candidates, self.firefighter)
        print(f'Node to protect: {node_to_protect} | Time to reach: {node_time}')
        
        if node_to_protect:
            node_pos = self.tree.nodes_positions[node_to_protect]
            if(self.firefighter.get_remaining_time() >= node_time):
                self.state.protected_nodes.add(node_to_protect)
                self.firefighter.move_to_node(node_pos, node_time)
                self.firefighter.protecting_node = None
            else:
                self.firefighter.move_fraction(node_pos)
                self.firefighter.protecting_node = node_to_protect
                
            self.firefighter.print_info()
            return True

        else:
            print('No node to protect')
            return False

    def firefighter_action(self):
        """
        Turno del bombero
        """
        exist_candidate = True

        while(self.firefighter.get_remaining_time() > 0 and exist_candidate):
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
        self.firefighter.init_remaining_time()

        if not self.state.burning_nodes:
            self.start_fire(self.tree.root)
        else:
            self.firefighter_action()
            self.propagate()
