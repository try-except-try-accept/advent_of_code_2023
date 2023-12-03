from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import prod
PP_ARGS = False, False #rotate, cast int

DAY = 3
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..///467835   
"""

DEBUG = True
WIDTH = None
HEIGHT = None


def is_gear(cell):
    return cell == "*"

def get_part_numbers(data, y, x):    
    
    for ny in range(y-1, y+2):
        
        if ny < 0 or ny >= HEIGHT:
            continue
        nx = x - 1
        
        while nx < x + 2 and nx < WIDTH:
            if nx >= 0 and nx < WIDTH:
                this_num = data[ny][nx]
                spans_right = False
                if this_num.isdigit():                
                    lx = nx - 1
                    while data[ny][lx].isdigit():
                        this_num = data[ny][lx] + this_num
                        lx -= 1
                        if lx < 0:
                            break

                    rx = nx + 1
                    while data[ny][rx].isdigit():
                        this_num += data[ny][rx]
                        rx += 1
                        spans_right = True
                        if rx >= WIDTH:
                            break                        

                    if spans_right:
                        nx += rx
                    
                    yield int(this_num)                    
        
            nx += 1
            


def solve(data):
    count = 0
    global WIDTH, HEIGHT, DEBUG

    HEIGHT = len(data)
    WIDTH = len(data[0])
    print(HEIGHT, WIDTH)

    gear_ratio = 0
        
    for y, row in enumerate(data):
        x = 0
        for x, cell in enumerate(row):
            if is_gear(cell):
                gear_res = list(get_part_numbers(data, y, x))
                if len(gear_res) == 1:  continue
                gear_ratio += prod(gear_res)

    return gear_ratio




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        

