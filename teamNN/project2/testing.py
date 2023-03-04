import time

# import gym as gym
import numpy as np


from gametest import GameWrapper
import pygame


# # import gymnasium as gym
# import sys
# import math
# import random
# import matplotlib
# import matplotlib.pyplot as plt
# from collections import namedtuple, deque
# from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


# This is necessary to find the main code
import sys
from enum import Enum

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
# Import necessary stuff
from game import *

sys.path.insert(1, '../teamNN')
from utility import *
from qlearning import Qlearning
from trainingcharacter import *
from gametest import *
 

# if gpu is to be used
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# g = Game.fromfile('map.txt')
g = Game.fromfile('map.txt')

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# g = Game.fromfile('map.txt') 

# env: GameWrapper = GameWrapper("map.txt")

# g = env

# Get number of actions from gym action space
# n_actions = len(env.action_list)
# # Get the number of state observations
# env.reset()
# state = env.getStateImage()

# Main Loop
num_episodes = 50000
qlearning = Qlearning()

                              
training = TrainingCharacter("me", # name
                              "C",  # avatar
                              0, 0 ) # position)



g.add_character(training
)


for episode in range(num_episodes):
        
        s = qlearning.state(g.world)
        done = False
        while not done:
            # chose random action
            actionString = ['w','a','s','d','b']
            a = qlearning.choose(s,actionString,g.world)
            #Do random action,get next state and reward
            training.setNextAction(a)
            print(a)
            training.do(g.world)

            sp = qlearning.state(g.world)
            newlocation = character_location(g.world)
            print(newlocation)
            
            r = qlearning.reward(g.world,newlocation)
            qlearning.observe(s,a,sp,r,actionString,g.world)
            newstate = qlearning.state(g.world)
            s = newstate
            print("in while")
            g.go(100)  
            
            

        qlearning.update_epsilon
        print("done while")
        

print(qlearning.qvalue) 

 

#return what we need            

