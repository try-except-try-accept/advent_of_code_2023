from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy
PP_ARGS = False, False #rotate, cast int

DAY = 10
TEST_DELIM = "xxx"
FILE_DELIM = "\n"
TESTS = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........///4"""

"""xxxFF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L///10"""


WHITE = "\033[38;2;255;255;255m"
RED = "\033[38;2;255;0;0m"
GREEN = "\033[38;2;0;255;0m"
BLACK = "\033[38;2;0;0;0m"

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
height, width = None, None
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

BUFFER = 10
first_tile = "F"

def print_paths(viewport, colour_map):
    if not debug:   return

    s = ""

    for y, row in enumerate(colour_map):
        for x, colour_tile in enumerate(row):
            if viewport[0]-BUFFER <= x <= viewport[1]+BUFFER:
                if viewport[2]-BUFFER <= y <= viewport[3]+BUFFER:
                    s += colour_tile[0] + colour_tile[1]
        
        s += "\n"
                


    for row in s.splitlines():
        if not row: continue
        print(row.strip())

def calculate_area(y, x, visited, tiles, colour_map, viewport, deleted=None):
    global debug
    colour_map[y][x][0] = GREEN
    
    if deleted is None:
        deleted = set()
    explore = [(y, x)]


    while len(explore):
        node = explore.pop(0)
        y, x = node

        for y2 in range(-1, 2):
            for x2 in range(-1, 2):

                

                nx = x + x2
                ny = y + y2
                if nx >= width or nx < 0 or ny >= height or ny < 0:
                    continue

                key = (ny, nx)
                
                if key in visited:
                    pass
                elif key in deleted:
                    pass
                else:                    
                    colour_map[ny][nx][0] = BLACK
                    deleted.add(node)
                    if key not in explore:
                        explore.append(key)
                    

                #print_paths(viewport, colour_map)
                #p.bugprint()

    
    area = width * height
    in_the_loop = len(visited)
    debug = True
    print_paths(viewport, colour_map)
    print(WHITE)
    print(f"{area} tiles in total")
    print(f"{in_the_loop} were in the loop")
    print(f"{len(deleted)} were deleted")
    
    
    return colour_map, deleted
    
    
    
def solve(data):
    global  width, height, debug
    count = 0

    tiles = [list("."+row+".") for row in data]

    width = len(tiles[0])

    debug = False

    tiles.insert(0, "."*width)
    tiles.append("."*width)

    height = len(tiles)    

    

    colour_map = [[[WHITE, cell] for cell in row] for row in tiles]

    

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

    

    colour_map[y][x][1] = "0"

    visited = set()

    visited.add((y, x))

    viewport = [x, x, y, y]

    p.bugprint("-----")
    print_paths(viewport, colour_map)
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

                
                
                if 0 <= new_x < width:
                    if 0 <= new_y < height:
                        this_move = tiles[new_y][new_x]
                        
                        if this_move in allowed:
                            path_count = len(exp[i])
                            exp[i].append((new_y, new_x))
                            path_sym = chr(path_count + 32)
                            
                            colour_map[new_y][new_x] = [RED, path_sym]
                            visited.add((new_y, new_x))
                            no_path = False
                            break
                        else:
                            p.bugprint(f"Cant do {this_move} from {tiles[y][x]} only allowed {allowed}")
                    else:
                        p.bugprint("Off grid horiz")
                else:
                    p.bugprint("Off grid vert")
            
        if no_path and i == 1:
            print(path_count)
            
            print("part B")
            
            
            colour_map, deleted = calculate_area(0, 0, visited, tiles, colour_map, viewport)
            return (width * height) - len(visited) - len(deleted)
            colour_map, deleted = calculate_area(height//2, width//2, visited, tiles, colour_map, viewport, deleted)
            

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, debug, PP_ARGS)
    try:
        if p.check(TESTS, solve):
            first_tile = "J"
            puzzle_input = p.load_puzzle()
            puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
            print("FINAL ANSWER: ", solve(puzzle_input))
    except Exception as e:
        print(WHITE)
        print(e)
        

        

