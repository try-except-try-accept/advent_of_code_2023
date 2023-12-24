from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 12
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1///525152"""


    


DEBUG = True


def solve(data):
    count = 0

    for row in data:

        conditions, contiguous = row.split()
        contiguous = list(map(int, contiguous.split(","))) * 5

        conditions = "?".join([conditions for _ in range(5)])
        
        unknown = conditions.count("?")
        bin_length = 2**unknown

        i = 0


        conditions = conditions.replace(".", "0").replace("#", "1")
        while "?" in conditions:            
            conditions = conditions.replace("?", "{"+str(i)+"}", 1)
            i += 1

        print("testing", bin_length, "possibilities")

        this_row = 0
        for i in range(0, 2**unknown):
            fillers = bin(i)[2:].zfill(unknown)

            this_possibility = conditions.format(*fillers)

            bit_runs = this_possibility.split("0")
            if [len(b) for b in bit_runs if len(b)] == contiguous:
                this_row += 1

        print(row, ":", this_row, "possibilities")
                
          

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
