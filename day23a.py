from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 23
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#///94"""

DEBUG = True


def solve(data):
    count = 0

    h = len(data)
    w = len(data[0])

    start = 0, 1
    goal  = h-1, w-2


    paths = [[start]]

    visited = set()

    completed = set()

    while len(paths):

        path = paths.pop(0)
        y, x = path[-1]

        if (y, x) == goal:
            completed.add(len(path)-1)

        path_combos = {".":[(-1, 0), (0, 1), (1, 0), (0, -1)],
                       "v":[(1, 0)],
                       ">":[(0, 1)],
                       "<":[(0, -1)]}
                    
        tile = data[y][x]

        path_found = False

        for y2, x2 in path_combos[tile]:

            x2 += x
            y2 += y

            next_coord = (y2, x2)
                        
            if y2 < 0 or y2 >= h or x2 < 0 or x2 >= w or data[y2][x2] == "#" or next_coord in path:
                continue

            paths.insert(-1, path + [next_coord])

    return max(completed)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
