def greedy_action(obs):
    """
    Selects the best action based on the observation.
    """
    
    feasible_nodes = obs['feasible_nodes']
    print("Feasible nodes to protect:")
    best_time = float('inf')
    best_action = None
    for node in feasible_nodes:
        if node[1] < best_time:
            best_time = node[1]
            best_action = node[0]

    return best_action