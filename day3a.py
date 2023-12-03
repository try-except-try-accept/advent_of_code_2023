from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 3
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..///4361   
"""

DEBUG = True
WIDTH = None
HEIGHT = None

def find_num(data, y, x):
    num = ""
    while True:
        num += data[y][x]
        x += 1
        if x >= WIDTH or data[y][x].isdigit() == False:
            break
    return num

def is_symbol(cell):
    return not (cell.isalpha() or cell.isdigit() or cell == ".")

def has_symbol_neighbours(data, y, x, num_length, num):
    for x_change in range(num_length):
        this_x = x + x_change
        
        for nx in range(-1, 2):
            for ny in range(-1, 2):
                new_y = ny+y
                new_x = nx+this_x
                if new_y < 0 or new_y >= HEIGHT:
                    continue
                if new_x < 0 or new_x >= WIDTH:
                    continue

                if is_symbol(data[new_y][new_x]):
                    return True
                
                

    return False

def solve(data):
    count = 0
    global WIDTH, HEIGHT, DEBUG

    HEIGHT = len(data)
    WIDTH = len(data[0])
    print(HEIGHT, WIDTH)

    nums = []
        
    for y, row in enumerate(data):
        x = 0
        while x < len(row):
            if data[y][x].isdigit():
                num = find_num(data, y, x)
                if num == "717":
                    DEBUG = True
                p.bugprint("Found a num", num)
                if has_symbol_neighbours(data, y, x, len(num), num):
                    nums += [int(num)]                    
                    p.bugprint("Has symbol neighbours!")
                    
                else:
                    p.bugprint("Did not have symbol neighbours")
                x += len(num)            
            else:
                x += 1
            


    return sum(nums)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        

