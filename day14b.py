from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int
REP_REQ = 7
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


TARGET = 1000000000

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

cycle = None








debug = False

def flip(data):
    new = ["".join(reversed(row)) for row in data]

    display(data)
    return new

def rotate(data):


    new = [[] for i in range(len(data[0]))]
    # go through each row
    for row in data:
        # append each cell of this row to one column each
        for i, cell in enumerate(row):
            new[i] = [cell] + new[i]


    display(data)


    return ["".join(row) for row in new]

def display(data):
    if not debug:   return
    for row in data:
        p.bugprint("".join(row))
    p.bugprint()


def shift(data, west):
    new = []                 

    for row in data:
        cube_indices = set()
        for index, char in enumerate(row):
            if char == "#":
                cube_indices.add(index)
        chunks = row.split("#")
        
        for i in range(len(chunks)):
            chunks[i] = shift_chunk(chunks[i], west)

        new.append("#".join(chunks))


    display(new)
    return new

def shift_chunk(row, west=False):

    rollies = row.count("O")
    blanks = len(row) - rollies
    right = (blanks * ".") + (rollies * "O")
    left =  (rollies * "O") + (blanks * ".")
    
    return left if west else right

def check(data):
    
    if cycle:
        test = cycle.pop(0).splitlines()
        p.bugprint("Checking", data)
        p.bugprint("Against", test)
        assert data == test


def sum_load(data):
    total = 0
    for y, row in enumerate(data):
        mul = len(data)-y
        this_row = 0
        for i, char in enumerate(row):
            this_row += mul * (1 if char == "O" else 0)
        total += this_row
    return total



def rep_detected(patt):
    patt = [str(i) for i in patt]
    last_n = "".join(patt[-REP_REQ:])
    return "".join(patt).count(last_n) > 1

def identify_subsequence(loads, seq, sub_prefix, sub_repeat_idx):
    p.bugprint("cycle", sub_repeat_idx)
    offset = 0
    pattern = []
    recording = False
    ## go through every value
    for i in range(len(seq)):
    
        ## check if matches sub_prefix
        if seq[i:i+len(sub_prefix)] == sub_prefix:
            if recording:
                return offset, pattern
            
            recording = True
        ## record every value until next sub_prefix
        if recording:
            pattern.append(loads[i])
        else:
            offset += 1
                

def solve(data):
   
    total = 0
    new = []
    hashes = []
    loads = []

    for cycle in range(TARGET):

        for rotations_needed, west in ((1, False),
                                             (0, True),
                                             (3, False),
                                             (0, False)):

            for _ in range(rotations_needed):
                data = rotate(data)

            if rotations_needed:
                check(data)

            data = shift(data, west)

            check(data)

            if rotations_needed:
                for _ in range(4-rotations_needed):
                    data = rotate(data)
                check(data)

        display(data)
        load = sum_load(data)
        hashes.append(hash("".join(data)))
        loads.append(load)
                
        
        if len(loads) > REP_REQ and rep_detected(hashes):
            sub_prefix = hashes[-REP_REQ:]

            offset, pattern = identify_subsequence(loads, hashes, sub_prefix, cycle)

            p.bugprint(hashes)
            p.bugprint(f"Pattern prefix is {sub_prefix}")
            p.bugprint(f"Pattern begins at {offset}")
            p.bugprint(f"Pattern length is {len(pattern)}")
            p.bugprint(f"Pattern: {pattern}")

            return pattern[(TARGET-offset-1) % len(pattern)]


pattern_length = 7
if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, debug, PP_ARGS)

    if p.check(TESTS, solve):
        pattern_length = 38 # hacky, gross
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
