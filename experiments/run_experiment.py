import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from greedy.visualizer import TreeVisualizer
from greedy.fire_simulation import FirePropagation
from greedy.fire_simulation import FireState
from config_tree import my_tree, root

def run_fire_simulation(fire, state, visualizer):
    step = 0
    state.display_state()
    burning_nodes = fire.getBurningNodes()
    burned_nodes = fire.getBurnedNodes()
    protected_nodes = fire.getProtectedNodes()
    while not fire.is_completely_burned(burning_nodes, burned_nodes, protected_nodes):
        step += 1
        fire.greedy_step()
        fire.propagate()
        print(f"Paso {step}")
        state.set_state(fire.getBurningNodes(), fire.getBurnedNodes(), fire.getProtectedNodes())
        burned_nodes = state.get_burned_nodes()
        burning_nodes = state.get_burning_nodes()
        protected_nodes = state.get_protected_nodes()
        state.display_state()
        visualizer.plot_fire_state(burning_nodes, burned_nodes, step, protected_nodes, fire.firefighter.position)


    visualizer.plot_3d_final_state(fire.burning_nodes, fire.burned_nodes, fire.protected_nodes, fire.firefighter.position)
    print('-' * 50 + f"\nDaño: {len(fire.burned_nodes) + len(fire.burning_nodes)}\n" + '-' * 50)

def simulate_fire(tree, visualizer, root):
    fire = FirePropagation(tree)
    state = FireState(tree)
    fire.start_fire(root)
    burned_nodes = fire.getBurnedNodes()
    burning_nodes = fire.getBurningNodes()
    protected_nodes = fire.getProtectedNodes()
    visualizer.plot_fire_state(burning_nodes, burned_nodes, 0, protected_nodes, fire.firefighter.position)
    run_fire_simulation(fire, state, visualizer)

def execute_experiment():
    visualizer = TreeVisualizer(my_tree)
    visualizer.plot_3d_tree(my_tree, "images/initial_tree")
    visualizer.plot_2d_tree_with_root(my_tree, root)
    print("Root:", root)
    simulate_fire(my_tree, visualizer, root)
    

def main():
    start_time = time.perf_counter()
    execute_experiment()
    end_time = time.perf_counter()
    print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
