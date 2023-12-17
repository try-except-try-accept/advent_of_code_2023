from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from random import randint
from time import time as default_timer
import multiprocessing, logging

PP_ARGS = False, False #rotate, cast int

DAY = 16
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """.|...$....
|.-.$.....
.....|-...
........|.
..........
.........$
..../.$$..
.-.-/..|..
.|....-|.$
..//.|....///51"""

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
STATE_MIN = 5
DEBUG = False
DISPLAY_CUTOFF = 1000


### refactor Beam as Ray class

### Beam then becomes containing class

### If Beam enters cached y, x, direction at any point

    ### Total energy that beam will produce is known

### If all rays in a beam have gone off grid

    ### Return history of all rays in beam and add to cache - overall length of history = energy 



class MyTimer(object):
    """Timer object context manager to time process speed"""
    def __init__(self, task_num, total):
        self.task_num = task_num
        self.total_tasks = total

    def __enter__(self):
        self.start = default_timer()
        
    def __exit__(self, type, value, traceback):
        logger = create_logger()
        self.end = default_timer()
        duration = self.end-self.start
        print(f"That took {duration} seconds.\n")
        left = self.total_tasks - self.task_num
        print(f"ESTIMATED TIME REMAINING to complete {left} tasks: {convert_seconds(duration * left)} remaining")

def create_logger():
    import multiprocessing, logging
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(\
        '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
    handler = logging.FileHandler('loggy.txt')
    handler.setFormatter(formatter)

    # this bit will make sure you won't have 
    # duplicated messages in the output
    if not len(logger.handlers): 
        logger.addHandler(handler)
    return logger 

def convert_seconds(seconds):
    days = seconds // (24 * 3600)
    seconds %= 24 * 3600
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} mins and {seconds} seconds"        

class Beam:

    def __init__(self, y, x, history, direction, width, height, grid):
        
        self.y = y
        self.x = x
        self.direction = direction
        self.beam_id = randint(111, 999)
        self.ENERGISE_MIRRORS = False        
        self.spawn = None
        self.history = set()
        self.off_grid = False
        self.width = width
        self.height = height
        self.grid = grid      
        self.add_history()

    def __str__(self):
        return f"{self.y}|{self.x}|{self.direction}"

    def get_key(self):
        return (self.y, self.x, self.direction)

    def on_mirror_check(self):
        return self.get_tile() in "$/-|"

    def off_grid_check(self):
        self.off = self.x >= self.width or self.y < 0 or self.y >= self.height or self.x < 0
        return self.off

    def go_right(self):
        self.direction = EAST
        self.x += 1

    def go_left(self):
        self.direction = WEST
        self.x -= 1

    def go_up(self):
        self.direction = NORTH
        self.y -= 1

    def go_down(self):
        self.direction = SOUTH
        self.y += 1

    def split_horiz(self):
        self.direction = EAST
        self.x += 1
        self.spawn = Beam(self.y, self.x - 2, self.history, WEST, self.width, self.height, self.grid)

    def split_vert(self):
        self.direction = NORTH
        self.y -= 1
        self.spawn = Beam(self.y + 2, self.x, self.history, SOUTH, self.width, self.height, self.grid)

    def end(self):

        return self.history

    def get_spawn(self):
        spawn = self.spawn
        self.spawn = None
        return spawn
    
    def update(self):
        
        

        cached = beam_cache.get((self.y,self.x,self.direction))

        if cached is not None:
            return cached

        changemap = {NORTH:(-1, 0),
                     EAST: (0, 1),
                     SOUTH:(1, 0),
                     WEST: (0, -1)}

        new_beam = None
        if not self.on_mirror_check():
            change = changemap[self.direction]
            self.y += change[0]
            self.x += change[1]

        else:
            new_cell = self.get_tile()            
            
            if new_cell == "/":
                new_beam = [self.go_right, self.go_up, self.go_left, self.go_down][self.direction]()
            elif new_cell == "$":
                new_beam = [self.go_left, self.go_down, self.go_right, self.go_up][self.direction]()
            elif new_cell == "-":
                new_beam = [self.split_horiz, self.go_right, self.split_horiz, self.go_left][self.direction]()
            elif new_cell == "|":
                new_beam = [self.go_up, self.split_vert, self.go_down, self.split_vert][self.direction]()
     
        self.add_history()
        

    def get_symbol(self):

        return ["^", ">", "v", "<"][self.direction]

    def get_tile(self):
        return self.grid[self.y][self.x]

    def add_history(self):
        if not self.off_grid_check():
            tile = self.get_tile()
            self.history.add((self.y, self.x, self.direction, self.get_symbol() if self.ENERGISE_MIRRORS or tile == "." else tile))

def display(beams, grid):
    s = ""
    trails = [list(row) for row in grid]
    energised = set([his[:2] for his in history])


    if DEBUG:
        for y, x, _ , sym in history:
            trails[y][x] = sym

        s = ""
        for row in trails:
            s += ("".join(row)) + "\n"

        print(s[:DISPLAY_CUTOFF])
   

    return len(energised)


cache = {}



def solve(data):

    if len(data[-1]) == 0:
        data = data[:-1]


    grid = tuple(data)


    return construct_tests(grid)


    # top row
    results = set()
    task_num = 1
    total_tasks = self.width + self.width + HEIGHT + HEIGHT
    
    for x in range(w):
        with MyTimer(task_num, total_tasks) as t:
            results.add(beam_until_no_change(0, x, SOUTH))
        with MyTimer(task_num, total_tasks) as t:
            results.add(beam_until_no_change(h-1, x, NORTH))
            
    for y in range(h):
        with MyTimer(task_num, total_tasks) as t:
            results.add(beam_until_no_change(y, 0, EAST))
        with MyTimer(task_num, total_tasks) as t:
            results.add(beam_until_no_change(y, w-1, WEST))

    return max(results)


def remove_none(a):
    return a != None


def hash_beams(history, beams):
    return hash(str(history)+",".join(str(b) for b in beams if not b.off))

beam_cache = {}

def beam_until_no_change(start_y, start_x, direction, w, h, grid):
    global DEBUG
    print(f"Beaming from row {start_y} column {start_x}")
  
    beams = []
    beams.append(Beam(start_y, start_x, None, direction, w, h, grid))
    state_change = True
    energised = set()
    state_record = []
    last = None

    max_tiles = w * h
    energised = 0

    while state_change:
        beam_hash = hash_beams(history, beams)
        next_move = cache.get(beam_hash)

        # go through each beam
        new_beams = []
        ended_beams = []
        for beam in beams:
            # update beam
            beam.update()

            cache_result = cache.get(beam.get_key())

            if cache_result is not None:
                print("Beam {beam.beam_id} found in cache.")
                ended_beams.append(beam)
                energised += cache_result
            elif beam.off:
                print(f"Beam {beam.beam_id} went off grid, so adding to cache")
                for y, x, direction, _ in beam.history:
                    cache[(y,x,direction)] = len(beam.history)
                ended_beams.append(beam)
                energised += len(beam.history)
            
        # spawn new beams
        beams.extend(new_beams)

        # remove ended beams
        for removed in ended_beams:
            beams.remove(removed)

        

        state_record.append(display(beams, grid))
        
        state_change = len(state_record) < STATE_MIN or len(set(state_record[-STATE_MIN:])) > 1

    print(f"results in {state_record[-1]} out of {max_tiles} tiles energised")

    return energised


def beam_from_perim(y1, y2, x1, x2, direction, total_tasks, w, h, grid):
    logger = create_logger()
    logger.info('Starting pooling')

    #y1, y2, x1, x2, direction = final_tests
    this_proc_results = set()

    task_num = 1
    

    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            with MyTimer(task_num, total_tasks) as t:
                this_proc_results.add(beam_until_no_change(x, y, direction, w, h, grid))
                task_num += 1
 
    return this_proc_results

def construct_tests(grid):
    results = set()
    W, H = len(grid[0]), len(grid)
    total_tasks = (W + W + H + H)
    
    final_tests = ((0,      0,      0,      W//2,   EAST, total_tasks, W, H, grid),
                   (0,      0,      W//2,   W,      EAST, total_tasks, W, H, grid),
                   (H-1  ,   H-1,    0,      W//2,   WEST, total_tasks, W, H, grid),
                   (H-1,    H-1,    W//2,   W,      WEST, total_tasks, W, H, grid),
                   (0,      H//2,   0,      0,      SOUTH, total_tasks, W, H, grid),
                   (H//2,   H,      0,      0,      SOUTH, total_tasks, W, H, grid),
                   (0,      H//2,   W-1,    W-1,    NORTH, total_tasks, W, H, grid),
                   (H//2,   H,      W-1,    W-1,    NORTH, total_tasks, W, H, grid))

    
    for x in range(W):
        for y in range(H):
            for direction in range(4):
                beam_cache[(y,x,direction)] = None
                

    for y1, y2, x1, x2, direction, total_tasks, W, H, grid in final_tests:
        results |= beam_from_perim(y1, y2, x1, x2, direction, total_tasks, W, H, grid)


    # abandoned multiprocessing
##    print("Starting a pool party...")
##    with multiprocessing.Pool() as pool:
##        for result in pool.starmap(beam_from_perim, final_tests):
##            results |= result
##    print("The pool party's over!!!")

    return max(results)
    

    



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    #tests()

    

    if p.check(TESTS, solve):
        input()

        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
