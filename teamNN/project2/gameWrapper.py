import sys
import random
import time
from typing import List, Any

import numpy as np
import pygame
from PIL import Image

from traningchracter import TrainingCharacter

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

from utility import euclidean_distance_to_exit
from game import Game


class GameWrapper():
    """ A wrapper for the game, that adds findPossibleAction, and nextStep functions """

    # Public variables
    gameObj: Game = None
    mapFile = None
    lastEucDist = 0

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
        minX = 0
        minY = 0
        maxX = 7
        maxY = 3
        startX = random.randint(minX, maxX)
        startY = random.randint(minY, maxY)
        self.gameObj.add_character(TrainingCharacter("me", "C", startX, startY))
        # print("Starting at: ", startX, startY)

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
        # Make an np array of size world.width() x world.height()
        # Fill it with 127s
        bomb_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        explosion_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        wall_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        exit_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        self_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)

        char_pos = [0, 0]

        for x in range(self.gameObj.world.width()):
            for y in range(self.gameObj.world.height()):
                if self.gameObj.world.wall_at(x, y):  # Walls
                    wall_array[x][y] = 1
                if self.gameObj.world.explosion_at(x, y):  # Explosion
                    explosion_array[x][y] = 1
                if self.gameObj.world.characters_at(x, y):  # Player
                    char_pos[0] = x
                    char_pos[1] = y
                    self_array[x][y] = 1
                if self.gameObj.world.monsters_at(x, y):  # Monster
                    # threat_array[x][y] = 1
                    pass
                if self.gameObj.world.exit_at(x, y):  # Portal
                    exit_array[x][y] = 1
                if self.gameObj.world.bomb_at(x, y):  # Bomb
                    bomb_array[x][y] = 1

        # pil_image = Image.fromarray(returnArray)
        # pil_image = pil_image.convert("RGB")
        # pil_image.save("image.png")

        # Flatten the array and conbine it
        # returnArray = np.concatenate((wall_array.flatten(), threat_array.flatten(), exit_array.flatten(), self_array.flatten()))
        returnArray = np.zeros((6, self.gameObj.world.width(), self.gameObj.world.height()))
        returnArray[0] = wall_array
        returnArray[1] = self_array
        returnArray[2] = exit_array
        returnArray[3] = bomb_array
        returnArray[4] = explosion_array
        returnArray[5] = np.zeros((self.gameObj.world.width(), self.gameObj.world.height()))
        returnArray[5][0][0] = euclidean_distance_to_exit(self.gameObj.world, char_pos) / 20

        return returnArray

    def nextStep(self, actionString):
        """ Performs the actionString on the game, and returns the reward """
        next(iter(self.gameObj.world.characters.values()))[0].setNextAction(actionString)
        (self.gameObj.world, self.gameObj.events) = self.gameObj.world.next()
        self.gameObj.display_gui()
        # pygame.time.wait(1000)
        self.gameObj.world.next_decisions()
        euclidean_distance = 0
        if self.gameObj.done():
            euclidean_distance = self.lastEucDist
            # print("Done")
            # pass
            # time.sleep(2)
        else:
            euclidean_distance = euclidean_distance_to_exit(self.gameObj.world) * 50
            self.lastEucDist = euclidean_distance
        if self.gameObj.world.scores["me"] > 0:
            winOrLoss = 500
        else:
            winOrLoss = -500

        # score = (self.gameObj.world.time - 5000) - int(euclidean_distance) + winOrLoss
        score = -int(euclidean_distance) + winOrLoss
        # print(score)
        return score, self.gameObj.done()
