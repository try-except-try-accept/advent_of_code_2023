from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy
import numpy as np
from matplotlib.path import Path
from shapely.geometry import Polygon, Point

PP_ARGS = False, False #rotate, cast int


DAY = 10
TEST_DELIM = "xxx"
FILE_DELIM = "\n"
TESTS = """.....
.S-7.
.|.|.
.L-J.
.....///1xxx-L|F7
7S-7|
L|7||
-L-J|
L|-JF///1xxx...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........///4xxx..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........///4"""


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


debug = True
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

BUFFER = 3
first_tile = "F"


def get_polygon_points(pipe_path):
    return Polygon(pipe_path) # use shapely library instead
    
    global width, height
    '''borrowed from: https://stackoverflow.com/questions/21339448/how-to-get-list-of-points-inside-a-polygon-in-python'''
    y, x = np.meshgrid(np.arange(height), np.arange(width)) # make a canvas with coordinates
    y, x = y.flatten(), x.flatten()
    points = np.vstack((y,x)).T 
    p = Path(pipe_path) # make a polygon
    points_found = list(p.contains_points(points))

    x, y = 0, 0

    poly_points = set()

    while len(points_found):
        if points_found.pop(0):
            poly_points.add((y, x))
        x += 1
        if x % width == 0:
            y += 1
            x = 0

    return poly_points

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
    global debug, width, height
    count = 0
    debug = False

    path_sym = 0

    tiles = [list(row) for row in data]

    colour_map = [[WHITE for cell in row] for row in tiles]

    width = len(tiles[0])
    height = len(tiles)

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
    visited.add((y,x))

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

                
                
                if 0 <= new_x < width:
                    if 0 <= new_y < height:
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
            count = 0
            visited = list(visited)

            test_draw(visited)
            input()

            pipe_path = Polygon([(x, y) for (y, x) in visited])

            


            for y in range(height):
                for x in range(width):
                    this_point = Point(x, y)
 
                    if pipe_path.contains(this_point):
                        count += 1
                        print("Fooound")
                        print(this_point)
                        input()
            print("counted", count)
            return count
            
        

def test_draw(points):
    s = ""
    for y in range(height):
        for x in range(width):
            if (y, x) in points:
                s += "X"
            else:
                s += " "
        s += "\n"

    print(s)
    print()

def tests():

    test_poly = [(x, 1) for x in range(1, 10)] + [(x, 9) for x in range(1, 10)] + [(1, y) for y in range(1, 10)] + [(9, y) for y in range(1, 10)]

    global width, height
    width, height = 10, 10


    test_draw(test_poly)

    points_contained = get_polygon_points(test_poly)

    test_draw(points_contained)

        


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, debug, PP_ARGS)

    if p.check(TESTS, solve):
        first_tile = "J"
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        

