from greedy.greedy_step import GreedyStep
from greedy.environment import Environment

class Simulation:
    def __init__(self, tree):
        self.env = Environment(tree)
        self.greedy = GreedyStep(tree)

    def firefighter_action(self):
        """
        Turno del bombero
        """
        exist_candidate = True

        while(self.env.firefighter.get_remaining_time() > 0 and exist_candidate):
            exist_candidate = self.greedy.select_node_to_protect_and_move(self.env)
            
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
            self.env.start_fire(self.env.tree.root)
        else:
            self.firefighter_action()
            self.env.propagate()
