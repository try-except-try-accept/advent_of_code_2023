from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 15
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """rn=1///30"""

DEBUG = True


def solve(data):
    total = 0

        
    for step in data[0].split(","):
        current = 0
        for char in step:
            current += ord(char)
            current *= 17
            current %= 256
    
        total += current

    return total




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
