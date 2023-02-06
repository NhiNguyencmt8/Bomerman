# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
MIN_VALUE = -2147483647
MAX_VALUE = 2147483647
from utility import a_star_distance_to_exit

class Node:

    def __init__(self, value, dx, dy):
        self.value = value
        self.dx = dx
        self.dy = dy
        self.children = []


def newNode(value, dx, dy):
    temp = Node(value, dx, dy)
    return temp


def evaluate(node, wrld):
    h = 0
    # Evaluating values
    x = node.dx
    y = node.dy
    if wrld.exit_at(x, y):
        h += 10000
        return h
    if wrld.empty_at(x, y):
        h += 100
        h -= a_star_distance_to_exit(wrld, node)
        if len(wrld.monsters.items()) > 0:
            h += min([((node.dx - monster[1][0].x) ** 2 + (node.dy - monster[1][0].y) ** 2) ** 0.5 for monster in
                     wrld.monsters.items()])
        # print("Distance to the portal", h)
    return h


# Getting expectimax
def expectimaxSearch(node, is_max):
    # Condition for Terminal node
    if not node.children:
        # print("at leaf -> exit")
        return node.value

    # Maximizer node. Chooses the max from the children
    if is_max:
        bestVal = 0
        prevVal = 0
        for child in node.children:
            bestVal = max(expectimaxSearch(child, False), prevVal)
            prevVal = bestVal
        return bestVal

    # Chance node. Returns the average of all the children
    else:  # is_chance Node
        total_v = 0
        total_c = 0

        for child in node.children:
            total_c += 1  # Total Children
            total_v += expectimaxSearch(child, True)
        avgVal = total_v / total_c
        return avgVal
