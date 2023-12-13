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
#....#..#///405
"""

### guessed: 14862 too low

DEBUG = True

def rotate(data):

    new = [[] for i in range(len(data[0]))]

    
    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i].append(cell)


    return new




def check_reflection(pattern):
    reflect_stack = []
    reflect_line = None

    # once we've started to pop, every row must then pop
    reflecting = True
    for y, row in enumerate(pattern):
        row = int("".join(row).replace("#", "1").replace(".", "0"), 2)
        print("processing", row)
        if reflect_stack and row == reflect_stack[-1]:
            reflect_stack.pop(-1)
            reflecting = True
            if not reflect_line:
                reflect_line = y
                
        else:
            reflect_stack.append(row)
            reflecting = True
        print(reflect_stack)

    if len(reflect_stack) > 1:
        reflect_line = None
    print("Reflects at", reflect_line)

    
    return reflect_line

def find_symmetry(pattern, cols, rows):
    for i in range(2):
        sym = check_reflection(pattern)

        print("Found reflection line at", sym)
        if sym is not None:                
            if i % 2 == 1:
                cols += sym
                return cols, rows
            else:
                rows += sym
                return cols, rows

        pattern = rotate(pattern)
    

def solve(data):
    total = 0

    data = "\n".join(data)

    cols, rows = 0, 0
    for pattern in data.split("\n\n"):
        print()

        pattern = pattern.splitlines()
        cols, rows = find_symmetry(pattern, cols, rows)

    print(cols, rows)

    return cols + (100 * rows)

def tests():

    tests = ['''
###.#.#
##.#.#.

.##.#.#
####.#.

.####.#
#.##.#.

.####.#
##.##..

#.#.##.
.#..##.

#.###..
.##.#..

.#.###..#
..##.#..#

.#.#.#.##.#.
#.#.#.#..#.#''',

             '''
##
##

.#
##
##

.#
#.
##
##
..

..
#.
.#
..
..

.#
#.
.#
#.
..
..''']
    for test_num, test_set in enumerate(tests):
        for sym, puzzle in enumerate(test_set.strip().split("\n\n")):
            print()
            cols, rows = find_symmetry(puzzle.splitlines(), 0, 0)

            if test_num % 2 == 0:
                assert cols == sym + 1
            else:
                assert rows == sym + 1








if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    tests()
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
