from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 14
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """.#O
OO.
O#.///9---O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....///64"""

# rotate right once
# shift
# rotate right x3
# flip once
# shift
# flip back
# rotate right x3
# flip
# shift
# rotate right once
# flip back


cycle = '''OO.
#O#
..O

.OO
#O#
..O

O#O
OO.
.#.

O#O
.OO
.#.

O#O
.OO
.#.

O#O
OO.
.#.

O..
#O#
OO.

..O
#O#
.OO

..O
#O#
.OO

.#.
OO.
O#O'''.split("\n\n")








DEBUG = True

def flip(data):
    new = ["".join(reversed(row)) for row in data]
    print("Flipped")
    display(data)
    return new

def rotate(data):


    new = [[] for i in range(len(data[0]))]
    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i] = [cell] + new[i]

    print("Rotated")
    display(data)


    return ["".join(row) for row in new]

def display(data):
    for row in data:
        print("".join(row))
    print()


def shift(data):
    new = []                 

    for row in data:
        cube_indices = set()
        for index, char in enumerate(row):
            if char == "#":
                cube_indices.add(index)
        chunks = row.split("#")
        
        for i in range(len(chunks)):
            chunks[i] = shift_chunk(chunks[i])

        new.append("#".join(chunks))

    print("shifted")
    display(new)
    return new

def shift_chunk(row, east=True):

    rollies = row.count("O")
    blanks = len(row) - rollies

    
    right = (blanks * ".") + (rollies * "O")
    left =  (rollies * "O") + (blanks * ".")
    
    return right if east else left

def check(data):
    
    if cycle:
        test = cycle.pop(0).splitlines()
        print("Checking", data)
        print("Against", test)
        assert data == test
        
        
def solve(data):
   
    total = 0
    new = []

    

    for rotations_needed, flip_needed in ((1, False),
                                         (0, True),
                                         (3, True),
                                         (0, False)):

        for _ in range(rotations_needed):
            data = rotate(data)

        if rotations_needed:
            check(data)
        
        if flip_needed:
            data = flip(data)
            check(data)

        data = shift(data)

        check(data)
        


        if rotations_needed:
            for _ in range(4-rotations_needed):
                data = rotate(data)
            check(data)
            
        if flip_needed:
            data = flip(data)
            check(data)
            
    display(data)

 

    for row in data:
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

        
