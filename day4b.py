from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 4
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11///30
"""

DEBUG = True

def solve(data):
    data = "\n".join(data)
    data = data.replace("  ", " ").splitlines()

    copies = [1 for _ in range(len(data))]

    for i, card in enumerate(data):

        mine, wins = card.split(" | ")
        mine = mine.split(":")[-1].strip().split(" ")
        wins = wins.strip().split(" ")
        matches = len(set(wins).intersection(set(mine)))

        if not matches:
            continue

        for x in range(1, matches+1):
            for j in range(copies[i]):
                copies[i+x] += 1
    
    return sum(copies)

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
