from time import sleep

import torch

from gameWrapper import GameWrapper
from teamNN.project2.DQN import DQN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env: GameWrapper = GameWrapper("map.txt")

# Get number of actions from gym action space
n_actions = len(env.action_list)
# Get the number of state observations
env.reset()
state = env.getStateImage()
# n_observations = len(state)
# (length, width) = state.shape

(c, width, length) = state.shape
model = DQN(c, n_actions).to(device)
test = torch.load("../models/policy_net.pt");
model.load_state_dict(torch.load("../models/policy_net.pt"))

terminated = False
while not terminated:
    state = torch.tensor(env.getStateImage(), dtype=torch.float32, device=device).unsqueeze(0)
    action_index = model(state).max(1)[1].view(1, 1)
    print("Action: " + str(env.action_list[action_index]))
    reward, terminated = env.nextStep(env.action_list[action_index])
    print("Reward: " + str(reward))
    sleep(0.1)

print(reward)
sleep(5)
