from visualizer import TreeVisualizer
import json

def save_results(burned_nodes, burning_nodes, protected_nodes, filename):
    results = {
        "burned_nodes": [int(node) for node in burned_nodes],
        "burning_nodes": [int(node) for node in burning_nodes],
        "protected_nodes": [int(node) for node in protected_nodes]
    }
    with open('result/' + filename, 'w') as file:
        json.dump(results, file)

def vizualize_state(visualizer, env, step, folder):
    burning_nodes = env.state.burning_nodes
    burned_nodes = env.state.burned_nodes
    protected_nodes = env.state.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, env.firefighter.position, folder)
    