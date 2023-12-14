from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 14
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....///136"""

DEBUG = True

def rotate(data):

    new = [[] for i in range(len(data[0]))]
    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i] = [cell] + new[i]

    return ["".join(row) for row in new]

def display(data):
    for row in data:
        print("".join(row))
    print()


def shift(row):

    rollies = row.count("O")
    blanks = len(row) - rollies

    return (blanks * ".") + (rollies * "O")
        
def solve(data):
    data = rotate(data)
    total = 0
    new = []
    for row in data:
        cube_indices = set()
        for index, char in enumerate(row):
            if char == "#":
                cube_indices.add(index)
        chunks = row.split("#")
        
        for i in range(len(chunks)):
            chunks[i] = shift(chunks[i])

        new.append("#".join(chunks))

    for row in new:
        print("final row", row, end=" = ")
        this_row = 0
        for i, char in enumerate(row):
            this_row += (i+1) * (1 if char == "O" else 0)
            
        print(this_row)
        total += this_row

    return total

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
