from heapq import heappush, heappop
ROW = "ABCDEFGHI"
COL = "123456789"

class Entry(object):
    def __init__(self, len, idx):
        self.len = len
        self.idx = idx
    def __lt__(self, other):
        return self.len < other.len
    def __repr__(self):
        return(str([self.len, self.idx]))

class Sudoku(object):
    def __init__(self, board):
        self.dom = {}
        self.board = board
        self.init_dom()
        self.mrv = []
        self.mrv_cache = {}

    def init_dom(self):
        for r in ROW:
            for c in COL:
                if self.board[r+c] == 0:
                    self.dom[r+c] = set([1,2,3,4,5,6,7,8,9])
                else:
                    self.dom[r+c] = set([self.board[r+c]])

    def bt(self):
        # do first fc before backtracking
        # to guarantee constraint and cut search space
        # TA in piazza said we are allowed to do this
        for r in ROW:
            for c in COL:
                if self.board[r+c] != 0:
                    if not self.forward_checking(r, c)[1]:
                        return None

        # start backtracking search
        if self.bt_helper():
            return self.board

        return None

    def bt_helper(self):
        idx = None
        while len(self.mrv) > 0:
            entry = heappop(self.mrv)
            if self.mrv_cache[entry.idx] == entry:
                idx = entry.idx
                break

        if len(self.mrv) == 0 and idx is None:
            return True

        doms = self.dom[idx]

        for val in doms:
            if self.is_consistent(idx[0], idx[1], val):
                self.board[idx] = val
                self.dom[idx] = set([val])
                change, inference = self.forward_checking(idx[0], idx[1])
                if inference and self.bt_helper():
                    return True
                # backtrack
                self.board[idx] = 0
                self.dom[idx] = doms
                for cg_idx in change:
                    self.dom[cg_idx].add(val)
                    entry = Entry(len(self.dom[cg_idx]), cg_idx)
                    heappush(self.mrv, entry)
                    self.mrv_cache[cg_idx] = entry
        return False

    def is_consistent(self, i, j, val):
        for peer in self.get_neighbors(i, j):
            if val == self.board[peer]:
                    return False
        return True

    def forward_checking(self, i, j):
        # FC check for position i,j
        change = []
        val = self.board[i+j]
        for peer in self.get_neighbors(i, j):
            if val in self.dom[peer]:
                if len(self.dom[peer]) == 1:
                    return change, False
                self.dom[peer].remove(val)
                entry = Entry(len(self.dom[peer]), peer)
                heappush(self.mrv, entry)
                self.mrv_cache[peer] = entry
                change.append(peer)
        return change, True

    def get_neighbors(self, i, j):
        row_neighbors = [i+c for c in COL if c != j]
        col_neighbors = [r+j for r in ROW if r != i]
        i = ord(i) - ord('A')
        j = ord(j) - ord('1')
        box_neighbors = [chr(r + ord('A'))+chr(c + ord('1')) for r in range(i//3*3, i//3*3+3) \
                         for c in range(j//3*3, j//3*3 + 3) if r != i or c != j]
        return set(row_neighbors + col_neighbors + box_neighbors)












