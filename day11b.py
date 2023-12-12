from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from numpy import array, transpose
from copy import deepcopy
from math import sqrt, dist
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
#...#.....///1030"""

def dist(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))



global expansion_rate

MILLION = chr(3452)

expansion_rate = 10

DEBUG = False


def rotate(data):

    new = [[] for i in range(len(data[0]))]

    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i].append(cell)

    return new


def expand_space(data, manual=False):

    global expansion_rate

    p.bugprint("Expanding", expansion_rate)

    for i in range(2):
        new = []
        for row in data:
            if row.count(".") + row.count(MILLION) == len(row):
                if manual:
                    for i in range(expansion_rate):
                        new.append(row)
                else:
                    new.append([MILLION for cell in row])
            else:
                new.append(row)
        data = rotate(deepcopy(new))
    for i in range(2):
        new = rotate(deepcopy(new))
    return new

def display(data):
    for row in data:
        p.bugprint("".join(row))
        
def find_galaxies(data):

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == "#":
                yield (y, x)


def find_distance(a, b, data):
    global expansion_rate

    p.bugprint("Finding distance between", a, "and", b)
    p.bugprint("in")
    p.bugprint(data)
    p.bugprint(len(data), len(data[0]))
    y, x = a
    y2, x2 = b

    y_steps = 0
    x_steps = 0

    while x != x2:
        p.bugprint(y, x)
        increase = 1
        x += 1 if x < x2 else -1
        if data[y][x] == MILLION:
            increase = expansion_rate
        x_steps += increase
        
    while y != y2:
        p.bugprint(y, x)
        increase = 1
        y += 1 if y < y2 else -1
        if data[y][x] == MILLION:
            increase = expansion_rate
        y_steps += increase
            
    my_dist = x_steps + y_steps
    p.bugprint("My dist is", my_dist)

    return my_dist

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
            total += abs(find_distance(*this_pair, data))
            done.add(this_pair)

    return total


def tests():
    global expansion_rate
    d = """#....
.....
.....
....#""".splitlines()

    display(d)

    for expansion_rate in [1, 2, 10, 50]:

        x = expand_space(d)
        display(x)
        y = expand_space(d, manual=True)
        p.bugprint("manually expanded")
        display(y)
        result = find_distance(*find_galaxies(y), y)
        assert find_distance(*find_galaxies(x), x) == result


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    tests()
    expansion_rate = 10

    if p.check(TESTS, solve):
        expansion_rate = 1000000
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
