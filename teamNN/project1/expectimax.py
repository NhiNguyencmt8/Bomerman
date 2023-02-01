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


def addChildren(node, wrld):
    actions = [-1, 0, 1]
    for dx in actions:
        for dy in actions:
            if (wrld.exit_at(node.dx + dx, node.dy + dy) or
                    wrld.empty_at(node.dx + dx, node.dy + dy)):
                node.children.append(newNode(0, node.dx, node.dy))
    return node


def evaluate(node, wrld):
    h = 0
    # Evaluating values
    for successor in node.children:
        x = successor.dx
        y = successor.dy
        if wrld.exit_at(x, y):
            h += 1000
        if wrld.wall_at(x, y):
            h -= 10
        if wrld.empty(x, y):
            h += 10

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


def expectimaxSearch(node, depth, isMax, alpha, beta, wrld):
    global bestSpot, bestHVal
    if depth == 0:
        node.value = evaluate(node, wrld)
        bestHVal = node.value

    if isMax:
        addChildren(node, wrld)
        # Travelling through all the children in the list to assign them some evalues
        for child in node.children:
            child.value = evaluate(child, wrld)

            if child.value >= 1000:  # Found a child move that leads us to the exit -> won move
                bestSpot = [child.dx, child.dy]
                bestHVal = child.value + depth * 1000
                bestMove = [bestSpot, bestHVal]
                return bestMove  # Return that move immediately

            current = expectimaxSearch(child, depth - 1, False, alpha, beta, wrld)
            if current[1] > alpha:
                bestSpot = [child.dx, child.dy]
                bestHVal = current[1]
                alpha = bestHVal

            if alpha > beta:
                break
    else:
        if alpha == MIN_VALUE:
            v = 0
            for child in node.children:
                child.value = evaluate(child, wrld)
                p = 1 / len(node.children)  # TODO: Change this into a probability function later
                v += p * child.value
            node.value = v
            bestHVal = node.value
            bestSpot = [node.dx, node.dy]
        else:
            v = 0
            total_p = 0
            for child in node.children:
                child.value = evaluate(child, wrld)
                p = 1 / len(node.children)  # TODO: Change this into a probability function later
                total_p += p
                v += p * child.value
                test = v + (1 - total_p) * beta
                if test < alpha:
                    node.value = test
                    bestHVal = node.value
                    bestSpot = [node.dx, node.dy]
                    break
            node.value = v
            bestHVal = v
            bestSpot = [node.dx, node.dy]

    bestMove = [bestSpot, bestHVal]
    return bestMove
