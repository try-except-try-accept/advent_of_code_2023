from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 9
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45///2"""

DEBUG = True


def solve(data):
    result = 0
    for row in data:
        histories = [list(map(int, row.split()))]
        while not all(val == 0 for val in histories[-1]):
            history = []
            for i in range(len(histories[-1])-1):
                history.append(histories[-1][i+1] - histories[-1][i])
            
            histories.append(history)

        histories[-1].insert(0, 0)


        for i in range(len(histories)-2, -1, -1):
            new = histories[i][0] - histories[i+1][0]
            histories[i].insert(0, new)
            
        
        result += histories[0][0]

##        for row in histories:
##            print(" ".join(str(n) for n in row).center(20))
##        
    return result



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
