from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy
from random import randint
PP_ARGS = False, False #rotate, cast int

DAY = 10
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF///4---..F7.
.FJ|.
SJ.L7
|F--J
LJ...///8"""


WHITE = "\033[38;2;255;255;255m"
RED = (255, 0, 0)

ANSI = "\033[38;2;{0};{1};{2}m"

DEBUG = True
HEIGHT, WIDTH = None, None
PIPES = "|-LJ7F.S"

NEIGH_COMBS = ((-1, 0,  "|7FS"),
               (1,  0,  "|LJS"),
               (0,  -1, "-FLS"),
               (0,  1,  "-7JS"))

BUFFER = 3

result = None

def get_colour():
    colour = lambda: randint(0, 255)
    return (colour(), colour(), colour())


def explore(tiles, y, x, paths, viewport, colour_map, stage=0, colour=None, last=None, visited=None):

    global result

    
    if colour is None:
        colour = list(RED)
    if visited is None:
        visited = set()

    


    visited.add((y, x))

    viewport[0] = min(x, viewport[0])
    viewport[1] = max(x, viewport[1])
    viewport[2] = min(y, viewport[2])
    viewport[3] = max(y, viewport[3])

    path_count = 0
    path_sym = chr(stage + 48)
    paths[y][x] = path_sym
    colour_map[y][x] = ANSI.format(*colour)

    p.bugprint(f"stage {path_count} {path_sym}")
    p.bugprint("-----")
    print_paths(paths, viewport, colour_map)
    p.bugprint("-----")

    result = None
    
    for y2, x2, allowed in NEIGH_COMBS:
        new_x = x + x2
        new_y = y + y2


                            

        if (new_y, new_x) not in visited:
            if 0 <= new_x < WIDTH:
                if 0 <= new_y < HEIGHT:
                    if tiles[new_y][new_x] in allowed:

       
                        
                        path_count += 1
                        if path_count > 1:
                            print("colour change")
                            input()
                            colour = get_colour()
 

                        last = (y, x)

                        if paths[new_y][new_x] == "0":
                            print("BACK TO ZERO")
                        input()


                        explore(tiles, new_y, new_x, paths, viewport, colour_map, stage+1, colour, last, visited)
    

                    

def print_paths(paths, viewport, colour_map):
    if not DEBUG:   return

    s = ""

    for y, row in enumerate(paths):
        for x, tile in enumerate(row):
            if viewport[0]-BUFFER <= x <= viewport[1]+BUFFER:
                if viewport[2]-BUFFER <= y <= viewport[3]+BUFFER:
                    s += colour_map[y][x] + tile
        
        s += "\n"
                


    for row in s.splitlines():
        if not row: continue
        print(row.strip())
    
def solve(data):
    global WIDTH, HEIGHT, result
    count = 0
    result = None

    tiles = [list(row) for row in data]

    paths = deepcopy(tiles)

    colour_map = [[WHITE for cell in row] for row in tiles]

    WIDTH = len(tiles[0])
    HEIGHT = len(tiles)

    for y, row in enumerate(tiles):
        try:
            x = row.index("S")
            break
        except:
            pass

    print("Starting at", x, y)

    viewport = [x, x, y, y]
    

    explore(tiles, y, x, paths, viewport, colour_map)

    return result



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        

