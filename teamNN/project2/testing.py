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

# import torch
# import torch.nn as nn
# import torch.optim as optim
# import torch.nn.functional as F


# This is necessary to find the main code
import sys
from enum import Enum

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
# Import necessary stuff
from game import Game

sys.path.insert(1, '../teamNN')
from utility import *
from qlearning import Qlearning
from trainingcharacter import *
from gametest import *
 

# if gpu is to be used
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# g = Game.fromfile('map.txt')

env: GameWrapper = GameWrapper("map.txt")

g = env

# Main Loop
num_episodes = 50000
qlearning = Qlearning()

                              
training = TrainingCharacter("me", # name
                              "C",  # avatar
                              0, 0 ) # position)

#wrld = g.world

g.add_character(training
)

for episode in range(num_episodes):
        
        env.reset()
        s = qlearning.state(g.gameObj.world)
        done = False
        while not done:
            # chose random action
            actionString = ['w','a','s','d','b']
            a = qlearning.choose(s,actionString,g.gameObj.world)
            #Do random action,get next state and reward
            print(a)
            check = training.setNextAction(a)
            print(check)
            training.do(g.gameObj.world)
            sp = qlearning.state(g.gameObj.world)
            newlocation = character_location(g.gameObj.world)
            print(newlocation)
            r = qlearning.reward(g.gameObj.world,newlocation)
            qlearning.observe(s,a,sp,r,actionString,g.gameObj.world)
            newstate = qlearning.state(g.gameObj.world)
            s = newstate

        qlearning.update_epsilon

print(qlearning.qvalue)    

#return what we need            

