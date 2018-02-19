#!/usr/bin/env python3
class TreeNode(object):
    """
    This class represents the search tree node
    """
    def __init__(self, state, parent_move = None, parent = None):
        self.state = state
        self.parent_move = parent_move
        self.parent = parent
        self.cost = parent.cost + 1 if parent else 0
        self.heuristics = self.__get_manhattan_dis()
        self.tot_cost = self.cost + self.heuristics

    def get_neighbors(self, reverse = False):
        """
        get the neighbors(children) of the current node
        :param reverse: boolean
        :return: list
        """
        neighbor = []
        zero_index = self.state.index(0)
        zero_row, zero_col = zero_index // 3, zero_index % 3

        if zero_row > 0:
            up_neighbor = list(self.state)
            up_neighbor[zero_index], up_neighbor[zero_index - 3] = \
                up_neighbor[zero_index - 3], up_neighbor[zero_index]
            neighbor.append(TreeNode(tuple(up_neighbor), 'Up', self))

        if zero_row < 2:
            down_neighbor = list(self.state)
            down_neighbor[zero_index], down_neighbor[zero_index + 3] = \
                down_neighbor[zero_index + 3], down_neighbor[zero_index]
            neighbor.append(TreeNode(tuple(down_neighbor), 'Down', self))

        if zero_col > 0:
            left_neighbor = list(self.state)
            left_neighbor[zero_index], left_neighbor[zero_index - 1] = \
                left_neighbor[zero_index - 1], left_neighbor[zero_index]
            neighbor.append(TreeNode(tuple(left_neighbor), 'Left', self))

        if zero_col < 2:
            right_neighbor = list(self.state)
            right_neighbor[zero_index], right_neighbor[zero_index + 1] = \
                right_neighbor[zero_index + 1], right_neighbor[zero_index]
            neighbor.append(TreeNode(tuple(right_neighbor), 'Right', self))

        return neighbor if not reverse else neighbor[::-1]

    def __get_manhattan_dis(self):
        """
        get manhanttan distance
        :return: int
        """
        cost = 0
        for i, v in enumerate(self.state):
            if v != 0:
                cost += abs(i % 3 - v % 3) + abs(i // 3 - v // 3)

        return cost

    def __str__(self):
        """
        for debug use
        :return:
        """
        return str(self.state)

    def __lt__(self, other):
        """
        comparator function for heapq
        :param other: the other node
        :return: boolean
        """
        order = {'Up':1,
                 'Down':2,
                 'Left':3,
                 'Right':4}
        if self.tot_cost == other.tot_cost:
            return order[self.parent_move] < order[other.parent_move]
        return self.tot_cost < other.tot_cost

if __name__ == "__main__":

    node1 = TreeNode((8,0,4,2,6,3,5,1,7))
    node2 = TreeNode((8,6,4,0,2,3,5,1,7))

    # print (node1.tot_cost, node2.tot_cost)





