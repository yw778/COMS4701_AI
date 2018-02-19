#!/usr/bin/env python3
from collections import deque
from treeNode import TreeNode
from heapq import heappush, heappop
import time
import resource
class Puzzle(object):
    """
    This class represent the game
    """
    def __init__(self, initial_node, goal = (0,1,2,3,4,5,6,7,8)):
        self.initial_node = TreeNode(initial_node)
        self.goal = goal
        self.result = {}
        self.time = 0
        self.max_ram = 0
        self.node_expand = 0
        self.max_depth = 0

    def search(self, method):
        """
        initialize a search
        :param method: search method
        :return: None
        """
        self.time = time.time()
        if method == "bfs":
            self.__bfs()
        elif method == "dfs":
            self.__dfs()
        elif method == "ast":
            self.__ast()
        else:
            print("invalid input, please input as the following line")
            print("<method> must be bfs, dfs or ast")
            exit(1)

        self.time = time.time() - self.time
        self.max_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)

    def __bfs(self):
        """
        breath first search function
        enter queue in normal order
        move out of queue in normal order
        :return: None
        """
        frontier, explored = deque([self.initial_node]), {self.initial_node.state}
        while frontier:
            node = frontier.popleft()
            # print(node.state)
            explored.add(node.state)

            if self.__goalTest(node):
                self.result['end'] = node
                return

            self.node_expand += 1

            for neighbor in node.get_neighbors():
                if neighbor.state not in explored:
                    frontier.append(neighbor)
                    explored.add(neighbor.state)
                    self.max_depth = max(self.max_depth, neighbor.cost)

            # self.max_ram = max(self.max_ram,
            #                     resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024))

        return

    def __dfs(self):
        """
        depth search function
        enter stack in reverse order
        move out of stack in normal order
        :return: None
        """
        frontier, explored = [self.initial_node], {self.initial_node.state}
        while frontier:
            node = frontier.pop()
            explored.add(node.state)

            if self.__goalTest(node):
                self.result['end'] = node
                return

            self.node_expand += 1

            for neighbor in node.get_neighbors(reverse=True):
                if neighbor.state not in explored:
                    frontier.append(neighbor)
                    explored.add(neighbor.state)
                    self.max_depth = max(self.max_depth, neighbor.cost)

            # self.max_ram = max(self.max_ram,
            #                     resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024))

        return

    def __ast(self):
        """
        A* search function
        :return: None
        """
        frontier, explored = [self.initial_node], set()
        frontier_dic = {self.initial_node.state : self.initial_node.tot_cost}

        while frontier:
            node = heappop(frontier)
            # means the node should be decrease key in former steps
            if node.state not in frontier_dic:
                continue
            explored.add(node.state)
            del frontier_dic[node.state]

            if self.__goalTest(node):
                self.result['end'] = node
                return node

            self.node_expand += 1

            for neighbor in node.get_neighbors():
                if neighbor.state in explored:
                    continue
                elif neighbor.state not in frontier_dic:
                    heappush(frontier, neighbor)
                    frontier_dic[neighbor.state] = neighbor.tot_cost
                    self.max_depth = max(self.max_depth, neighbor.cost)
                elif neighbor.state in frontier_dic and frontier_dic[neighbor.state]> neighbor.tot_cost:
                    frontier_dic[neighbor.state] = neighbor.tot_cost
                    heappush(frontier, neighbor)
                    self.max_depth = max(self.max_depth, neighbor.cost)
        return

    def __goalTest(self, node):
        """
        test if reach the goal
        :param node:
        :return: boolean
        """
        return node.state == self.goal

    def __get_path(self, node):
        """
        get the path by backtracking
        :param node:
        :return:
        """
        path = []
        while node:
            if node.parent_move:
                path.append(node.parent_move)
            node = node.parent
        return path[::-1]

    def get_result(self):
        """
        get the result of the npuzzle game
        :return: dict
        """
        if not self.result:
            return None
        self.result["path_to_goal"] = str(self.__get_path(self.result["end"]))
        self.result["cost_of_path"] = str(self.result["end"].cost)
        self.result["nodes_expanded"] = str(self.node_expand)
        self.result["search_depth"] = str(self.result["end"].cost)
        self.result["max_search_depth"] = str(self.max_depth)
        self.result["running_time"] = self.time
        self.result["max_ram_usage"] = self.max_ram
        return self.result




























