import unittest
import numpy as np
from tree_utils import Tree, tree_to_structure
import json

class TestTreeLegacy(unittest.TestCase):
    def setUp(self):
        # Configuración inicial de prueba
        self.nodes = np.array([0, 1, 2, 3])
        self.edges = [(0, 1), (1, 2), (1, 3)]
        self.positions = {0: [0.0, 0.0, 0.0], 1: [1.0, 1.0, 0.0], 2: [2.0, 2.0, 0.0], 3: [3.0, 3.0, 0.0]}
        self.tree = Tree(self.nodes, self.edges, nodes_positions=self.positions)
    

    def test_to_directed(self):
        # Verifica si el árbol se convierte correctamente a dirigido
        directed_tree, height = self.tree.to_directed(0)
        self.assertTrue(directed_tree.is_directed)
        self.assertEqual(height, 3)
        self.save_results_json(directed_tree, "test_to_directed.json")


    def test_add_firefighter_position(self):
        # Agrega una posición de bombero y verifica el resultado
        new_position = [4.0, 4.0, 0.0]
        self.tree.add_firefighter_position(new_position)
        expected_positions = np.array([self.positions[i] for i in self.nodes] + [new_position])
        np.testing.assert_array_equal(self.tree.nodes_positions, expected_positions)
        self.save_results_json(self.tree, "test_add_firefighter_position.json")

    def test_get_subtree_nodes(self):
        # Verifica los nodos en el subárbol
        directed_tree, _ = self.tree.to_directed(0)
        subtree_nodes = directed_tree.get_subtree_nodes(1)
        expected_nodes = np.array([1, 2, 3])
        np.testing.assert_array_equal(subtree_nodes, expected_nodes)
        self.save_results_json(directed_tree, "test_get_subtree_nodes.json")

    def test_tree_to_structure(self):
        # Convierte el árbol en estructura y verifica la integridad
        directed_tree, _ = self.tree.to_directed(0)
        tree_struct = tree_to_structure(directed_tree)
        self.assertEqual(tree_struct.n_nodes, len(self.nodes))
        self.assertEqual(tree_struct.height, directed_tree.height)
        self.save_results_json(directed_tree, "test_tree_to_structure.json")

    def save_results_json(self, tree, filename):
        data = {
            "height": tree.height,
            "is_directed": tree.is_directed,
            "root": tree.root,
            "edges": tree.edges.tolist()  # Convierte la matriz de NumPy a lista
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

if __name__ == '__main__':
    unittest.main()