from greedy.greedy_step import GreedyStep
from firefighter import Firefighter
from fire_state import FireState
import copy

class Environment:
    def __init__(self, tree):
        self.tree = tree
        self.state = FireState(tree)
        self.firefighter = Firefighter(tree)

    def copy(self):
        """
        Copia el estado de la simulacion
        """
        return copy.deepcopy(self)

    