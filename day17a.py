from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import inf as INF

PP_ARGS = False, False #rotate, cast int

DAY = 17
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533///102"""

DEBUG = True

graph = {}


def get_or_make_node(key):
    node = graph.get(key)
    if key is None:
        node = Node(key)
        graph[key] = node
    
    return node

def manhattan(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def solve(grid):
    count = 0
    h = len(grid)
    w = len(grid[0])
    start = (0, 0)
    goal = (h-1, w-1)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            
            for y_shift in range(3):
                for x_shift in range(3):



    

def a_star(grid, w, h, start, goal):

    current = None
    visited = set()

    data = {}
    for y in range(h):
        for x in range(w):
            data[(y,x)] = {"f":INF,
                            "g":0,
                            "h":manhattan(x, y, *goal),
                            "came from":None}
    # make an openlist containing only the starting node
    fringe = [current]
    # make an empty closed list
    closed = set()
    # while (the destination node has not been reached):
    current = None
    while current != goal:
        #  consider the node with the lowest f score in the open list
        current = sorted(fringe, key=lambda n: data[n]["f"])[0]
        #     if (this node is our destination node) :
        if current == goal:
            #         we are finished 
            continue
    
        #     if not:
        
        #          put the current node in the closed list and look at all of its neighbors
        closed.add(current)
        #         for (each neighbor of the current node):

        for y_change, x_change in ((-1, 0), (0, 1), (1, 0), (0, -1),
                     (-2, 0), (0, 2), (2, 0), (0, -2)
                     (-3, 0), (0, 3), (3, 0), (0, -3)):
            y, x = current[0] + y_change, current[1] + x_change
            # if (neighbor has lower g value than current and is in the closed list) :
            neighbour = (y, x)
            if data[neighbour]["g"] < data[current]["g"] and neighbour in closed:
                # replace the neighbor with the new, lower, g value 
                data[current]["g"] = data[neighbour]["g"]
                # current node is now the neighbor's parent            
                data[neighbour]["came from"] = current
            # else if (current g value is lower and this neighbor is in the open list ) :
            elif data[current]["g"] < data[neighbour]["g"] and neighbour in fringe:
                # replace the neighbor with the new, lower, g value 
                data[current]["g"] = data[neighbour]["g"]
                # change the neighbor's parent to our current node
                data[neighbour]["came from"] = current
                #  else if this neighbor is not in both lists:
            elif neighbour not in closed and neighbour not in fringe:
                #                 add it to the open list and set its g
                fringe.append(neighbour)
                

                    data[neighbour]["g"] += grid[y][x]


        visited.add(current)

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
