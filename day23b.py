from re import search, match, findall
from collections import Counter, defaultdict
from helpers import PuzzleHelper, get_or_make_node
from math import sqrt, inf as INF
PP_ARGS = False, False #rotate, cast int

DAY = 23
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####.###
#...#...#.#.>...#.>.###
#.###.###.#.###.#.#.###
#.....###...###...#...#
#####################.#///154"""

MOVEMENTS = ((0, 1), (0, -1), (1, 0), (-1, 0))
DEBUG = True

RED = "\033[38;2;255;0;0m"
GREEN = "\033[38;2;0;255;0m"
BLACK = "\033[38;2;0;0;0m"



def get_h(here, there, max_heur):
    x1, y1 = here
    x2, y2 = there
    return abs(x2-x1) + abs(y2-y1)

def visualise(data, paths):
    print()
    s = ""
    for y in range(len(data)):
        for x in range(len(data[0])):
            char = BLACK + data[y][x]
            for i, p in enumerate(paths):
                if (y, x) in p["points"]:
                    char = RED + hex(i)[-1]
            s += char
        s += "\n"

    print(s)
     
def check_bounds(y, x, h, w):
    return 0 <= y < h and 0 <= x < w

def solve(data):
    h, w = len(data), len(data[0])

    vertices["S"] = 0, 1
    vertices["E"] = h-1, w-2
    maze = [list(row) for row in data]
    vertices = {}
    vertex_num = 0
    # mark all vertices with X
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if data[y][x] in "v>":
                label = chr(vertex_num + 199)
                maze[y][x] = label
                vertex_num += 1
                vertices[label] = (y, x)

    
    g = {}

    # set up weighted graph

    for row in maze:
        print("".join(row))


    for label, vertex in vertices.items():
        g[label] = get_or_make_node(label, g, vertex)
        paths = [[vertex]]

        print(label, "connects to")
        
        while len(paths):

            path = paths.pop(0)

            y, x = path[-1]

            if (y, x) in vertices.values() and (y, x) != vertex:
                print("\t", maze[y][x],  "in", len(path), "steps")
                neighbour = get_or_make_node(label, g, (y, x))
                g[label].add_connection(neighbour, len(path))
                neighbour.add_connection(g[label], len(path))
                continue

            for y2, x2 in MOVEMENTS:
                y2 += y
                x2 += x
                next_coord = (y2, x2)
                if (not check_bounds(y2, x2, h, w)) or data[y2][x2] == "#" or next_coord in path:
                    continue
                paths.insert(0, path + [next_coord])

    



def solve_dfs(data):
    count = 0

    h = len(data)
    w = len(data[0])

    start = 0, 1
    goal  = h-1, w-2


    paths = [[start]]

    visited = set()

    completed = set()

    while len(paths):

        path = paths.pop(0)
  
        y, x = path[-1]

    

        if (y, x) == goal:
            completed.add(len(path)-1)

        dead_end = True
        for y2, x2 in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            
            y2 += y
            x2 += x
            next_coord = (y2, x2)
            if (y2 < 0 or y2 >= h or x2 < 0 or x2 >= w or data[y2][x2] == "#"):
                continue
            if next_coord in path:
                dead_end = False
                continue

            dead_end = False
        
            paths.insert(0, path + [next_coord])

        if dead_end:
            print("Dead end at ", y2, x2)      



    return max(completed)


def solve_a_star(data):
    count = 0

    h = len(data)
    w = len(data[0])

    max_heur = sqrt(w**2 + h**2)

    start = 0, 1
    goal  = h-1, w-2
    visited = set()
    completed = set()

    # a star search, but invert heuristics
    open_set = [start]
    came_from = {}
    g_scores = defaultdict(lambda : INF)
    g_scores[start] = 0

    f_scores = defaultdict(lambda : INF)
    f_scores[start] = get_h(start, goal, max_heur)

    def get_best_f_score():
        best = None
        best_f = 0
        for n in open_set:
            if f_scores[n] >= best_f:
                best_f = f_scores[n]
                best = n
        return best
    
    current = None
    closed = set()
    while current != goal:    
        current = get_best_f_score()

        if current == goal:
            break

        open_set.remove(current)
        closed.add(current)

        y,x = current
        path_combos = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for y2, x2 in path_combos: 
            x2 += x
            y2 += y
            neighbour = (y2, x2)
         
            if y2 < 0 or y2 >= h or x2 < 0 or x2 >= w or data[y2][x2] == "#" or neighbour in closed:       
                continue

            tentative_g_score = g_scores[current] + 1

            if tentative_g_score < g_scores[neighbour]:
           
                came_from[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_scores[neighbour] = tentative_g_score + get_h(neighbour, goal, max_heur)
                if neighbour not in open_set:
                    open_set.append(neighbour)

     


    current = goal
    count = 0
    while current is not start:
        current = came_from[current]
        count += 1


    return count





if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
