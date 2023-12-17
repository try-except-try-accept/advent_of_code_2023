from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from random import randint
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
..//.|....///46"""

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
STATE_MIN = 5
DEBUG = False
DISPLAY_CUTOFF = 1000

class Beam:

    def __init__(self, y, x, grid, history, direction=EAST):
        
        self.y = y
        self.x = x
        self.direction = direction
        self.beam_id = randint(111, 999)
        self.grid = grid
        self.ENERGISE_MIRRORS = True        
        self.history = history

        self.off_grid = False

        p.bugprint(f"new {self.beam_id} heading", self.direction, "from", self.y, self.x)
        self.add_history()

    def hash(self):
        return f"{self.history}"


    def on_mirror_check(self):
        return self.get_tile() in "$/-|"

    def off_grid_check(self):
        off = self.x >= len(self.grid[0]) or self.y < 0 or self.y >= len(self.grid) or self.x < 0
  
        return off

    



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
        return Beam(self.y, self.x - 2, self.grid, self.history, direction=WEST)

    def split_vert(self):
        self.direction = NORTH
        self.y -= 1
        return Beam(self.y + 2, self.x, self.grid, self.history, direction=SOUTH)
    
    def update(self):
        if self.off_grid_check():   return None

        p.bugprint(f"running update for beam {self.beam_id}")

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
            p.bugprint(self.y, self.x, self.direction)
                   
            if new_cell == "/":
                new_beam = [self.go_right, self.go_up, self.go_left, self.go_down][self.direction]()
            elif new_cell == "$":
                new_beam = [self.go_left, self.go_down, self.go_right, self.go_up][self.direction]()
            elif new_cell == "-":
                new_beam = [self.split_horiz, self.go_right, self.split_horiz, self.go_left][self.direction]()
            elif new_cell == "|":
                new_beam = [self.go_up, self.split_vert, self.go_down, self.split_vert][self.direction]()
     
        self.add_history()
            
        if new_beam:
            p.bugprint(f"beam {self.beam_id} has spawned new beam {new_beam.beam_id}")
        return new_beam

    def get_symbol(self):

        return ["^", ">", "v", "<"][self.direction]

    def get_tile(self):
        return self.grid[self.y][self.x]

    def add_history(self):
        if not self.off_grid_check():
            tile = self.get_tile()
            self.history.add((self.y, self.x, self.get_symbol() if self.ENERGISE_MIRRORS or tile == "." else tile))

def display(grid, beams, h, w, history):
    s = ""
    trails = [list(row) for row in grid]
    energised = set([his[:2] for his in history])
    p.bugprint()

    if DEBUG:

        for y, x, sym in history:
            trails[y][x] = sym

        s = ""
        for row in trails:
            s += ("".join(row)) + "\n"

        print(s[:DISPLAY_CUTOFF])
        input()

    return len(energised)

def solve(data):
    p
    count = 0
    height = len(data)
    width = len(data[0])

    history = set()

    if len(data[-1]) == 0:
        data = data[:-1]

    p.bugprint(height, width)

    beams = []
    beams.append(Beam(0, 0, data, history))

    state_change = True

    energised = set()

    state_record = []

    last = None

    while state_change:
        p.bugprint("We have", len(beams), "beams")
        beams_to_create = []
        new_beams = [b.update() for b in beams]
        def remove_none(a):
            return a != None
        
        beams.extend(filter(remove_none, new_beams))
        state_record.append(display(list(data), beams, height, width, history))

        p.bugprint(state_record)
        state_change = len(state_record) < STATE_MIN or len(set(state_record[-STATE_MIN:])) > 1

    return state_record[-1]


def tests():

    TEST_CASES = '''
...$
....
$../
===10

.......$
.....|.|
.....$-/
===13

/////
===1

$/$/$../
\/$/$../
===12'''


    for test in TEST_CASES.split("\n\n"):

        grid, result = test.split("===")

        assert solve(grid.strip().splitlines()) == int(result)

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    #tests()

    if p.check(TESTS, solve):

        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
