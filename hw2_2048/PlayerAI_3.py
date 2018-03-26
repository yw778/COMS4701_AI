from BaseAI_3 import BaseAI
import time
import math

INFINITY = float("inf")
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

def get_children(grid, dirs=vecIndex):
    children = []

    for x in dirs:
        gridCopy = grid.clone()

        if gridCopy.move(x):
            children.append((x, gridCopy))

    return children

# def eval(state):
#     return state.getMaxTile()

def eval(state, cnt_w = 2.7, max_value_w = 0, smoothness_w = 1.5, monotonicity_w = 1.5, corner_max_w = 3):
    map = state.map
    cnt = 0
    max_value = -INFINITY
    smoothness = 0
    monotonicity = [0, 0, 0, 0] # left, right, up, down
    corner_max = 0

    for i in range(4):
        for j in range(4):
            if map[i][j] == 0:
                cnt += 1
            else:
                max_value = max(max_value, map[i][j])
                if j + 1 < 4 and map[i][j + 1]:
                    # smoothness -= abs(math.log2(map[i][j + 1]) - math.log2(map[i][j]))
                    smoothness += math.log2(map[i][j]) if map[i][j + 1] == map[i][j] else 0
                    # if map[i][j + 1] < map[i][j]:
                    #     monotonicity[0] += math.log2(map[i][j + 1]) - math.log2(map[i][j])
                    # else:
                    #     monotonicity[1] += math.log2(map[i][j]) - math.log2(map[i][j + 1])
                if i + 1 < 4 and map[i + 1][j]:
                    smoothness += math.log2(map[i][j]) if map[i + 1][j] == map[i][j] else 0
                    # smoothness -= abs(math.log2(map[i + 1][j]) - math.log2(map[i][j]))
                    # if map[i + 1][j] < map[i][j]:
                    #     monotonicity[2] += math.log2(map[i + 1][j]) - math.log2(map[i][j])
                    # else:
                    #     monotonicity[3] += math.log2(map[i][j]) - math.log2(map[i + 1][j])

    # left and right monotonicity
    for x in range(4):
        current = 0
        next = current + 1
        while(next < 4):
            while(next < 4 and not map[x][next]):
                next += 1
            if next >= 4:
                next -= 1
            current_v = math.log2(map[x][current]) if map[x][current] else 0
            next_v = math.log2(map[x][next]) if map[x][next] else 0
            if current_v > next_v:
                monotonicity[0] += next_v - current_v
            else:
                monotonicity[1] += current_v - next_v
            current = next
            next += 1

    # up and down monotonicity
    for y in range(4):
        current = 0
        next = current + 1
        while(next < 4):
            while(next < 4 and not map[next][y]):
                next += 1
            if next >= 4:
                next -= 1
            current_v = math.log2(map[current][y]) if map[current][y] else 0
            next_v = math.log2(map[next][y]) if map[next][y] else 0
            if current_v > next_v:
                monotonicity[2] += next_v - current_v
            else:
                monotonicity[3] += current_v - next_v
            current = next
            next += 1

    for x, y in [(0,3), (3,0), (0,0), (3,3)]:
        if map[x][y] == max_value:
            corner_max = 1

    return smoothness_w * smoothness + corner_max_w * corner_max * math.log2(max_value) + \
            + max_value_w * max_value + cnt_w * cnt  \
            + monotonicity_w * (max(monotonicity[0], monotonicity[1]) + \
                                max(monotonicity[2], monotonicity[3]))

class PlayerAI(BaseAI):
    def __init__(self):
        self.limit = 0.2
        self.time = None
        self.max_depth = None

    def getMove(self, grid):
        self.time = time.clock()
        return self.iterative_deepening(grid)

    def iterative_deepening(self, grid):
        self.max_depth = 0
        best_move = None
        while time.clock() - self.time <= self.limit:
            local_move = self.decision(grid)
            best_move = local_move if local_move is not None else best_move # 0 will be false here
            self.max_depth += 1
        return best_move

    # def iterative_deepening(self, grid):
    #     self.max_depth = 0
    #     best_move = self.decision(grid)
    #     return best_move

    def decision(self, state):
        child, _ = self.maximize(state, -INFINITY, INFINITY, 0)
        return child

    def maximize(self, state, alpha, beta, depth):

        if self.terminate_test(depth):
            return None, eval(state)

        maxChild = None
        maxUntility = -INFINITY

        for move, child in get_children(state):
            utility = self.minimize(child, alpha, beta, depth + 1)
            if utility > maxUntility:
                maxChild, maxUntility = move, utility
            if maxUntility >= beta:
                break
            if maxUntility > alpha:
                alpha = maxUntility

        return maxChild, maxUntility

    # combine chance layer and minimize layer in one function
    def minimize(self, state, alpha, beta, depth):
        if self.terminate_test(depth):
            return eval(state)

        minUntility = {2:INFINITY,
                       4:INFINITY}

        for value in [2, 4]:
            for cell in state.getAvailableCells():
                    child = state.clone()
                    child.insertTile(cell, value)
                    _, utility = self.maximize(child, alpha, beta, depth + 1)
                    if utility < minUntility[value]:
                        minUntility[value] = utility
                    if minUntility[value] <= alpha:
                        break
                    if minUntility[value] < beta:
                        beta = minUntility[value]

        return minUntility[2] * 0.9  + minUntility[4] * 0.1

    def terminate_test(self, depth):
        if time.clock() - self.time >= self.limit:
            return True
        if depth > self.max_depth:
            return True




