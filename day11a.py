from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from numpy import array, transpose
from copy import deepcopy
from math import dist
PP_ARGS = False, False #rotate, cast int

DAY = 11
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....///374"""

DEBUG = True


def rotate(data):

    new = [[] for i in range(len(data[0]))]

    display(data)
    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i].append(cell)


    return new


def expand_space(data):


    for i in range(2):
        new = []
        for row in data:
            r = 1
            if "#" not in row:
                r = 2
            for k in range(r):
                new.append(list(row))
   
        data = rotate(deepcopy(new))
    for i in range(2):
        new = rotate(deepcopy(new))

    return new

def display(data):
    for row in data:
        print(row)

def find_galaxies(data):

    for y, row in enumerate(data):

        for x, cell in enumerate(row):

            if cell == "#":
                yield (y, x)


def dist(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def solve(data):

    data = [list(row) for row in data]


    data = expand_space(data)
 
    galaxies = set(find_galaxies(data))
    total = 0
    done = set()
    for g in galaxies:
        for g2 in galaxies:
            this_pair = tuple(sorted((g, g2)))
            if g == g2 or this_pair in done:
                continue
            total += abs(dist(*this_pair))
            done.add(this_pair)
        
    

    return total




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
