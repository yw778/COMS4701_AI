from BaseAI_3 import BaseAI
from random import randint
from Grid_3 import Grid
import time

class PlayerAI(BaseAI):


    def getMove(self, grid):
        self.time = time.time()
        moves = grid.getAvailableMoves()
        print ("from player AI")
        print(moves)
        exit(1)
        return moves[randint(0, len(moves) - 1)] if moves else None

