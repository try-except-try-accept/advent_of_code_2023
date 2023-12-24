from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import ceil
from math import inf as INF

PP_ARGS = False, False #rotate, cast int

DAY = 22
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9///5"""

DEBUG = True

'''
 x
012
.G. 9
.G. 8       G can fall because its min is 8 and F's max is 7
... 7
FFF 6
..E 5 z
D.. 4
CCC 3
BBB 2
.A. 1
--- 0
'''

class Brick:
    def __init__(self, label, data):
        self.label = label
        coord1, coord2 = data.split("~")
        x1, y1, z1 = map(int, coord1.split(","))
        x2, y2, z2 = map(int, coord2.split(","))
        self.cubes = set()
        self.mins = [min(x1, x2), min(y1, y2), min(z1,z2)]
        self.maxes = [max(x1, x2), max(y1, y2), max(z1,z2)]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    self.cubes.add((x, y, z))

        self.fell = False


        
    def __lt__(self, other):
        return self.mins[2] < other.maxes[2]
    
    def can_fall_past(self, other):
        """Check if block can fall past other block, based on axis 0 (x) or 1 (y)"""
        print(f"Check if brick {self.label} can fall past {other.label}")

  
 

class Stack:
    def __init__(self, data):
        self.bricks = sorted([Brick(chr(65+i), row) \
                              for i, row in enumerate(data)], \
                                reverse=True)
        
        self.maxes = (max(self.bricks, key=lambda b: b.maxes[0]).maxes[0],
                      max(self.bricks, key=lambda b: b.maxes[1]).maxes[1],
                      max(self.bricks, key=lambda b: b.maxes[2]).maxes[2])



    def settle_bricks(self):
        """Allow all bricks to fall to their minimum y position"""
        settled = False
        max_pass = len(self.bricks) - 1
        while not settled:
            settled = True
            for i in range(0, max_pass):
                this_block = self.bricks[i]
                that_block = self.bricks[i+1]
                falls_through = this_block.can_fall_past(that_block)
                if falls_through:
                    settled = False
                    print("Swapped", this_block.label, "and", that_block.label)
                    print(self.draw())
                    self.bricks[i], self.bricks[i+1] = self.bricks[i+1], self.bricks[i]
                    input()
            max_pass -= 1

    def draw(self, normal_facing=True):
        """Draw the stack from the given perspective"""
        h_index, h_label = 0, "x"
        if not normal_facing:
            h_index, h_label = 1, "y"
        
        h_labels = ("".join(hex(h)[-1] for h in range(self.maxes[h_index]+1)))
        bottom_bar = ("-" * (self.maxes[h_index]+1)) + " 0"
        stack_print = h_label.center(len(h_labels)) + "\n" + h_labels + "\n"
        laid = 0
        z_label = ceil(self.maxes[2] / 2)

        for z in range(self.maxes[2], 0, -1):
            for x in range(self.maxes[h_index]+1):
                bricks_at_this_pos = set()
                for b in self.bricks[laid:]:
                    for cube in b.cubes:
                        if cube[h_index] == x and cube[2] == z:
                            bricks_at_this_pos.add(b.label)
                            brick = b.label

                if len(bricks_at_this_pos) > 1:
                    stack_print += "?"
                elif len(bricks_at_this_pos):
                    stack_print += brick
                else:
                    stack_print += "."

            if len(bricks_at_this_pos):
                laid += 1
            stack_print += f' {z}{" z" if z == z_label else ""}\n'

        return stack_print + bottom_bar


def solve(data):
    s = Stack(data)
    print("Normal")
    print(s.draw(True))
    print("Side facing")
    print(s.draw(False))
    input()
    s.settle_bricks()
    print("Settled")
    print(s.draw(True))
    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
