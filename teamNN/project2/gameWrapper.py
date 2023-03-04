import sys
import random
import time
from typing import List, Any

import numpy as np
import pygame
from PIL import Image


# sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

from traningchracter import TrainingCharacter
from Bomberman.game import Game
from utility import *

class GameWrapper():
    """ A wrapper for the game, that adds findPossibleAction, and nextStep functions """

    # Public variables
    gameObj: Game = None
    mapFile = None
    lastEucDist = 0
    lastScore = 0
    progress = 0
    char_pos = [-1, -1]
    bomb_pos = [-1, -1]

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
        maxY = 0
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


    def getStateImageNew(self):
        # Make an np array of size world.width() x world.height()
        # Fill it with 127s
        return_array = np.zeros((self.gameObj.world.width(), self.gameObj.world.height()))

        for x in range(self.gameObj.world.width()):
            for y in range(self.gameObj.world.height()):
                if self.gameObj.world.wall_at(x, y):  # Walls
                    return_array[x][y] = 0.16
                if self.gameObj.world.explosion_at(x, y):  # Explosion
                    return_array[x][y] = .5
                if self.gameObj.world.characters_at(x, y):  # Player
                    self.char_pos[0] = x
                    self.char_pos[1] = y
                    return_array[x][y] = 1
                if self.gameObj.world.monsters_at(x, y):  # Monster
                    # threat_array[x][y] = 1
                    pass
                if self.gameObj.world.exit_at(x, y):  # Portal
                    return_array[x][y] = 0.81
                if self.gameObj.world.bomb_at(x, y):  # Bomb
                    self.bomb_pos[0] = x
                    self.bomb_pos[1] = y
                    return_array[x][y] = 0.33

        # pil_image = Image.fromarray(returnArray)
        # pil_image = pil_image.convert("RGB")
        # pil_image.save("image.png")

        # Flatten the array and conbine it
        priorsArray = np.zeros(3)
        priorsArray[0] = euclidean_distance_to_exit(self.gameObj.world, self.char_pos) / 20
        isInBombPathX : bool = False
        isInBombPathY : bool = False
        if self.char_pos[0] == self.bomb_pos[0]:
            isInBombPathX = True
            for y in range(min(self.char_pos[1], self.bomb_pos[1]), max(self.char_pos[1], self.bomb_pos[1])):
                if self.gameObj.world.wall_at(self.char_pos[0], y):
                    isInBombPathX = False
                    break
        if self.char_pos[1] == self.bomb_pos[1]:
            isInBombPathY = True
            for x in range(min(self.char_pos[0], self.bomb_pos[0]), max(self.char_pos[0], self.bomb_pos[0])):
                if self.gameObj.world.wall_at(x, self.char_pos[1]):
                    isInBombPathY = False
                    break
        if isInBombPathX:
            priorsArray[1] = 1
        if isInBombPathY:
            priorsArray[2] = 1

        return_array = np.append(return_array.flatten(), priorsArray)
        return return_array

    def getStateImage(self):
        # Make an np array of size world.width() x world.height()
        # Fill it with 127s
        bomb_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        explosion_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        wall_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        exit_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)
        self_array = np.full((self.gameObj.world.width(), self.gameObj.world.height()), 0)

        char_pos = [-1, -1]
        bomb_pos = [-1, -1]

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
                    bomb_pos[0] = x
                    bomb_pos[1] = y
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
        isInBombPathX : bool = False
        isInBombPathY : bool = False
        if char_pos[0] == bomb_pos[0]:
            isInBombPathX = True
            for y in range(min(char_pos[1], bomb_pos[1]), max(char_pos[1], bomb_pos[1])):
                if self.gameObj.world.wall_at(char_pos[0], y):
                    isInBombPathX = False
                    break
        if char_pos[1] == bomb_pos[1]:
            isInBombPathY = True
            for x in range(min(char_pos[0], bomb_pos[0]), max(char_pos[0], bomb_pos[0])):
                if self.gameObj.world.wall_at(x, char_pos[1]):
                    isInBombPathY = False
                    break
        if isInBombPathX:
            returnArray[5][0][1] = 1
        if isInBombPathY:
            returnArray[5][0][2] = 1

        return returnArray

    def render(self):
        self.gameObj.display_gui()


    def nextStep(self, actionString):
        """ Performs the actionString on the game, and returns the reward """
        next(iter(self.gameObj.world.characters.values()))[0].setNextAction(actionString)
        (self.gameObj.world, self.gameObj.events) = self.gameObj.world.next()
        # pygame.time.wait(1000)
        self.gameObj.world.next_decisions()


        winOrLoss = 0
        # if self.gameObj.done():
        #     euclidean_distance = self.lastEucDist
        #     if self.gameObj.world.scores["me"] > 0:
        #         winOrLoss = 5000
        #         # print("WIN")
        #     else:
        #         winOrLoss = -500
        #         # print("LOSS")
        # else:
        #     euclidean_distance = euclidean_distance_to_exit(self.gameObj.world) * 20
        #     self.lastEucDist = euclidean_distance


        # score = (self.gameObj.world.time - 5000) - int(euclidean_distance) + winOrLoss
        # score = euclidean_distance + winOrLoss + (self.gameObj.world.time - 5000)
        # score = self.gameObj.world.scores["me"] - euclidean_distance
        # returnScore = score - self.lastScore
        # self.lastScore = score

        returnScore = -1
        # print("Progess: "+ str(self.progress))
        # print("Char Pos: " + str(self.char_pos[1]))
        if self.char_pos[1] > self.progress:
            self.progress = self.char_pos[1]
            returnScore = 100

        if self.gameObj.done():
            if self.gameObj.world.scores["me"] > 0:
                returnScore = 5000
            else:
                returnScore = -200

        isInBombPath: bool = False
        if self.char_pos[0] == self.bomb_pos[0]:
            isInBombPath = True
            for y in range(min(self.char_pos[1], self.bomb_pos[1]), max(self.char_pos[1], self.bomb_pos[1])):
                if self.gameObj.world.wall_at(self.char_pos[0], y):
                    isInBombPath = False
                    break
        if self.char_pos[1] == self.bomb_pos[1]:
            isInBombPath = True
            for x in range(min(self.char_pos[0], self.bomb_pos[0]), max(self.char_pos[0], self.bomb_pos[0])):
                if self.gameObj.world.wall_at(x, self.char_pos[1]):
                    isInBombPath = False
                    break
        if isInBombPath:
            returnScore -= -1

        if self.bomb_pos[0] != -1:
            distanceToBomb = euclidean_dist(self.char_pos, self.bomb_pos)
            if distanceToBomb < 3:
                returnScore += 2

        # print(returnScore)
        return returnScore, self.gameObj.done()