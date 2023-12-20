from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper, calculate_polygon_area
from shapely import Polygon
import re
PP_ARGS = False, False #rotate, cast int

DAY = 18
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)///62"""

BLACK = "\033[38;2;0;0;0m"
RED = "\033[38;2;255;0;0m"

DEBUG = True

def move(d, y, x):
    if d == "L":
        return y, x-1
    elif d == "R":
        return y, x+1
    elif d == "U":
        return y-1, x
    else:
        return y+1, x

def set_up_display(walls, x_min, x_max, y_min, y_max):
    s = []
    i = 48
    for y in range(y_min, y_max+1):
        s.append([])
        for x in range(x_min, x_max+1):
            if (y, x) in walls:
                s[-1].append(BLACK + "#")
            else:
                s[-1].append(" ")

    return s

def update_display(display, y, x):
    if display[y][x] == RED + "X":
        raise Exception("Already visited error")
    display[y][x] = RED + "X"
    for row in display[y-20:y+20]:
        print("".join(row))

    print()
    input()
    return display


def find_inner_area(walls, y, x, x_min, x_max, y_min, y_max):

    visited = set()
    search = [(y, x)]
    display = set_up_display(walls, x_min, x_max, y_min, y_max)
    area = 0

    while search:
        y, x = search.pop(-1)
        display = update_display(display, y, x)  
        visited.add((y, x))
        for y2, x2 in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            x_new = x + x2
            y_new = y + y2
            if x_min < x_new < x_max:
                if y_min < y_new < y_max:
                    if (y_new, x_new) not in walls:
                        if (y_new, x_new) not in visited.union(walls).union(set(search)):
                            search.append((y_new, x_new))
                        
    for row in display:
        print("".join(row))
    return len(visited)

def solve(data):
    count = 0

    wall = []
    colours = []

    
    y, x = 0, 0

    for row in data:
        if not row: continue
        direction, amount, colour = row.split()
        for _ in range(int(amount)):
            y, x = move(direction, y, x)
            wall.append((y, x))
            colours.append(int(colour[2:-1], 16))

  
    max_y = max(wall)[0]
    max_x = max(wall, key=lambda y: y[1])[1]
    min_y = min(wall)[0]
    min_x = min(wall, key=lambda y: y[1])[1]

    return find_inner_area(wall, max_y//2, max_x//2,
                           min_x, max_x, min_y, max_y) + len(wall)


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
