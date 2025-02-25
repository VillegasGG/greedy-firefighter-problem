import os
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from tree_utils import Tree

def load_positions(filename):
    with open(filename, "r") as file:
        nodes = []
        nodes_positions = []
        for line in file:
            node_data = line.split()
            nodes.append(int(node_data[0]))
            nodes_positions.append((float(node_data[1]), float(node_data[2]), float(node_data[3])))
        
        print("Nodes:", nodes)
        print("Nodes positions:", nodes_positions)
        return nodes, nodes_positions

def load_edges(filename):
    with open(filename, "r") as file:
        root = int(file.readline())
        edges = []
        for line in file:
            edges.append([float(node) for node in line.split()])

    print("Root:", root)
    print("Edges:", edges)
    return root, edges

def load_expected_results(filename):
    with open(filename, "r") as file:
        results = file.read()
        results_dict = eval(results)
        burning_nodes = set(results_dict["burning_nodes"])
        burned_nodes = set(results_dict["burned_nodes"])
        protected_nodes = set(results_dict["protected_nodes"])
        
    return burning_nodes, burned_nodes, protected_nodes

def create_positions_dict(nodes, nodes_positions):
    positions_dict = {}
    for i in range(len(nodes)):
        positions_dict[np.int64(nodes[i])] = np.array(nodes_positions[i])
    return positions_dict

def main():
    experiment = 1
    nodes, positions = load_positions("data/" + str(experiment) + "/positions.txt")
    root, edges = load_edges("data/" + str(experiment) + "/edges.txt")
    nodes_positions = create_positions_dict(nodes, positions)
    expected_burning_nodes, expected_burned_nodes, expected_protected_nodes = load_expected_results("data/" + str(experiment) + "/" + "results.json")


if __name__ == "__main__":
    main()