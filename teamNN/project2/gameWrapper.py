import sys
import random
from typing import List, Any

import numpy as np
import pygame
from PIL import Image

from traningchracter import TrainingCharacter

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

from game import Game


class GameWrapper():
    """ A wrapper for the game, that adds findPossibleAction, and nextStep functions """

    # Public variables
    gameObj: Game = None
    mapFile = None

    # action_list: list[str] = ["w", "a", "s", "d", "wa", "wd", "sa", "sd", "wb", "wb", "ab", "sb", "db", "wab",
    #                                 "wdb", "sab", "sdb",
    #                                 "wbb", ""]
    action_list: list[str] = ["w", "a", "s", "d", "wa", "wd", "sa", "sd", "b"]
    action_space = my_array = [i for i in range(0, len(action_list))]

    def get_random_action(self):
        return random.choice(self.action_space)

    # Constuctor
    def __init__(self, filename):
        self.mapFile = filename
        self.reset()

    def reset(self):
        """ Resets the game """
        self.gameObj = Game.fromfile(self.mapFile)
        self.gameObj.add_character(TrainingCharacter("me", "C", 0, 0))

    def getStateImageOld(self):
        """ Returns the current state of the game as an image """
        # self.gameObj.display_gui()
        screen_array = pygame.surfarray.array3d(self.gameObj.screen)
        pil_image = Image.fromarray(screen_array)
        pil_image = pil_image.convert("RGB")
        # pil_image.save("image.jpg")

        downscale_factor = 4
        new_width = pil_image.width // downscale_factor
        new_height = pil_image.height // downscale_factor
        downscaled_image = pil_image.resize((new_width, new_height))
        # downscaled_image.save("downscaled_image.jpg")

        grayscale_image = downscaled_image.convert("L")
        # grayscale_image.save("grayscale_image.jpg")
        # print(np.array(grayscale_image).shape)
        return np.array(grayscale_image)

    def getStateImage(self):
        #Make an np array of size world.width() x world.height()
        #Fill it with 127s
        returnArray = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 127)

        for x in range(self.gameObj.world.width()):
            for y in range(self.gameObj.world.height()):
                if self.gameObj.world.wall_at(x, y): # Walls
                    returnArray[x][y] = 255
                if self.gameObj.world.explosion_at(x, y): # Explosion
                    returnArray[x][y] = 42
                if self.gameObj.world.characters_at(x, y): # Player
                    returnArray[x][y] = 0
                if self.gameObj.world.monsters_at(x, y): # Monster
                    returnArray[x][y] = 84
                if self.gameObj.world.exit_at(x, y): # Portal
                    returnArray[x][y] = 211
                if self.gameObj.world.bomb_at(x, y): # Bomb
                    returnArray[x][y] = 169

        pil_image = Image.fromarray(returnArray)
        # pil_image = pil_image.convert("RGB")
        # pil_image.save("image.png")

        return returnArray
        


    def nextStep(self, actionString):
        """ Performs the actionString on the game, and returns the reward """
        next(iter(self.gameObj.world.characters.values()))[0].setNextAction(actionString)
        (self.gameObj.world, self.gameObj.events) = self.gameObj.world.next()
        self.gameObj.display_gui()
        # pygame.time.wait(1)
        self.gameObj.world.next_decisions()
        return self.gameObj.world.scores["me"], self.gameObj.done()
