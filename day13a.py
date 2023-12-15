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

DEBUG = False

class Pattern:

    def __init__(self, data):

        data = data.splitlines()

        self.horiz = self.binarise(data)
        self.vert = self.binarise(self.rotate(data))

    def binarise(self, data):
        p.bugprint(type(data[0]))
        return [int(row.replace("#", "1").replace(".", "0"), 2) for row in data]



    def rotate(self, data):

        new = [[] for i in range(len(data[0]))]
        # go through each row
        for row in data:
            # append each cell of this row to one column each
            for i, cell in enumerate(row):
                new[i] = [cell] + new[i]

        return ["".join(row) for row in new]

    def find_symmetry(self, horiz=False):

        data = self.horiz if horiz else self.vert

        if data[0] == data[1]:
            return 1

        stack = []
        reflecting = False
        line = None
        p.bugprint("reflection finding in", data)
        for y, row in enumerate(data):
            if stack:
                if row == stack[-1]:
                    if not reflecting:
                        line = y
                        print("set line to", line)
                        reflecting = True
                        print("reflecting now")
                    stack.pop(-1)

                    if len(stack) == 0:
                        return line
                    continue
                elif reflecting:
                    print("Resetting stack")
                    reflecting = False
                    line = None
            stack.append(row)
            print(stack)

        if line:
            p.bugprint("symmetry found at", line)
            return line
        else:
            raise NoSymmetryException("No symmetry found")

class NoSymmetryException(Exception):

    pass



def solve(data):
    total = 0

    data = "\n".join(data)

    p.bugprint(data)
    patterns = [Pattern(pat) for pat in data.split("\n\n")]

    cols, rows = 0, 0
    for pattern in patterns:

        try:
        
            cols += pattern.find_symmetry()
        except NoSymmetryException:
            try:
                rows += pattern.find_symmetry(horiz=True)
            except NoSymmetryException:
                print("no symmetry found")
                print(pattern.horiz)
                print(pattern.vert)
                input()

    p.bugprint(cols, rows)
    

    return cols + (100 * rows)



def tests():

    patterns = """##.#
##.#
....
.#..
#...///1///1

###
...
.#.
#.#
...
...///1///5

##
..///0///1

.#.##
#.###///0///4

.#...##
#....##
....###///0///6

.#.#
....
#.##
.###
.###
#.##
....
#.#.
.#.#
####
....
....
####///1///11

#.#..
.....
.....
#....///0///4

##..#
.....
.#..#
.....///0///3

...
...
#.#
.#.
.#.///1///1

.#.
...
...
#.#
.#.
.#.///1///5"""
    

    for test in patterns.split("\n\n"):

        pattern, horiz, expected = test.split("///")
        actual = Pattern(pattern).find_symmetry(horiz=bool(int(horiz)))
        print("actual...", actual)
        assert actual == int(expected)
        print("passed")

    input()
    
        


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    tests()
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
