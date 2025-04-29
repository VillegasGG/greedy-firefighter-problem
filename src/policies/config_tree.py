from tree_generator import generate_random_tree

n_nodes = 15
tree, sequence, root = generate_random_tree(n_nodes, 5, 'min')
my_tree, _ = tree.convert_to_directed(root)