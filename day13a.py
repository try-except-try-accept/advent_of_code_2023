from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 13
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#///aa
"""

DEBUG = True

def rotate(data):

    new = [[] for i in range(len(data[0]))]

    
    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i].append(cell)


    return new




def find_symmetry(pattern):
    reflect_stack = []
    for y, row in enumerate(pattern[1:]):
        if row == pattern[y-1]:
            print("row", row)
            print("pattern", pattern)
            return y


def solve(data):
    total = 0

    data = "\n".join(data)

    columns, rows = 0, 0
    for pattern in data.split("\n\n"):

        pattern = pattern.splitlines()
        for i in range(4):
            sym = find_symmetry(pattern)

            print("Found reflection line at", sym)
            if sym is not None:                
                if i % 2 == 1:
                    columns += sym - 1
                else:
                    rows += sym - 1
                break
                
            pattern = rotate(pattern)

    return columns + (100 * rows)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
