# This is necessary to find the main code
import sys

sys.path.insert(0, '../../Bomberman')
# Import necessary stuff
from entity import CharacterEntity

sys.path.insert(2, '../teamNN')
from project2.qlearning import *


class TrainingCharacter(CharacterEntity):


    def setNextAction(self, actionString):
        self.nextActionString = actionString
        
    


    def do(self, wrld):
        # Commands
        dx, dy = 0, 0
        bomb = False
        # Handle input
        # for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
        for c in self.nextActionString:
            if 'w' == c:
                dy -= 1
            if 'a' == c:
                dx -= 1
            if 's' == c:
                dy += 1
            if 'd' == c:
                dx += 1
            if 'b' == c:
                bomb = True
        # Execute commands
        if bomb:
            self.place_bomb()
        self.move(dx, dy)