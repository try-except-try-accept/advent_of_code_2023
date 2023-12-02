from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import prod

PP_ARGS = False, False #rotate, cast int

DAY = 2
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green///2286"""

DEBUG = True

BLUE = 14
RED  = 12
GREEN = 13

def get_cubes(colour, row):
    return [int(i.split()[0]) for i in findall("\d{1,2} " + colour, row)]

def solve(data):
    powers = 0

    for row in data:
        blue = get_cubes("blue", row)
        red = get_cubes("red", row)
        green = get_cubes("green", row)
        powers += prod(map(max, [blue, red, green]))

    return powers




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
