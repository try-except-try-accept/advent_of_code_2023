from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 1
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet///142
"""


DEBUG = True


def solve(data):
    count = 0
    score = 0
    for row in data:
        
        a = findall("\d", row)
        score += int(a[0] + a[-1])
        
        
    return score


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
