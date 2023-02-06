# This is necessary to find the main code
import sys

from utility import monster_location

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue
from expectimax import Node, expectimaxSearch, newNode, evaluate
import random

class TestCharacter(CharacterEntity):
    firstTime = True
    a_star_path = []
    prevMove = [0,0]


    def a_star(self, wrld, goal=None, start=None):
        if start is None:
            start = (self.x, self.y)  # Start at current position
        if goal is None:
            goal = wrld.exitcell  # Goal is exit cell

        cost_so_far = {start: 0}  # Dictionary of costs to get to each cell
        came_from = {start: None}  # Dictionary of where each cell came from

        frontier = PriorityQueue()  # Priority queue of cells to visit
        frontier.put(start, 0)

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            # Check all walkable neighbors of current cell
            for neighbor in self.eight_neighbors(wrld, current[0], current[1]):
                # Calculate cost to get to neighbor - 1 or 1.4
                new_cost = cost_so_far[current] + euclidean_dist(current, neighbor)

                # If neighbor has no path or new path is better, update path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + euclidean_dist(neighbor, goal)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current

        # Reconstruct path using came_from dictionary
        currPos = goal
        finalPath = []
        finalPath.append(goal)
        while currPos != start:
            currPos = came_from[currPos]
            finalPath.append(currPos)

        finalPath.reverse()
        return finalPath

    def is_cell_walkable(self, wrld, x, y):
        return wrld.exit_at(x, y) or wrld.empty_at(x, y) or wrld.monsters_at(x, y)

    def eight_neighbors(self, wrld, x, y):
        """
        Returns the walkable 8-neighbors cells of (x,y) in wrld
        """
        return_list = []

        if x != 0 and self.is_cell_walkable(wrld, x - 1, y):
            return_list.append((x - 1, y))
        if x != wrld.width() - 1 and self.is_cell_walkable(wrld, x + 1, y):
            return_list.append((x + 1, y))
        if y != 0 and self.is_cell_walkable(wrld, x, y - 1):
            return_list.append((x, y - 1))
        if y != wrld.height() - 1 and self.is_cell_walkable(wrld, x, y + 1):
            return_list.append((x, y + 1))
        if x != 0 and y != 0 and self.is_cell_walkable(wrld, x - 1, y - 1):
            return_list.append((x - 1, y - 1))
        if x != wrld.width() - 1 and y != 0 and self.is_cell_walkable(wrld, x + 1, y - 1):
            return_list.append((x + 1, y - 1))
        if y != wrld.height() - 1 and x != 0 and self.is_cell_walkable(wrld, x - 1, y + 1):
            return_list.append((x - 1, y + 1))
        if x != wrld.width() - 1 and y != wrld.height() - 1 and self.is_cell_walkable(wrld, x + 1, y + 1):
            return_list.append((x + 1, y + 1))

        return return_list

    def manhattan_distance_to_exit(self, wrld):
        return abs(self.x - wrld.exitcell[0]) + abs(self.y - wrld.exitcell[1])

    def euclidean_distance_to_exit(self, wrld):
        return ((self.x - wrld.exitcell[0]) ** 2 + (self.y - wrld.exitcell[1]) ** 2) ** 0.5

    def a_star_distance_to_exit(self, wrld):
        return len(self.a_star(wrld))

    def manhattan_distance_to_monster(self, wrld):
        if len(wrld.monsters) == 0:
            return 0
        else:
            return min(
                [abs(self.x - monster[1][0].x) + abs(self.y - monster[1][0].y) for monster in wrld.monsters.items()])

    def euclidean_distance_to_monster(self, wrld):
        if len(wrld.monsters) == 0:
            return 0
        else:
            return min([((self.x - monster[1][0].x) ** 2 + (self.y - monster[1][0].y) ** 2) ** 0.5 for monster in
                        wrld.monsters.items()])

    def a_star_distance_to_monster(self, wrld):

        if len(wrld.monsters) == 0:
            return 0
        else:
            return min(
                [len(self.a_star(wrld, (monster[1][0].x, monster[1][0].y))) for monster in wrld.monsters.items()])

    def monster_make_move(self, node, wrld):
        cells = []
        if len(wrld.monsters) > 0:
            x = monster_location(wrld)[0]
            y = monster_location(wrld)[1]
        else:
            x = node.dx
            y = node.dy
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if (x + dx >= 0) and (x + dx < wrld.width()):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if (y + dy >= 0) and (y + dy < wrld.height()):
                        # Is this cell walkable?
                        if not wrld.wall_at(x + dx, y + dy):
                            cells.append((x + dx, y + dy))
        return cells

    def do_astar(self, wrld):
        if self.firstTime:
            print("Character at", self.x, self.y)
            print("Exit at", wrld.exitcell)
            print("Explosions:", wrld.explosions)
            print("Monsters:", wrld.monsters)
            print("Euclidean distance to exit:", self.euclidean_distance_to_exit(wrld))
            print("Manhattan distance to exit:", self.manhattan_distance_to_exit(wrld))
            print("A* distance to exit:", self.a_star_distance_to_exit(wrld))
            print("Euclidean distance to monster:", self.euclidean_distance_to_monster(wrld))
            print("Manhattan distance to monster:", self.manhattan_distance_to_monster(wrld))
            print("A* distance to monster:", self.a_star_distance_to_monster(wrld))
            self.a_star_path = self.a_star(wrld)
            print("A* path to goal:", self.a_star_path)

            for point in self.a_star_path:
                # Mark path on world
                self.set_cell_color(point[0], point[1], Fore.RED + Back.GREEN)
            self.firstTime = False
        else:
            nextCell = self.a_star_path.pop(0)
            self.move(nextCell[0] - self.x, nextCell[1] - self.y)

    def expandChildren(self, rootNode, wrld, isBomberman):
        if isBomberman:  # If rootNode
            listChildren = self.eight_neighbors(wrld, rootNode.dx, rootNode.dy)
            for element in listChildren:
                childNode = newNode(0, element[0], element[1])
                value = evaluate(childNode, wrld)
                childNode.value = value
                rootNode.children.append(childNode)

                # print("Child expand from root node\n")
        else:  # If Monsters turn
            monster_cells = self.monster_make_move(rootNode, wrld)
            for element in monster_cells:
                childNode = newNode(0, element[0], element[1])
                childNode.value = 0
                rootNode.children.append(childNode)
        return rootNode


    def do(self, wrld):
        print("prevPose",self.prevMove[0], self.prevMove[1])
        rootNode = Node(0, self.x, self.y)
        print("Current pose", self.x, self.y)
        rootNode = self.expandChildren(rootNode, wrld, True)
        for i, child in enumerate(rootNode.children):
            child = self.expandChildren(child, wrld, False)
            rootNode.children[i] = child
            # print("Depth 1 child is", child.dx,child.dy,child.value)
            for j, grandchildren in enumerate(child.children):
                grandchildren = self.expandChildren(grandchildren, wrld, True)
                rootNode.children[i].children[j] = grandchildren
                # print("Depth 2 grandchild is", grandchildren.dx, grandchildren.dy, grandchildren.value)

        max_val = 0
        max_index = 0
        for i, child in enumerate(rootNode.children):
            value = expectimaxSearch(child, True) * 0.7 + child.value * 0.3
            child.value = value
            print("value is", child.dx, child.dy, value)
            # print("max_val is", max_val)
            if value >= max_val:
                if self.prevMove[0] != child.dx and self.prevMove[1] != child.dy:
                    print("swap")
                    max_val = value
                    max_index = i

        bestMove = rootNode.children[max_index]
        self.prevMove = [self.x, self.y]
        print("Best move is", bestMove.dx, bestMove.dy, bestMove.value)

        self.move(bestMove.dx - self.x, bestMove.dy - self.y)


def euclidean_dist(point_one, point_two):
    return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5
