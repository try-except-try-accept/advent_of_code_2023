from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 21
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........///16"""

DEBUG = True
STEPS = 6

def display(garden, stack, w, h):
    s = ""
    for y in range(h):
        for x in range(w):
            if (y, x) in stack[-1]:
                s += "O"
            else:
                s += garden[y][x]
        s += "\n"
    print(s)
    input()
    
def solve(data):
    count = 0
    h, w = len(data), len(data[0])
    garden = []
    for y in range(h):
        garden.append([])
        for x in range(w):
            if "S" == data[y][x]:
                start_x, start_y = x, y
            garden[-1].append(data[y][x])

    PLOT = "."
    VISITED = "O"

    stack = [[(h//2, w//2)]]

    for step in range(STEPS):
        print("step", step)
        layer = stack.pop(0)
        stack.append(set())
        
        for a, b in layer:
            for y, x in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                y += a
                x += b
                if 0 <= y < h and 0 <= x < w:
                    if garden[y][x] == PLOT:
                        stack[-1].add((y, x))
        #display(garden, stack, w, h)

    return len(stack[-1]) + 1

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        STEPS = 64
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
