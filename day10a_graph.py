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

BLACK = "\033[38;2;0;0;0m"

WHITE = "\033[38;2;255;255;255m"
RED = (255, 0, 0)

ANSI = "\033[38;2;{0};{1};{2}m"

DEBUG = True
HEIGHT, WIDTH = None, None



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
                        GO_LEFT: LEFTDOWN + LEFTUP + HORIZ,
                    },
                LEFTDOWN:
                    {
                        GO_DOWN: LEFTUP + RIGHTUP + VERT,
                        GO_UP: None
                        GO_RIGHT: RIGHTUP + RIGHTDOWN + HORIZ,
                        GO_LEFT:None
                    },
                RIGHTDOWN:
                    {
                        GO_DOWN: LEFTUP + RIGHTUP + VERT,
                        GO_UP:None,
                        GO_RIGHT: None,
                        GO_LEFT: LEFTUP + LEFTDOWN + HORIZ
                    },
}

BUFFER = 3

result = None

def get_colour():
    colour = lambda: randint(0, 255)
    return (colour(), colour(), colour())

class Node:
    def __init__(self, y, x, pipe_type):
        self.x = x
        self.y = y
        self.pipe_type = pipe_type
        self.conns = []

    def __str__(self):
        return f"{self.pipe_type} {self.x} {self.y}"

    def add(self, new):
        self.conns.append(new)

def adjust_viewport(y, x, viewport):
    viewport[0] = min(x, viewport[0])
    viewport[1] = max(x, viewport[1])
    viewport[2] = min(y, viewport[2])
    viewport[3] = max(y, viewport[3])
    return viewport


def explore(start, viewport, colour_map):
    node = start
    first = True

    visited = set()

    

    explore = [node]
    while len(explore):
        node = explore.pop(0)
        viewport = adjust_viewport(node.y, node.x, viewport)
        print(WHITE+"Exploring", node.x, node.y)
        visited.add(node)
        connections = node.conns
        explore.extend(c for c in connections if c not in visited)
        colour_map[node.y][node.x][0] = WHITE
        print_paths(viewport, colour_map)
        
            
            
            
def print_paths(viewport, colour_map):
    if not DEBUG:   return

    s = ""

    for y, row in enumerate(colour_map):
        for x, (colour, tile) in enumerate(row):
            if viewport[0]-BUFFER <= x <= viewport[1]+BUFFER:
                if viewport[2]-BUFFER <= y <= viewport[3]+BUFFER:
                    s += colour + tile
        
        s += "\n"
                


    for row in s.splitlines():
        if not row: continue
        print(row.strip())            
            
    input()



def add_or_get_node(y, x, pipe_type, graph):
    key = (y, x)
    node = graph.get(key)
    if node is None:
        node = Node(y, x, pipe_type)
        graph[key] = node
    return node
        
    
def solve(data):
    global WIDTH, HEIGHT, result
    count = 0
    result = None

    tiles = [list(row) for row in data]

    paths = deepcopy(tiles)

    colour_map = [[[BLACK, cell] for cell in row] for row in tiles]

    WIDTH = len(tiles[0])
    HEIGHT = len(tiles)

    graph = {}

    


    for y, row in enumerate(tiles):

        for x, tile in enumerate(row):


            if tile == "S":
                origin = (y, x)
                tile = "F"
                tiles[y][x] = "F"

            node = add_or_get_node(y, x, tiles[y][x], graph)

            for y2, x2, allowed in NEIGH_COMBS:

                

                new_x, new_y = x+x2, y+y2

                if 0 <= new_x < WIDTH:
                    if 0 <= new_y < HEIGHT:

                        new_tile = tiles[new_y][new_x]

                        if new_tile in PIPE_TRANSFERS[tile]:

                            if new_tile in allowed:
                                

                                neighbour = add_or_get_node(new_y, new_x, new_tile, graph)

                                node.add(neighbour)
                                neighbour.add(node)

                                print(f"connected {node} to {neighbour}")
                                
    viewport = [origin[0], origin[0], origin[1], origin[1]]
                    
    start = graph[origin]

    explore(start, viewport, colour_map)


    return result



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    try:
        if  p.check(TESTS, solve):
            puzzle_input = p.load_puzzle()
            puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
            print("FINAL ANSWER: ", solve(puzzle_input))
    except:
        print(WHITE)

print(WHITE)
        


