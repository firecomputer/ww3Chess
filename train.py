import gym
from env import *
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import pickle

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))
                
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

env = HOIEnv(0)

BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4

state = env.reset()
# Get number of actions from gym action space
n_actions = len(env.action_space)
# Get the number of state observations
n_observations = len(state[0])

try:
    with open("policy.pickle","cb") as fw:
        policy_net = pickle.dump(policy_net, fw)
    with open("target.pickle","cb") as fw:
        target_net = pickle.dump(target_net, fw)
except:
    policy_net = DQN(n_observations, n_actions).to(device)
    target_net = DQN(n_observations, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)


steps_done = 0


def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    '''
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            newPolicy = policy_net(state[0])
            pol = newPolicy.max(1)
            pol2 = pol[1].view(2)
            return pol2
    else:
        '''
    return torch.tensor([[env.action_space.sample()]], device=device, dtype=torch.long)


episode_durations = []
episode_x = []


def plot_durations():
    plt.figure(1)
    plt.clf()
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 3:
        means = durations_t.unfold(0, 3, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(2), means))
        plt.plot(episode_x, means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    print(policy_net(state_batch).shape)
    print(action_batch.shape)
    #action_batch = action_batch.reshape(128,82,3)[:,:,:2].reshape(128,164)
    state_action_values = policy_net(state_batch)[:128,0,:].reshape(128,246).gather(1, action_batch.reshape(128,246))

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device).expand((246,128)).reshape(128,246)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch.expand((123,128,2)).reshape(128,246)

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

if torch.cuda.is_available():
    num_episodes = 600
else:
    num_episodes = 100

for i_episode in range(num_episodes):
    # Initialize the environment and get it's state
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0).reshape(1,2,329)
    t = 0
    while True:
        action = select_action(state)
        env.setDuraction(t+1)
        observation, reward, done, info = env.step(action[0][0])
        reward = torch.tensor([reward], device=device)
        for id, ob in enumerate(observation):
            for idx, stating in enumerate(ob):
                if(stating == None):
                    observation[id][idx] = -1
        print(state.shape)
        next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        state = next_state

        print(state.shape)

        # Perform one step of the optimization (on the policy network)
        optimize_model()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)
        if done:
            episode_durations.append(t + 1)
            episode_x.append(i_episode)
            #plot_durations()
            env.reset()
            break
        t += 1
with open("policy.pickle","wb") as fw:
    pickle.dump(policy_net, fw)
with open("target.pickle","wb") as fw:
    pickle.dump(target_net, fw)

print('Complete')
plt.ioff()
plt.show()

'''
for episode in range(0,1):
    for _ in range(10000):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        observation_ger = observation[0]
        observation_sov = observation[1]
        reward_ger = reward[0]
        reward_sov = reward[1]
        if done:
            observation = env.reset()
            observation_ger = observation[0]
            observation_sov = observation[1]
            break
env.close()
env.isplayable = 1
with open("env.pickle","wb") as fw:
    pickle.dump(env, fw)
'''
