from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 2
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green///8"""

DEBUG = True

BLUE = 14
RED  = 12
GREEN = 13

def get_cubes(colour, row):
    return [int(i.split()[0]) for i in findall("\d{1,2} " + colour, row)]

def get_id(row):
    return int(row.split()[1].replace(":", ""))

def solve(data):    

    ids = 0
    for row in data:
        blue = get_cubes("blue", row)
        red = get_cubes("red", row)
        green = get_cubes("green", row)
        if all(b <= BLUE for b in blue):
            if all(r  <= RED for r in red):
                if all(g <= GREEN for g in green):
                    ids += get_id(row)
                    
    return ids




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
