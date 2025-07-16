from ffenv.environment import FFProblemEnv

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from greedy import greedy_action

env = FFProblemEnv(
        space_limits=(-1, 1),
        speed=1.0,
        num_nodes=10,
        root_degree=5,
        type_root_degree='exact'
    )
obs = env.reset()
obs, reward, done, info = env.step(None)  # Start the fire propagation

while not done:
    action = greedy_action(obs)
    print(f"Selected action: {action}")
    obs, reward, done, info = env.step(action)

print("Final observation:")
print(f"On fire nodes: {obs['on_fire_nodes']}")
print(f"Protected nodes: {obs['protected_nodes']}")