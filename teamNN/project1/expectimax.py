# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
MIN_VALUE = -2147483647
MAX_VALUE = 2147483647


class Node:

    def __init__(self, value, dx, dy):
        self.value = value
        self.dx = dx
        self.dy = dy
        self.children = []


def newNode(value, dx, dy):
    temp = Node(value, dx, dy)
    return temp


def is_cell_walkable(wrld, x, y):
    return wrld.exit_at(x, y) or wrld.empty_at(x, y) or wrld.monsters_at(x, y)


def addChildren(node, wrld):
    x = node.dx
    y = node.dy
    return_list = []

    if x != 0 and is_cell_walkable(wrld, x - 1, y):
        return_list.append((x - 1, y))
    if x != wrld.width() - 1 and is_cell_walkable(wrld, x + 1, y):
        return_list.append((x + 1, y))
    if y != 0 and is_cell_walkable(wrld, x, y - 1):
        return_list.append((x, y - 1))
    if y != wrld.height() - 1 and is_cell_walkable(wrld, x, y + 1):
        return_list.append((x, y + 1))
    if x != 0 and y != 0 and is_cell_walkable(wrld, x - 1, y - 1):
        return_list.append((x - 1, y - 1))
    if x != wrld.width() - 1 and y != 0 and is_cell_walkable(wrld, x + 1, y - 1):
        return_list.append((x + 1, y - 1))
    if y != wrld.height() - 1 and x != 0 and is_cell_walkable(wrld, x - 1, y + 1):
        return_list.append((x - 1, y + 1))
    if x != wrld.width() - 1 and y != wrld.height() - 1 and is_cell_walkable(wrld, x + 1, y + 1):
        return_list.append((x + 1, y + 1))

    for element in return_list:
        childNode = newNode(0, element[0], element[1])
        node.children.append(childNode)
    return node


def evaluate(node, wrld):
    h = 0
    # Evaluating values
    x = node.dx
    y = node.dy
    if wrld.exit_at(x, y):
        h += 10000
    if wrld.wall_at(x, y):
        h -= 1000
    if wrld.empty_at(x, y):
        h += 100
        h -= abs(x - wrld.exitcell[0]) + abs(y - wrld.exitcell[1])
        # print("Distance to the portal", h)
    return h


def expValue(node, wrld):
    if node.children is None:
        return node.value
    v = 0
    evaluate(node, wrld)
    for successor in node.children:
        p = 1 / len(node.children)  # TODO: Change this into a probability function later
        v += p * successor.value
    return v


def maxValue(node):
    if node.children is None:
        return node
    v = MIN_VALUE
    for successor in node.children:
        v = max(v, expValue(successor))
    return v


# def expectimaxSearch(node, depth, isMax, wrld):
#     global bestSpot, bestHVal
#     if depth == 0:
#         node.value = evaluate(node, wrld)
#         bestHVal = node.value
#
#     if isMax:
#         addChildren(node, wrld)
#         # Travelling through all the children in the list to assign them some evalues
#         for child in node.children:
#             child.value = evaluate(child, wrld)
#             print("I stuck here")
#             if child.value >= 1000:  # Found a child move that leads us to the exit -> won move
#                 bestSpot = [child.dx, child.dy]
#                 bestHVal = child.value + depth * 1000
#                 bestMove = [bestSpot, bestHVal]
#                 print("Stuck here 1")
#                 return bestMove  # Return that move immediately
#             current = expectimaxSearch(child, depth - 1, False, wrld)
#             #current = expectimaxSearch(child, depth - 1, False, alpha, beta, wrld)
#             # if current[1] > alpha:
#             #     bestSpot = [child.dx, child.dy]
#             #     bestHVal = current[1]
#             #     alpha = bestHVal
#             #
#             # if alpha > beta:
#             #     break
#     else:
#
#         # print("Stuck here 2")
#         # if alpha == MIN_VALUE:
#         v = 0
#         for child in node.children:
#             child.value = evaluate(child, wrld)
#             p = 1 / len(node.children)  # TODO: Change this into a probability function later
#             v += p * child.value
#         #     print("Stuck here 3")
#         node.value = v
#         bestHVal = node.value
#         bestSpot = [node.dx, node.dy]
#         # else:
#         #     v = 0
#         #     total_p = 0
#         #     for child in node.children:
#         #         child.value = evaluate(child, wrld)
#         #         p = 1 / len(node.children)  # TODO: Change this into a probability function later
#         #         total_p += p
#         #         v += p * child.value
#         #         test = v + (1 - total_p) * beta
#         #         if test < alpha:
#         #             node.value = test
#         #             bestHVal = node.value
#         #             bestSpot = [node.dx, node.dy]
#         #             break
#         #     print("Stuck here 4")
#         #     node.value = v
#         #     bestHVal = v
#         #     bestSpot = [node.dx, node.dy]
#
#     bestMove = [bestSpot, bestHVal]
#     return bestMove

def makingTree(depth, rootNode):
    pass


# Getting expectimax
def expectimaxSearch(node, is_max):
    # Condition for Terminal node
    if node.children is None:
        print("at leaf -> exit")
        return node.value

    # Maximizer node. Chooses the max from the children
    if (is_max):
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
            total_c +=1 #Total Children
            total_v += expectimaxSearch(child, True)
        avgVal = total_v/total_c
        return avgVal

