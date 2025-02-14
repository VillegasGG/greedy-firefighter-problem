import time
from src.python.visualizer import TreeVisualizer
from src.python.fire_simulation import FirePropagation
from config_tree2 import my_tree, root

start_time = time.perf_counter()

def run_fire_simulation(fire, visualizer):
    step = 0
    burning_nodes, burned_nodes = fire.display_state()
    protected_nodes = fire.protected_nodes
    while not fire.is_completely_burned(burning_nodes, burned_nodes, protected_nodes):
        step += 1
        fire.greedy_step()
        fire.propagate()
        print(f"Paso {step}")
        burning_nodes, burned_nodes = fire.display_state()
        protected_nodes = fire.protected_nodes
        visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes)

    visualizer.plot_3d_final_state(burning_nodes, burned_nodes, protected_nodes)
    print('-' * 50)
    print('Datos finales:')
    print('Numero total de nodos: ' + str(len(my_tree.nodes)))
    print(f"Daño: {len(burned_nodes) + len(burning_nodes)}")
    print('-' * 50)

def simulate_fire(my_tree, visualizer, root):
    fire = FirePropagation(my_tree)
    fire.start_fire(root)
    visualizer.plot_3d_tree(my_tree, "images/initial_fire")
    step = 0
    burning_nodes, burned_nodes = fire.display_state()
    protected_nodes = fire.protected_nodes
    visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes)

    run_fire_simulation(fire, visualizer)

visualizer = TreeVisualizer(my_tree)
visualizer.plot_3d_tree(my_tree, "images/initial_tree")
visualizer.plot_2d_tree_with_root(my_tree, 0)

simulate_fire(my_tree, visualizer, root)

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Tiempo de ejecución total: {execution_time:.4f} segundos")