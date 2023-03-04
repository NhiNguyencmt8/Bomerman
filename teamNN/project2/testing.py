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
from monsters.stupid_monster import StupidMonster
 

# if gpu is to be used
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# g = Game.fromfile('map.txt')


# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# g = Game.fromfile('map.txt') 
random.seed(123) # TODO Change this if you want different random choices
env: GameWrapper = GameWrapper("map.txt")

g = env

# Get number of actions from gym action space
n_actions = len(env.action_list)
# Get the number of state observations
env.reset()
state = env.getStateImage()

# Main Loop
num_episodes = 500
qlearning = Qlearning()

                              
training = TrainingCharacter("me", # name
                              "C",  # avatar
                              0, 0 ) # position)



g.add_character(training
)

g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 9      # position
))

for episode in range(num_episodes):
        
        env.reset()
        
        s = qlearning.state(g.gameObj.world)
      
        
        while not g.gameObj.done():
            # chose random action
            actionString = ['w','a','s','d','b']
            a = qlearning.choose(s,actionString,g.gameObj.world)
            #Do random action,get next state and reward
            #training.setNextAction(a)
            
            env.nextStep(a)
            if not g.gameObj.done():
                sp = qlearning.state(g.gameObj.world)
                newlocation = character_location(g.gameObj.world)
                print("newlocation")
                print(newlocation)
               
                r = qlearning.reward(g.gameObj.world,newlocation)
                qlearning.observe(s,a,sp,r,actionString,g.gameObj.world)
                
                newstate = newlocation
                s = newstate
                print(qlearning.monsterweight,qlearning.exitweight) 
                print("newstate")
                print(newstate)
                print(s)
        
                


        
        
        qlearning.update_epsilon()
        print(qlearning.update_epsilon())

        

print(qlearning.monsterweight,qlearning.exitweight) 

 

#return what we need            

