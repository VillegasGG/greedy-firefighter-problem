import networkx as nx
import matplotlib.pyplot as plt
from generators import generate_random_tree
import pygraphviz as pgv

def tree_to_networkx(tree, root):
    G = nx.Graph()
    Gz = pgv.AGraph()
    
    # Agrega los nodos al grafo
    G.add_node(root)
    Gz.add_node(root)
    for node in tree.nodes: 
        if(node != root):
            G.add_node(node)
            Gz.add_node(node)
    
    # Agregar aristas
    n_nodes = tree.nodes.shape[0]
    for i in range(n_nodes):
        for j in range(n_nodes):
            if tree.edges[i, j] == 1:
                G.add_edge(i, j)
                Gz.add_edge(i, j)
    
    return G, Gz

def plotG(G):
    pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=500, edge_color='gray')

    plt.savefig("grafo_nx.png")  
    plt.close()

def plotGz(Gz):
    Gz.write("pygrapghviz.dot")
    Gz.layout(prog="dot")
    Gz.draw("grafo_gzdot.png")

    Gz.layout()
    Gz.draw("grafo_gz.png")

def plotGo(Gz):
    Gz.write("pygrapghviz.dot")
    Gz.layout(prog="dot")
    Gz.draw("grafo_godot.png")

    Gz.layout()
    Gz.draw("grafo_go.png")

def tree_orden(tree, root):
    Gz = pgv.AGraph()
    adj_matrix = tree.edges

    Gz.add_node(root)
    stack = [root]
    visitados = set() 

    while stack:
        actual = stack.pop() 
        if actual not in visitados:
            visitados.add(actual) 

            for posicion in range(len(adj_matrix[actual])):
                if adj_matrix[actual][posicion] == 1: 
                    Gz.add_node(posicion)
                    Gz.add_edge(actual, posicion) 
                    
                    if posicion not in visitados:
                        stack.append(posicion) 
    return Gz
        

def plot(tree, root):
    G, Gz = tree_to_networkx(tree, root)
    Go = tree_orden(tree, root)
    
    # for node, neighbors in G.adjacency():
    #     print(f"{node}: {list(neighbors.keys())}")
    plotG(G)
    plotGz(Gz)
    plotGo(Go)



n_nodes = 15
root_degree = 3
type_root_degree = "min"
tree, sequence, root = generate_random_tree(n_nodes, root_degree, type_root_degree)
print(tree.nodes)
print(root)
print("----------------------")
plot(tree, root)