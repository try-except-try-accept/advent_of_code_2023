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

class Pattern:

    def __init__(self, data):

        data = data.splitlines()
        self.orig = data
        self.horiz = self.binarise(data)
        self.vert = self.binarise(self.rotate(data))

    def binarise(self, data):
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
        stack = []
        reflecting = False
        line = None
        p.bugprint("reflection finding in", data)
        sym_lines = []
        for y, row in enumerate(data):
            print("compare row", row, 'stack', stack)
            if stack:
                # does this row reflect?
                if row == stack[-1]:
                    if not reflecting:
                        # first instance so record..
                        line = y
                        print("found los")
                        reflecting = True
                        
                    stack.pop(-1)
                    continue

                # doesn't reflect...
                elif reflecting:
                    print("broken symmetry reset line")
                    reflecting = False
                    stack = []
                    line = 0
            elif reflecting:
                return line
                    
            stack.append(row)


        if line:
            p.bugprint("symmetry found at", line)

            return line
        else:
            return 0 # no symmetry found
        


def show_symmetry(pattern, horiz, index):

    if not DEBUG: return

    num_labels = len(pattern[0]) if horiz else len(pattern)
    labels = [str(hex(i)[2:]) for i in range(1, num_labels+1)]

    sym_marker = list(labels)
    sym_marker[index-1] = ">" if horiz else "v"
    sym_marker[index] = "<" if horiz else "^"
    print(sym_marker)
    sym_marker = [" "  if thing not in "><^v" else thing for thing in sym_marker]
    print(index)
    print(sym_marker)

    if horiz:
        print(" ".join(labels))
        print(" ".join(sym_marker))
        for row in pattern:
            print(row.replace("#", "██").replace(".", "  "))
        print(" ".join(sym_marker))
        print(" ".join(labels))

    else:
        while sym_marker:
            print(labels.pop(0) + sym_marker.pop(0) + "".join(pattern.pop(0).replace("#", "██").replace(".", "  ")))

    


def solve(data):
    total = 0

    data = "\n".join(data)

    p.bugprint(data)
    patterns = [Pattern(pat) for pat in data.split("\n\n")]
    total = 0

    cols, rows = 0, 0
    for pattern in patterns:
        vert_los = pattern.find_symmetry()

        cols += vert_los

 
        horiz_los = pattern.find_symmetry(horiz=True)
        rows += horiz_los

        

        if vert_los and horiz_los:
            show_symmetry(pattern.orig, True, vert_los)

            show_symmetry(pattern.orig, False, horiz_los)
 
            input("multi los found")



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
.#.///1///5""" # <- deal with this test case
    

    for test in patterns.split("\n\n"):

        pattern, horiz, expected = test.split("///")
        actual = Pattern(pattern).find_symmetry(horiz=bool(int(horiz)))
        print("actual...", actual)
        assert actual == int(expected)
        print(test)
        print("passed")


    
        


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    tests()
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
