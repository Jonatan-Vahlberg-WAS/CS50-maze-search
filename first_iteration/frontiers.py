from enum import Enum

class Node():

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.distance_traversed = 0
    
    def set_distance_traversed(self, distance_traversed = 0):
        self.distance_traversed = distance_traversed

#Deapth first search DFS
class StackFrontier:

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[ : -1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1 :]
            return node

class GreedyBestFirstFrontier(StackFrontier):

    def __init__(self, goal = None):
        super().__init__()
        if goal is None:
            raise Exception("For this frontier a goal has to be submitted")
        self.goal = goal

    def get_distance(self, node):
        y_diff = node.state[0] - self.goal[0]
        x_diff = node.state[1] - self.goal[1]
        manhattan_distance = abs(y_diff) + abs(x_diff)
        return manhattan_distance

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node_index = 0
            sel_node = self.frontier[node_index]
            sel_node_distance = self.get_distance(sel_node)
            for i, node in enumerate(self.frontier):
                if sel_node is not None:
                    node_distance = self.get_distance(node)
                    if node_distance < sel_node_distance:
                        sel_node = node
                        node_index = i
                        sel_node_distance = node_distance
                         

            del self.frontier[node_index]
            return sel_node

class AStarFrontier(GreedyBestFirstFrontier):

    def get_distance(self, node):
        manhattan_distance = super().get_distance(node)
        return manhattan_distance + node.distance_traversed


class FrontierFactory():
     
    def create_frontier(self, frontier, goal):
        if frontier == "STACK":
            return StackFrontier()
        elif frontier == "QUEUE":
            return QueueFrontier()
        elif frontier == "GREEDY":
            return GreedyBestFirstFrontier(goal=goal)
        elif frontier == "ASTAR":
            return AStarFrontier(goal=goal)