#!/usr/bin/env python
# coding:utf-8

"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""

import sys
import time
ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'
from sudoku import *


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """
    result = backtracking(board)
    # print()

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result



def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    sudoku = Sudoku(board)
    solved_board = sudoku.bt()
    # time.sleep(5.)
    return board_to_string(solved_board)




if __name__ == '__main__':

    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = string_to_board(sys.argv[1])
        write_solved(board)

    else:
        print("Running all from sudokus_start")
        # start_all = time.time()
        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()
        # cnt = 1
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            # start = time.time()
            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = string_to_board(line)

            # Append solved board to output.txt
            write_solved(board, mode='a+')
            # print("time for boards %d: %.4f seconds" % (cnt, (time.time() - start)))
            # cnt += 1

        # print("total time for all boards: %.4f seconds" % (time.time() - start_all))

        print("Finished all boards in file.")