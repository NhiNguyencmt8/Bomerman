import time
import random
import collections
from utility import *

class Qlearning(object):

    def __init__(self):
        """Establish initial weights and learning parameters."""
        self.monsterweight = 5
        self.exitweight = 6
        #self.weight = collections.defaultdict(float) # Each w((f,a)) starts at 0
        self.epsilon = 0.05 # Exploration rate
        self.gamma = 0.99 # Discount factor
        self.alpha = 0.01 # Learning rate
    
            # monsterweight: int = 5
            # exitweight: int = 6
            # dfactor: float = 0.9 # constant?
            # alpha: float = 0.25 #constant?


    def state(self,wrld):
        """Return a description of the state of the environment."""
        s = character_location(wrld)
        
        # # Baseline feature noting how many pellets are left
        # s['pellets left'] = len(self.pellets) / float(self.density)
        
        # # YOU ADD MORE FEATURES
        
        return s
    
    def reward(self):  #get the reward of the next function or reward in general 
        r = 10
        return r


    def choose(self, s, actions,wrld):
        """Return an action to try in this state."""
        p = random.random()
        if p < self.epsilon:
            return random.choice(actions)
        else:
            return self.policy(s, actions,wrld)

    def policy(self, s, actions,wrld):
        """Return the best action for this state."""
        max_value = max([self.Q(s,a,wrld) for a in actions])
        max_actions = [a for a in actions if self.Q(s,a,wrld) == max_value]
        return random.choice(max_actions)

    def Q(self, s, a,wrld):
        qstate = (self.monsterweight*euclidean_distance_to_monster(wrld)) - (self.exitweight*euclidean_distance_to_exit(wrld))   #distancetobomb?
        qvalue = (qstate,s,a)
        print(qvalue)
        return qvalue 
        """Return the estimated Q-value of this action in this state."""
       # return 0 # YOU CHANGE THIS

    #def observe(self, s, a, sp, r, actions):

    def observe(self, state, action, r,actions,wrld):
        qmax = self.getMaxQ(state,actions,wrld)
        qstate = self.Q(state,action,wrld)
        q = qstate[0]
        delta = r + self.gamma*qmax - q
        self.monsterweight = self.monsterweight + self.alpha*delta*euclidean_distance_to_monster(wrld)
        self.exitweight = self.exitweight + self.alpha*delta*euclidean_distance_to_exit(wrld)
        return self.monsterweight,self.exitweight
        """Update weights based on this observed step."""

        # YOU FILL THIS IN
    def getMaxQ(self,state,actions,wrld):
        q_list = []
        for a in actions:
            qvalues = self.Q(state,a,wrld)
            print(qvalues)
            q = qvalues[0]
            print(q)
            q_list.append(q)
        if len(q_list) ==0:
            return 0
        return max(q_list)
    

    #our functions    
    # def getqvalue(state,action,wrld):
    #     qstate = (monsterweight*a_star_distance_to_monster(wrld)) - (exitweight*a_star_distance_to_exit(wrld))   #distancetobomb?
    #     qvalue = (qstate,state,action)
    #     return qvalue

    # def updateq(state,action,wrld):
    #     weightupdates = updateW(state,action)
    #     updatedq = (weightupdates[1]*a_star_distance_to_monster(wrld)) - (weightupdates[2]*a_star_distance_to_exit(wrld))
    #     return updatedq

    # def updateW(state, action):
    #         reward = 100 #how we get that?
    #         qmax = getMaxQ(state)
    #         q = getqvalue(state,action)
    #         delta = reward + dfactor*qmax - q
    #         monsterweight = monsterweight + alpha*delta*a_star_distance_to_monster
    #         exitweight = exitweight + alpha*delta*a_star_distance_to_exit
    #         return monsterweight,exitweight

    # def getMaxQ(state):
    #     q_list = []
    #     for a in eight_neighbors(state):
    #         q = getqvalue(state,a)
    #         q_list.append(q)
    #     if len(q_list) ==0:
    #         return 0
    #     return max(q_list)
        

