from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int
REP_REQ = 9
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
        print("".join(row))
    print()


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
        print("Checking", data)
        print("Against", test)
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





def detect_subsequence(seq):

    ## go through each value in the sequence
    for i in range(len(seq)):
        ## compare against every other value - check for match
        for j in range(i+1, len(seq)):

        ## if match is found... ?
            if seq[i] == seq[j]:
                ## record this index as offset
                offset = i
                patt_length = 0
                ## scan forward and check while match is found
                while j+patt_length < len(seq) and seq[i+patt_length] == seq[j+patt_length]:
                    patt_length += 1
                       
                if patt_length > 10:
                    print("in", seq)
                    print(f"found offset {offset} and Patt length {patt_length}")
                    return offset , patt_length
    return None, None

def solve(data):
   
    total = 0
    new = []

    periods = []
    loads = []

    for cycle in range(1000000000):

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

        
                
        loads.append(load)
                
        
        if len(loads) > 50:

            offset, patt_length = detect_subsequence(loads)


            if patt_length:
                left = 1000000000 - cycle

                more_patterns = left // pattern_length

                
                remain = left %  pattern_length


                return loads[offset:][len(loads) % (more_patterns + remain)]

                

                

            
        

        


   

                

                

                       

 



    return total
pattern_length = 7
if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, debug, PP_ARGS)

    if p.check(TESTS, solve):
        pattern_length = 38 # hacky, gross
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
