from re import search, match, findall
from collections import Counter, defaultdict
from os import system
from helpers import PuzzleHelper, get_or_make_node
from math import sqrt, inf as INF, factorial
from copy import copy
PP_ARGS = False, False #rotate, cast int
from string import ascii_lowercase, ascii_uppercase
from random import choice, randint
NODE_LABELS = "".join([str(i) for i in range(10)]) + ascii_uppercase + ascii_lowercase

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

ANSI =  "\033[38;2;r;g;bm"

START_SYM = chr(53464)
END_SYM = chr(23424)
PRUNE_TOLERANCE = 10


glob_best_path = []

def get_rand_colour():
    rand_colour = lambda : str(randint(0, 255))
    return ANSI.replace("r", rand_colour()).replace("g", rand_colour()).replace("b", rand_colour())

def get_h(here, there, max_heur):
    x1, y1 = here
    x2, y2 = there
    return abs(x2-x1) + abs(y2-y1)

def visualise(data, paths, colour=RED):
    system("clear")
    print()
    s = ""
    for y in range(len(data)):
        for x in range(len(data[0])):
            char = BLACK + data[y][x]
            for i, p in enumerate(paths):
                if (y, x) in p:
                    char = colour + "█"
            s += char
        s += "\n"

    print(s)
 
     
def check_bounds(y, x, h, w):
    return 0 <= y < h and 0 <= x < w

def solve(data):


    def find_vertices():
        vertex_num = 0
        maze = [list(row) for row in data]
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell == ".":
                    neighbours = ""
                    for y2, x2 in MOVEMENTS:
                        y2 += y
                        x2 += x
                        if check_bounds(y2, x2, h, w):
                            neighbours += data[y2][x2]
                    
                    if neighbours.count("#") < 2:
                        label = NODE_LABELS[vertex_num]
                        maze[y][x] = label
                        vertex_num += 1
                        vertices[(y, x)] = label
        return vertices, maze
    
    def find_reg_vertices(block_h, block_w):

        vertex_num = 0
        maze = [list(row) for row in data]

        for y in range(3, h-3, h//block_h):
            for x in range(3, w-3, w//block_w):
                moves = list(MOVEMENTS)
                y_new = y
                x_new = x
                valid_vertex = maze[y_new][x_new] != "#"

                while not valid_vertex:
                    this_move = moves.pop(0)
                    y_new = y + this_move[0]
                    x_new = x + this_move[1]
                    print("Checking", y_new, x_new)
                    if check_bounds(y_new, x_new, h, w):
                        valid_vertex = maze[y_new][x_new] != "#"

                label = NODE_LABELS[vertex_num]
                maze[y_new][x_new] = label
                vertex_num += 1
                vertices[(y_new, x_new)] = label

        return vertices, maze



    h, w = len(data), len(data[0])
    vertices = {}

    vertices, maze = find_vertices()

    # vertex_sort = sorted(list(vertices.keys()), key=lambda x: x[1])
    # vertex_sort = sorted(vertex_sort)

    # for i, v in enumerate(vertex_sort):
    #     this_label = NODE_LABELS[i]
    #     vertices[v] = this_label
    #     maze[v[0]][v[1]] = this_label 


    vertices[(0, 1)] = START_SYM
    vertices[(h-1, w-2)] = END_SYM
         

    
    g = {}

    # set up weighted graph

    for row in maze:
        print("".join(row))
    input()

    for vertex, label in vertices.items():
        g[label] = get_or_make_node(label, g, vertex)
        paths = [[vertex]]

        #print(label, "connects to")
        
        while len(paths):
            path = paths.pop(0)
            y, x = path[-1]
            n_coords = (y, x)

            if n_coords in vertices.keys() and n_coords != vertex:
                #print("\t", maze[y][x],  "in", len(path), "steps")
                neighbour = get_or_make_node(vertices[n_coords], g, n_coords)
                g[label].add_connection(neighbour, path)
                continue

            for y2, x2 in MOVEMENTS:
                y2 += y
                x2 += x
                next_coord = (y2, x2)
                if (not check_bounds(y2, x2, h, w)) or data[y2][x2] == "#" or next_coord in path:
                    continue
                paths.insert(0, path + [next_coord])

    ## prim's algorithm: find maximum spanning subtree
    

    def prim():
        # choose random vertex
        current = choice(list(g.values()))
        subtree = set()
        subtree.add(current)
        # repeat until all vertices added            
        while len(subtree) != len(g.values()):
            # choose shortest edge
            subtree.add(current.get_neighbours(nearest=True, num=1))
            print([str(s) for s in subtree])
            # choose nearest vertex
            x = current
            q = [current]
            while x in subtree:
                x = q.pop(0)
                q = list(current.get_neighbours()) + q
            subtree.add(x)
            
    
                
    ## find furthest node that is unvisited
                

    ## dijkstra's for longest path
                
    unvisited = list(g.values())
    
   
    
    def get_manhattan(node, neighbour):
        x1, y1 = node.extra
        x2, y2 = neighbour.extra
        return abs(x1-x2) + abs(y1-y2)
    

    def find_longest_path(unvisited):

        current = g[START_SYM]
        cost = 0
        path = []
        while unvisited:
            print(f" current is {current}")
            unvisited.remove(current)
            best_cost = 0
            best_manhattan = 0
            best_path = []
            for neighbour, this_path in current.connections.values():
                #print(f"neighbour is {neighbour}")
                if neighbour not in unvisited:
                    #print("skipping")
                    continue
                weight = len(this_path)
                this_manhattan = get_manhattan(current, neighbour)
                
                if weight > best_cost or \
                    weight == best_cost and this_manhattan > best_manhattan:
                    next_current = neighbour
                    best_cost = weight
                    best_manhattan = this_manhattan
                    best_path = this_path
            print(f"Best path is from {current} to {next_current}")
            print(best_path)
            
            current = next_current
            cost += best_cost
            path += best_path
            visualise(maze, [path])
            input()
        print(path)
        print(len(path), "pathy")
        
        input()
        return set(path), len(set(path)) - 1



    def dijkstra(unvisited):

        def walk_path(neighbour, prev):
            current = neighbour
            while current not in [start]:
                current = prev[current]
                yield str(current)
        
        def get_best_node(unvisited, dists):
            best_distance = INF
            best = None
            for node in unvisited:
                if dists[node] <= best_distance:
                    best_distance = dists[node]
                    best = node
            return best
        
        dists = {node:INF  for node in g.values()}
        prev =  {node:None for node in g.values()}
        best_paths =  {node:[] for node in g.values()}

        start, end = g[START_SYM], g[END_SYM]
        
        dists[start] = 0
        current = None

 
        while unvisited:
            current = get_best_node(unvisited, dists)
            unvisited.remove(current)
            for neighbour, path in sorted(list(current.connections.values()), key=lambda c:c[1]):
                if neighbour in unvisited:
                    tentative_distance = (dists[current] + (len(path)))
                    if tentative_distance <= dists[neighbour]:
                        dists[neighbour] = tentative_distance
                        prev[neighbour] = current
                        best_paths[neighbour] = best_paths[current] + path
                        print(f"Best path from start to {neighbour} is", list(walk_path(neighbour, prev)))
        
        final = set(best_paths[end])
        visualise(maze, [final])




    

        
    def brute_force():

        vertices = g.keys()
        n = len(vertices)

        print(f"{n} vertices found... brute force will take {factorial(n)} attempts...")
        input()

        home = g[START_SYM]
        best_path, _ = explore_paths(home)

        visualise(maze, [best_path])

        return len(best_path) + n - 1
    

    def hash_path(neighbour, visited_copy):
        return hash(str(neighbour) + "".join([str(n) for n in visited_copy]))

    cache = {}

    # start at home
    def explore_paths(node, all_path=None, visited=None, best_path=None, d=0, colour=RED):
        if visited is None:
            visited = []
            all_path = set()
            best_path = []
        
        visited.append(node)

        #visualise(maze, [all_path], colour)

        #print(" " * d, f"visiting {node}")

        # prune if current_path + area of remaining search space < known best

        y, x = node.extra
        if best_path and x > (w // PRUNE_TOLERANCE) * (PRUNE_TOLERANCE-1):
            area_left = (w-x) * (h-y)
            if len(all_path) + area_left < len(best_path):
                #print("pruney")
                return best_path, colour

        
        if node == g[END_SYM]:
            if len(all_path) > len(best_path):
                best_path = list(all_path)
       
            
        else:
            # find all neighbours
            no_neighbours = True
            #print(" " * d, f"finding neighbours of {node}")
            #print(" " * d, [str(n[0]) for n in node.connections.values()])
            for neighbour, path in node.connections.values():

                if neighbour in visited:
                    continue
                #print(" " * d, f"now visited {neighbour}")
                
                no_neighbours = False
                all_path_copy = copy(all_path)
                this_path = set(node.connections[neighbour.data][1])

                this_path.remove(neighbour.extra)
                this_path.remove(node.extra)
                
                if all_path_copy.intersection(this_path):
                    print("path clash")
                    continue


                

            
                
                all_path_copy |= this_path
                visited_copy = copy(visited)



                path_hash = hash_path(neighbour, visited_copy)


                data = cache.get(path_hash)

                if data is None:
                    data = explore_paths(neighbour, all_path_copy, visited_copy, best_path, d+1, colour)
                    cache[path_hash] = data
                    best_path, colour = data
           
                

                # recurse for each neighbour (general case)

            if no_neighbours:
                colour = get_rand_colour()
                #input("DEAD END")

        return best_path, colour
    

    def path_poly_scan_search(unvisited):

        # find approx reg perimeter of previous path

        # scan perim in current direction

        # if no more in that direction

        # switch

        # SNAKE 1: east east east south west west west south east east east south west west west

        # SNAKE 2: south south south east north north north east south south south east

        current = g[START_SYM]

        while current != g[END_SYM]:

            neighbours = current.connections

            if len(neighbours) == 1:
                print("Only one neighbour")
                chosen = neighbours[0]
                current = chosen[0]
                path += chosen[1]
            
            else:
                
                neighbours = sorted(neighbours, key=lambda n: n.data[1])
                







    def choose_path(unvisited):



        all_paths = []
        

        current = g[START_SYM]

        while unvisited:
            unvisited.remove(current)

            if not unvisited:
                return len(set(all_paths)) - 1
            
            valid_vertex = False
            neighbours = current.connections.keys()
            
            options = set(neighbours).intersection(set([str(n) for n in unvisited]))

            if len(options) == 1:
                next_vertex = list(options)[0]
                print(f"No choice, next vertex is {next_vertex}")
            else:
                while not valid_vertex:
                    
                    print("Which path?")
                    print(options)
                    print()
                    next_vertex = input()

                    if next_vertex not in options:
                        print("Already visited")
                        continue

                    
                    
                    valid_vertex = True

            all_paths += current.connections[next_vertex][1]
            print(all_paths)
            current = g[next_vertex]
            
            visualise(maze, [all_paths])

        return len(all_paths)
    


    def dfs_vertices():

        current = g[START_SYM]
        colour = get_rand_colour()
        stack = [(colour, [current])]

        best_path = []

        while stack:
            colour, this_path = stack.pop(0)
            current = this_path[-1]

            if current == g[END_SYM]:
                path_through = set()
                for i in range(len(this_path)-1):
                    path_through |= set(this_path[i].connections[this_path[i+1].data][1])
            
                #visualise(maze, [path_through], colour=colour)
                if len(path_through) > len(best_path):
                    best_path = path_through
            
            conns_found = 0
            for neighbour, new_path in current.connections.values():
                if neighbour not in this_path:
                    stack.insert(0, (colour, this_path + [neighbour]))
                    conns_found += 1

            #     if conns_found == 1:
            #         colour = get_rand_colour()

            # if conns_found == 0:
            #     print("DEAD END")

        return len(best_path) - 1

    return dfs_vertices()

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
        
            paths.insert(-1, path + [next_coord])
            
  

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
        try:
            puzzle_input = p.load_puzzle()
            puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
            print("FINAL ANSWER: ", solve(puzzle_input))
        except KeyboardInterrupt:
            print("POSS ANSWER:", max(glob_all_paths))

        
