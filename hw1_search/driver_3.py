#!/usr/bin/env python3
import sys
from puzzle import Puzzle
from os import linesep


def main():
    # print (sys.argv)
    start = [int(i) for i in sys.argv[2].split(",")]
    solver = Puzzle(tuple(start))
    solver.search(sys.argv[1])
    result = solver.get_result()
    # print (result)
    write_to_file(result)

def write_to_file(result):
    """
    write the result to files
    :param result: dict
    :return: None
    """
    cache = []
    cache.append("path_to_goal: " + result["path_to_goal"])
    cache.append("cost_of_path: " + result["cost_of_path"])
    cache.append("nodes_expanded: " + result["nodes_expanded"])
    cache.append("search_depth: " + result["search_depth"])
    cache.append("max_search_depth: " + result["max_search_depth"])
    cache.append("running_time: %.8f" % result["running_time"])
    cache.append("max_ram_usage: %.8f" % result["max_ram_usage"])

    with open("output.txt", 'w') as f:
        f.write("\n".join(cache))

if __name__ == "__main__":
    main()
