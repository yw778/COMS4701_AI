import math

def eval(state, cnt_w = 2.7, max_value_w = 0, smoothness_w = 1.5, monotonicity_w = 1.5, corner_max_w = 3):
    map = state.map
    cnt = 0
    max_value = -float("inf")
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

    return  smoothness_w * smoothness + corner_max_w * corner_max * math.log2(max_value) + \
                    + max_value_w * max_value + cnt_w * cnt  \
                    + monotonicity_w * (max(monotonicity[0], monotonicity[1]) + \
                                        max(monotonicity[2], monotonicity[3]))







