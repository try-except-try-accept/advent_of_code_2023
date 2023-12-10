from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy
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
RED = "\033[38;2;255;0;0m"

HORIZ = "-"
VERT  = "|"
LEFTUP = "L"
LEFTDOWN = "F"
RIGHTDOWN = "7"
RIGHTUP = "J"

GO_UP = (-1, 0)
GO_DOWN = (1, 0)
GO_LEFT = (0, -1)
GO_RIGHT = (0, 1)


debug = False
HEIGHT, WIDTH = None, None
PIPES = "|-LJ7F.S"

NEIGH_COMBS = {
                HORIZ:
                    {
                        GO_DOWN: None,
                        GO_UP:None,
                        GO_RIGHT: RIGHTDOWN + RIGHTUP + HORIZ,
                        GO_LEFT:  LEFTDOWN + LEFTUP + HORIZ,
                    },
                VERT:
                    {
                        GO_DOWN: RIGHTUP + LEFTUP + VERT,
                        GO_UP: RIGHTDOWN + LEFTDOWN + VERT,
                        GO_RIGHT: None,
                        GO_LEFT: None
                    },
                LEFTUP:
                    {
                        GO_DOWN:None,
                        GO_UP: LEFTDOWN + RIGHTDOWN + VERT,
                        GO_RIGHT: RIGHTDOWN + RIGHTUP + HORIZ,
                        GO_LEFT:None
                    },
                RIGHTUP:
                    {
                        GO_DOWN:None,
                        GO_UP: LEFTDOWN + RIGHTDOWN + VERT,
                        GO_RIGHT:None,
                        GO_LEFT: LEFTDOWN + LEFTUP + HORIZ
                    },
                LEFTDOWN:
                    {
                        GO_DOWN: LEFTUP + RIGHTUP + VERT,
                        GO_UP: None,
                        GO_RIGHT: RIGHTUP + RIGHTDOWN + HORIZ,
                        GO_LEFT:None
                    },
                RIGHTDOWN:
                    {
                        GO_DOWN: LEFTUP + RIGHTUP + VERT,
                        GO_UP:None,
                        GO_RIGHT: None,
                        GO_LEFT: LEFTUP + LEFTDOWN + HORIZ
                    }
                }

BUFFER = 3
first_tile = "F"

def print_paths(paths, viewport, colour_map):
    if not debug:   return

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
    global debug
    count = 0
    debug = False

    path_sym = 0

    tiles = [list(row) for row in data]

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

    first_pass = True

    exp = [[(y, x)], [(y, x)]]

    path_count = 0

    paths = deepcopy(tiles)

    paths[y][x] = "0"

    visited = set()

    viewport = [x, x, y, y]

    p.bugprint("-----")
    print_paths(paths, viewport, colour_map)
    p.bugprint("-----")

    while first_pass or exp[0][-1] != exp[1][-1]:
        no_path = True
        for i, this_path in enumerate(exp):

            

            y, x = this_path[-1]

            viewport[0] = min(x, viewport[0])
            viewport[1] = max(x, viewport[1])
            viewport[2] = min(y, viewport[2])
            viewport[3] = max(y, viewport[3])

            
            tile = tiles[y][x]
            if tile == "S":
                tile = first_tile

            for (y_shift, x_shift), allowed in NEIGH_COMBS[tile].items():

                if not allowed:
                    continue
                
                new_y = y+y_shift
                new_x = x+x_shift

                if (new_y, new_x) in visited:
                    p.bugprint("Not going back to", new_y, new_x)
                    continue

                
                
                if 0 <= new_x < WIDTH:
                    if 0 <= new_y < HEIGHT:
                        this_move = tiles[new_y][new_x]
                        
                        if this_move in allowed:
                            path_count = len(exp[i])
                            exp[i].append((new_y, new_x))

                            path_sym += 1
                            while chr(path_sym).isprintable() == False:
                                path_sym += 1
                            paths[new_y][new_x] = chr(path_sym)
                            colour_map[new_y][new_x] = RED
                            visited.add((new_y, new_x))
                            no_path = False
                            p.bugprint(f"stage {path_count} {path_sym}")
                            p.bugprint("-----")
                            print_paths(paths, viewport, colour_map)
                            p.bugprint("-----")
                            break
                        else:
                            p.bugprint(f"Cant do {this_move} from {tiles[y][x]} only allowed {allowed}")
                    else:
                        p.bugprint("Off grid horiz")
                else:
                    p.bugprint("Off grid vert")
            
        if no_path:
            debug = True
            print_paths(paths, viewport, colour_map)
            return path_count


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, debug, PP_ARGS)

    if p.check(TESTS, solve):
        first_tile = "J"
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        

